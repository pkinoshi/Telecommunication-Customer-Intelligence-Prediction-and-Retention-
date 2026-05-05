"""
ui/counterfactuals.py
---------------------
Renders the counterfactual retention scenarios (DiCE output) when a
customer is predicted to churn, and a retention tip when they are not.
"""

import streamlit as st
import pandas as pd

from config import FEATURES_TO_VARY, FEATURE_LABELS
from model import run_dice


# ── Helpers ───────────────────────────────────────────────────────────────────
def _arrow_style(col: str, original_val, new_val) -> tuple[str, str]:
    """
    Return (arrow_symbol, hex_colour) for a changed feature.
    MonthlyCharges gets directional arrows; all other changes use →.
    """
    if col == "MonthlyCharges":
        try:
            if float(new_val) < float(original_val):
                return "↓", "#4ade80"   # decrease = good (green)
            return "↑", "#f87171"       # increase = bad (red)
        except (ValueError, TypeError):
            pass
    return "→", "#a78bfa"               # categorical change (purple)


def _render_cf_card(col_label: str, original_val, new_val: str) -> None:
    """Render a single feature-change card."""
    arrow, color = _arrow_style(col_label.split(" (")[0], original_val, new_val)
    # col_label is the human name; we pass the raw col separately where needed
    st.markdown(
        f'<div class="cf-card">'
        f'  <div style="color:#94a3b8;font-size:0.78rem;text-transform:uppercase;letter-spacing:0.05em">'
        f'    {col_label}'
        f'  </div>'
        f'  <div style="color:#cbd5e1;font-size:0.9rem;margin:6px 0 2px;text-decoration:line-through">'
        f'    {original_val}'
        f'  </div>'
        f'  <div style="font-size:1.4rem;color:{color};font-weight:700">'
        f'    {arrow} {new_val}'
        f'  </div>'
        f'</div>',
        unsafe_allow_html=True,
    )


def _render_scenario(scenario_idx: int, cf_row: pd.Series, inputs: dict) -> None:
    """Render one DiCE scenario: header, change count, and changed-feature cards."""
    st.markdown(f"### Scenario {scenario_idx}")

    changed_cols = [
        c for c in FEATURES_TO_VARY
        if str(inputs.get(c, "")) != str(cf_row.get(c, ""))
    ]
    unchanged_count = len(FEATURES_TO_VARY) - len(changed_cols)

    st.markdown(
        f'<p style="color:#94a3b8;font-size:0.88rem">'
        f'<strong style="color:#4ade80">{len(changed_cols)} change(s)</strong> required · '
        f'{unchanged_count} features unchanged</p>',
        unsafe_allow_html=True,
    )

    if not changed_cols:
        st.info("No actionable changes found for this scenario.")
        return

    grid_cols = st.columns(min(len(changed_cols), 3))
    for idx, col in enumerate(changed_cols):
        original_val = inputs.get(col, "—")
        new_val      = cf_row.get(col, "—")
        if isinstance(new_val, float):
            new_val = round(new_val, 2)

        with grid_cols[idx % 3]:
            _render_cf_card(FEATURE_LABELS.get(col, col), original_val, new_val)

    st.markdown("---")


# ── Public renderers ──────────────────────────────────────────────────────────
def render_counterfactuals(
    model_pipeline,
    df_raw: pd.DataFrame,
    query_df: pd.DataFrame,
    inputs: dict,
    n_cfs: int,
) -> None:
    """
    Entry point for the counterfactual section.
    Called only when the model predicts churn.
    """
    st.markdown("## 💡 Retention Scenarios — What Would Keep This Customer?")
    st.markdown(
        "The model found the **minimum changes** to flip the prediction to **Stay**. "
        "Unchanged fields are hidden. 🟢 Green = favourable, 🔴 Red = charge increase."
    )

    with st.spinner(f"Generating {n_cfs} retention scenarios… (15–30 seconds)"):
        try:
            dice_result = run_dice(model_pipeline, df_raw, query_df, n_cfs=n_cfs)
            cf_df       = dice_result.cf_examples_list[0].final_cfs_df

            if cf_df is None or cf_df.empty:
                st.warning("DiCE could not find valid counterfactuals. Try adjusting the customer profile.")
                return

            cf_df = cf_df.drop(columns=["Churn"], errors="ignore")
            for idx, (_, cf_row) in enumerate(cf_df.iterrows(), 1):
                _render_scenario(idx, cf_row, inputs)

        except Exception as exc:
            st.error(f"DiCE encountered an error: {exc}")
            st.info("Tip: Make sure `df_cleaned_raw.csv` matches the training data used to build the pipeline.")


def render_no_churn_tip() -> None:
    """Positive reinforcement card shown when the customer is not predicted to churn."""
    st.markdown("## ✅ Retention Actions")
    st.markdown(
        '<div class="metric-card">'
        '<p style="color:#86efac;font-size:1rem;margin:0">'
        'This customer is <strong>not predicted to churn</strong>. No immediate intervention needed.<br><br>'
        '💡 <strong>Tip:</strong> Continue monitoring if their contract is month-to-month or their '
        'monthly charges are high — those are the strongest churn signals in this model.'
        '</p></div>',
        unsafe_allow_html=True,
    )
