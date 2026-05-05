"""
ui/sidebar.py
-------------
Renders the customer-input form in the Streamlit sidebar.
Returns a plain dict of field values plus the UI controls
(predict button, n_cfs slider) so app.py can act on them.
"""

import streamlit as st

from config import FEATURE_OPTIONS, FEATURE_LABELS, NUMERIC_BOUNDS


def render_sidebar() -> tuple[dict, int, bool]:
    """
    Render the full sidebar form.

    Returns
    -------
    inputs : dict
        Raw field values keyed by column name (strings / numbers, not encoded).
    n_cfs : int
        Number of DiCE counterfactual scenarios requested.
    predict_clicked : bool
        True when the user pressed the Run Prediction button.
    """
    with st.sidebar:
        st.markdown("## 📋 Customer Details")
        st.markdown("---")

        inputs = {}

        # ── Demographics ──────────────────────────────────────────────────────
        st.markdown('<p class="section-header">👤 Demographics</p>', unsafe_allow_html=True)
        for col in ["gender", "SeniorCitizen", "Partner", "Dependents"]:
            inputs[col] = st.selectbox(FEATURE_LABELS[col], FEATURE_OPTIONS[col])

        st.markdown("---")

        # ── Account info ──────────────────────────────────────────────────────
        st.markdown('<p class="section-header">📄 Account Info</p>', unsafe_allow_html=True)

        tenure_bounds  = NUMERIC_BOUNDS["tenure"]
        inputs["tenure"] = st.slider(
            FEATURE_LABELS["tenure"],
            tenure_bounds["min"], tenure_bounds["max"], tenure_bounds["default"],
        )

        for col in ["Contract", "PaperlessBilling", "PaymentMethod"]:
            inputs[col] = st.selectbox(FEATURE_LABELS[col], FEATURE_OPTIONS[col])

        monthly_bounds = NUMERIC_BOUNDS["MonthlyCharges"]
        inputs["MonthlyCharges"] = st.number_input(
            FEATURE_LABELS["MonthlyCharges"],
            min_value=float(monthly_bounds["min"]),
            max_value=float(monthly_bounds["max"]),
            value=float(monthly_bounds["default"]),
            step=float(monthly_bounds["step"]),
        )

        total_default = round(inputs["tenure"] * inputs["MonthlyCharges"], 2)
        total_bounds  = NUMERIC_BOUNDS["TotalCharges"]
        inputs["TotalCharges"] = st.number_input(
            FEATURE_LABELS["TotalCharges"],
            min_value=float(total_bounds["min"]),
            max_value=float(total_bounds["max"]),
            value=float(total_default),
            step=float(total_bounds["step"]),
        )

        st.markdown("---")

        # ── Services ──────────────────────────────────────────────────────────
        st.markdown('<p class="section-header">📡 Services</p>', unsafe_allow_html=True)
        for col in [
            "PhoneService", "MultipleLines", "InternetService",
            "OnlineSecurity", "OnlineBackup", "DeviceProtection",
            "TechSupport", "StreamingTV", "StreamingMovies",
        ]:
            inputs[col] = st.selectbox(FEATURE_LABELS[col], FEATURE_OPTIONS[col])

        st.markdown("---")

        # ── Run controls ──────────────────────────────────────────────────────
        n_cfs           = st.slider("Number of 'What-if' scenarios", 2, 5, 3)
        predict_clicked = st.button("🔍 Run Prediction")

    return inputs, n_cfs, predict_clicked
