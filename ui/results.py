"""
ui/results.py
-------------
Renders the prediction result section:
  - render_landing()         : placeholder shown before first prediction
  - render_result_banner()   : churn / no-churn verdict card
  - render_probability_gauge(): probability percentage bar
  - render_profile_summary() : expandable customer profile breakdown
"""

import streamlit as st

from config import FEATURE_LABELS


# ── Landing state ─────────────────────────────────────────────────────────────
def render_landing() -> None:
    """Three-step instruction cards shown before the user runs any prediction."""
    col1, col2, col3 = st.columns(3)
    steps = [
        ("Step 1", "Fill in customer details in the sidebar"),
        ("Step 2", "Click <strong>Run Prediction</strong>"),
        ("Step 3", "If churn risk is high, explore retention scenarios"),
    ]
    for col, (title, body) in zip([col1, col2, col3], steps):
        with col:
            st.markdown(
                f'<div class="metric-card">'
                f'<h3 style="color:#a78bfa;margin:0">{title}</h3>'
                f'<p style="color:#94a3b8;margin:8px 0 0">{body}</p>'
                f'</div>',
                unsafe_allow_html=True,
            )


# ── Verdict banner ────────────────────────────────────────────────────────────
def render_result_banner(will_churn: bool) -> None:
    """Large card communicating High / Low churn risk."""
    if will_churn:
        st.markdown(
            '<div class="churn-card">'
            '<div style="font-size:3rem">⚠️</div>'
            '<h2 style="color:#f87171;margin:8px 0">High Churn Risk</h2>'
            '<p style="color:#fca5a5;font-size:1.1rem;margin:0">This customer is likely to leave</p>'
            '</div>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            '<div class="safe-card">'
            '<div style="font-size:3rem">✅</div>'
            '<h2 style="color:#4ade80;margin:8px 0">Low Churn Risk</h2>'
            '<p style="color:#86efac;font-size:1.1rem;margin:0">This customer is likely to stay</p>'
            '</div>',
            unsafe_allow_html=True,
        )


# ── Probability gauge ─────────────────────────────────────────────────────────
def render_probability_gauge(churn_prob: float) -> None:
    """Numeric percentage + filled progress bar."""
    pct       = int(churn_prob * 100)
    bar_color = "#ef4444" if pct >= 50 else "#22c55e"
    label     = "Above 50% = predicted churn" if pct >= 50 else "Below 50% = predicted to stay"

    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.markdown("**Churn Probability**")
    st.markdown(
        f'<div style="font-size:2.5rem;font-weight:700;color:{bar_color};text-align:center">{pct}%</div>'
        f'<div class="probability-bar-container">'
        f'  <div style="width:{pct}%;height:100%;background:{bar_color};border-radius:8px;transition:width 0.5s"></div>'
        f'</div>'
        f'<p style="color:#94a3b8;font-size:0.82rem;text-align:center;margin:4px 0">{label}</p>',
        unsafe_allow_html=True,
    )
    st.markdown('</div>', unsafe_allow_html=True)


# ── Customer profile expander ─────────────────────────────────────────────────
def render_profile_summary(inputs: dict) -> None:
    """Collapsible expander showing the full customer profile in three columns."""
    demo_keys    = ["gender", "SeniorCitizen", "Partner", "Dependents"]
    account_keys = ["tenure", "Contract", "PaperlessBilling", "PaymentMethod",
                    "MonthlyCharges", "TotalCharges"]
    service_keys = ["PhoneService", "MultipleLines", "InternetService", "OnlineSecurity",
                    "OnlineBackup", "DeviceProtection", "TechSupport",
                    "StreamingTV", "StreamingMovies"]

    with st.expander("📋 Customer Profile Summary", expanded=False):
        c1, c2, c3 = st.columns(3)
        for col, keys, heading in [
            (c1, demo_keys,    "**Demographics**"),
            (c2, account_keys, "**Account**"),
            (c3, service_keys, "**Services**"),
        ]:
            with col:
                st.markdown(heading)
                for k in keys:
                    st.markdown(f"- **{FEATURE_LABELS[k]}:** {inputs[k]}")
