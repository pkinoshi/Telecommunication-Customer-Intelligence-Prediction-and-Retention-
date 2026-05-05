"""
app.py
------
Entry point. Orchestrates the app flow:
  1. Page config + CSS
  2. Load artifacts
  3. Render sidebar → collect inputs
  4. On prediction click → predict → render results
  5. If churn → run DiCE → render retention scenarios
"""

import streamlit as st

from ui.styles        import inject_styles
from ui.sidebar       import render_sidebar
from ui.results       import (
    render_landing,
    render_result_banner,
    render_probability_gauge,
    render_profile_summary,
)
from ui.counterfactuals import render_counterfactuals, render_no_churn_tip
from model            import load_artifacts, build_input_df, predict

# ── Page config (must be the very first Streamlit call) ───────────────────────
st.set_page_config(
    page_title="Customer Churn Predictor",
    page_icon="📡",
    layout="wide",
    initial_sidebar_state="expanded",
)
inject_styles()

# ── Load artifacts ────────────────────────────────────────────────────────────
try:
    model_pipeline, target_encoder, df_raw = load_artifacts()
    artifacts_loaded = True
except Exception as exc:
    artifacts_loaded = False
    load_error       = str(exc)

# ── Sidebar ───────────────────────────────────────────────────────────────────
inputs, n_cfs, predict_clicked = render_sidebar()

# ── Page header ───────────────────────────────────────────────────────────────
st.markdown("# 📡 Customer Churn Intelligence")
st.markdown("*Enter customer details in the sidebar, then click **Run Prediction**.*")
st.markdown("---")

# ── Guard: artifact load failure ──────────────────────────────────────────────
if not artifacts_loaded:
    st.error(
        f"**Could not load model files.** "
        f"Ensure these files are in the same folder as `app.py`:\n"
        f"- `churn_model_pipeline.pkl`\n"
        f"- `target_encoder.pkl`\n"
        f"- `df_cleaned_raw.csv`\n\n"
        f"Error: `{load_error}`"
    )
    st.stop()

# ── Guard: nothing predicted yet ──────────────────────────────────────────────
if not predict_clicked:
    render_landing()
    st.stop()

# ── Prediction ────────────────────────────────────────────────────────────────
query_df = build_input_df(inputs)

with st.spinner("Running prediction..."):
    churn_prob, churn_label = predict(model_pipeline, query_df)

will_churn = churn_label == 1

# ── Result layout ─────────────────────────────────────────────────────────────
col_verdict, col_gauge = st.columns([2, 1])
with col_verdict:
    render_result_banner(will_churn)
with col_gauge:
    render_probability_gauge(churn_prob)

st.markdown("---")
render_profile_summary(inputs)

# ── Counterfactuals or retention tip ─────────────────────────────────────────
if will_churn:
    render_counterfactuals(model_pipeline, df_raw, query_df, inputs, n_cfs)
else:
    render_no_churn_tip()

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown(
    '<p style="color:#475569;text-align:center;font-size:0.8rem">'
    "Churn Intelligence Dashboard · Powered by Logistic Regression + DiCE Counterfactuals"
    "</p>",
    unsafe_allow_html=True,
)
