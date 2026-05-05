import streamlit as st
import pandas as pd
import numpy as np
import joblib
import dice_ml
from dice_ml import Dice
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import warnings
from helpers import churn_model_pipeline.pkl, df_cleaned_raw.csv, target_encoder.pkl
warnings.filterwarnings("ignore")

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Customer Churn Predictor",
    page_icon="📡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Sidebar Navigation Info ─────────────────────────────
st.sidebar.markdown("## 📡 Navigation")
st.sidebar.info("""
- 📡 Dashboard
- 📘 About
- ⚙️ Methodology
""")

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    /* Main background */
    .stApp { background-color: #0f1117; }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1d2e 0%, #12141f 100%);
        border-right: 1px solid #2a2d3e;
    }
    [data-testid="stSidebar"] .stMarkdown h2,
    [data-testid="stSidebar"] .stMarkdown h3 {
        color: #a78bfa;
    }

    /* Cards */
    .metric-card {
        background: linear-gradient(135deg, #1e2130 0%, #252840 100%);
        border: 1px solid #2a2d3e;
        border-radius: 12px;
        padding: 20px 24px;
        margin-bottom: 16px;
    }
    .churn-card {
        background: linear-gradient(135deg, #2d1515 0%, #3d1a1a 100%);
        border: 1px solid #6b2020;
        border-radius: 12px;
        padding: 24px;
        text-align: center;
    }
    .safe-card {
        background: linear-gradient(135deg, #0d2d1a 0%, #123520 100%);
        border: 1px solid #1a6b35;
        border-radius: 12px;
        padding: 24px;
        text-align: center;
    }
    .cf-card {
        background: linear-gradient(135deg, #1a1d2e 0%, #1e2240 100%);
        border: 1px solid #3b4fd4;
        border-left: 4px solid #6366f1;
        border-radius: 12px;
        padding: 20px 24px;
        margin-bottom: 12px;
    }
    .section-header {
        color: #a78bfa;
        font-size: 1.1rem;
        font-weight: 600;
        letter-spacing: 0.05em;
        text-transform: uppercase;
        margin-bottom: 12px;
        border-bottom: 1px solid #2a2d3e;
        padding-bottom: 8px;
    }
    .change-badge-pos {
        background: #1a3d26;
        border: 1px solid #2d7a4a;
        color: #4ade80;
        border-radius: 20px;
        padding: 2px 10px;
        font-size: 0.82rem;
        font-weight: 500;
        display: inline-block;
        margin: 2px;
    }
    .change-badge-neg {
        background: #3d1a1a;
        border: 1px solid #7a2d2d;
        color: #f87171;
        border-radius: 20px;
        padding: 2px 10px;
        font-size: 0.82rem;
        font-weight: 500;
        display: inline-block;
        margin: 2px;
    }
    .change-badge-neutral {
        background: #1e2130;
        border: 1px solid #3a3d50;
        color: #94a3b8;
        border-radius: 20px;
        padding: 2px 10px;
        font-size: 0.82rem;
        font-weight: 500;
        display: inline-block;
        margin: 2px;
    }
    .probability-bar-container {
        background: #1e2130;
        border-radius: 8px;
        height: 12px;
        margin: 10px 0;
        overflow: hidden;
    }
    .stButton > button {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 12px 32px;
        font-weight: 600;
        font-size: 1rem;
        width: 100%;
        transition: opacity 0.2s;
    }
    .stButton > button:hover { opacity: 0.88; }
    div[data-testid="stSelectbox"] label,
    div[data-testid="stNumberInput"] label,
    div[data-testid="stSlider"] label {
        color: #cbd5e1 !important;
        font-size: 0.88rem;
    }
    .stTabs [data-baseweb="tab"] {
        color: #94a3b8;
        font-weight: 500;
    }
    .stTabs [aria-selected="true"] {
        color: #a78bfa !important;
    }
</style>
""", unsafe_allow_html=True)


# ── Load artifacts ────────────────────────────────────────────────────────────
@st.cache_resource
def load_artifacts():
    pipeline    = joblib.load("churn_model_pipeline.pkl")
    tgt_encoder = joblib.load("target_encoder.pkl")
    df_raw      = pd.read_csv("df_cleaned_raw.csv")
    return pipeline, tgt_encoder, df_raw

try:
    model_pipeline, target_encoder, df_raw = load_artifacts()
    artifacts_loaded = True
except Exception as e:
    artifacts_loaded = False
    load_error = str(e)


# ── Feature definitions ───────────────────────────────────────────────────────
BINARY_YES_NO     = ["No", "Yes"]
YES_NO_NOPHONE    = ["No", "No phone service", "Yes"]
YES_NO_NOINTERNET = ["No", "No internet service", "Yes"]

FEATURE_OPTIONS = {
    "gender":           ["Female", "Male"],
    "SeniorCitizen":    ["No", "Yes"],
    "Partner":          ["No", "Yes"],
    "Dependents":       ["No", "Yes"],
    "PhoneService":     BINARY_YES_NO,
    "MultipleLines":    YES_NO_NOPHONE,
    "InternetService":  ["DSL", "Fiber optic", "No"],
    "OnlineSecurity":   YES_NO_NOINTERNET,
    "OnlineBackup":     YES_NO_NOINTERNET,
    "DeviceProtection": YES_NO_NOINTERNET,
    "TechSupport":      YES_NO_NOINTERNET,
    "StreamingTV":      YES_NO_NOINTERNET,
    "StreamingMovies":  YES_NO_NOINTERNET,
    "Contract":         ["Month-to-month", "One year", "Two year"],
    "PaperlessBilling": BINARY_YES_NO,
    "PaymentMethod":    [
        "Bank transfer (automatic)",
        "Credit card (automatic)",
        "Electronic check",
        "Mailed check"
    ],
}

FEATURE_LABELS = {
    "gender":           "Gender",
    "SeniorCitizen":    "Senior Citizen",
    "Partner":          "Has Partner",
    "Dependents":       "Has Dependents",
    "PhoneService":     "Phone Service",
    "MultipleLines":    "Multiple Lines",
    "InternetService":  "Internet Service",
    "OnlineSecurity":   "Online Security",
    "OnlineBackup":     "Online Backup",
    "DeviceProtection": "Device Protection",
    "TechSupport":      "Tech Support",
    "StreamingTV":      "Streaming TV",
    "StreamingMovies":  "Streaming Movies",
    "Contract":         "Contract Type",
    "PaperlessBilling": "Paperless Billing",
    "PaymentMethod":    "Payment Method",
    "tenure":           "Tenure (months)",
    "MonthlyCharges":   "Monthly Charges ($)",
    "TotalCharges":     "Total Charges ($)",
}

FEATURES_TO_VARY = [
    "PhoneService", "MultipleLines", "InternetService", "OnlineSecurity",
    "OnlineBackup", "DeviceProtection", "TechSupport", "StreamingTV",
    "StreamingMovies", "Contract", "PaperlessBilling", "PaymentMethod",
    "MonthlyCharges"
]

IMMUTABLE = ["gender", "SeniorCitizen", "Partner", "Dependents"]

COLUMN_ORDER = [
    "gender", "SeniorCitizen", "Partner", "Dependents", "PhoneService",
    "MultipleLines", "InternetService", "OnlineSecurity", "OnlineBackup",
    "DeviceProtection", "TechSupport", "StreamingTV", "StreamingMovies",
    "Contract", "PaperlessBilling", "PaymentMethod", "tenure",
    "MonthlyCharges", "TotalCharges"
]


# ── Helpers ───────────────────────────────────────────────────────────────────
def build_input_df(inputs: dict) -> pd.DataFrame:
    return pd.DataFrame([inputs])[COLUMN_ORDER]


def predict(df: pd.DataFrame):
    prob  = model_pipeline.predict_proba(df)[0][1]   # probability of churn (class 1)
    label = model_pipeline.predict(df)[0]             # 0 or 1
    return prob, label


def run_dice(query_df: pd.DataFrame, n_cfs: int = 3):
    continuous_features = ["tenure", "MonthlyCharges", "TotalCharges"]
    dice_data = dice_ml.Data(
        dataframe=df_raw,
        continuous_features=continuous_features,
        outcome_name="Churn",
        immutable_features=IMMUTABLE
    )
    dice_model = dice_ml.Model(model=model_pipeline, backend="sklearn")
    exp = Dice(dice_data, dice_model)
    result = exp.generate_counterfactuals(
        query_df,
        total_CFs=n_cfs,
        desired_class="opposite",
        features_to_vary=FEATURES_TO_VARY,
        permitted_range={"MonthlyCharges": [18, 120]},
    )
    return result


def diff_badge(original, cf_val, col):
    if str(original) == str(cf_val):
        return f'<span class="change-badge-neutral">unchanged: {cf_val}</span>'
    if col in ["MonthlyCharges", "tenure", "TotalCharges"]:
        try:
            direction = "↓" if float(cf_val) < float(original) else "↑"
            css = "change-badge-pos" if direction == "↓" else "change-badge-neg"
            return f'<span class="{css}">{direction} {cf_val}</span>'
        except Exception:
            pass
    return f'<span class="change-badge-pos">→ {cf_val}</span>'


# ── Sidebar – customer input form ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 📋 Customer Details")
    st.markdown("---")

    # Demographics
    st.markdown('<p class="section-header">👤 Demographics</p>', unsafe_allow_html=True)
    gender         = st.selectbox(FEATURE_LABELS["gender"],         FEATURE_OPTIONS["gender"])
    senior         = st.selectbox(FEATURE_LABELS["SeniorCitizen"],  FEATURE_OPTIONS["SeniorCitizen"])
    partner        = st.selectbox(FEATURE_LABELS["Partner"],         FEATURE_OPTIONS["Partner"])
    dependents     = st.selectbox(FEATURE_LABELS["Dependents"],      FEATURE_OPTIONS["Dependents"])

    st.markdown("---")

    # Account
    st.markdown('<p class="section-header">📄 Account Info</p>', unsafe_allow_html=True)
    tenure         = st.slider(FEATURE_LABELS["tenure"], 0, 72, 12)
    contract       = st.selectbox(FEATURE_LABELS["Contract"],        FEATURE_OPTIONS["Contract"])
    paperless      = st.selectbox(FEATURE_LABELS["PaperlessBilling"],FEATURE_OPTIONS["PaperlessBilling"])
    payment        = st.selectbox(FEATURE_LABELS["PaymentMethod"],   FEATURE_OPTIONS["PaymentMethod"])
    monthly        = st.number_input(FEATURE_LABELS["MonthlyCharges"],  min_value=18.0, max_value=120.0, value=65.0, step=0.5)
    total          = st.number_input(FEATURE_LABELS["TotalCharges"],    min_value=0.0,  max_value=9000.0, value=float(round(tenure * monthly, 2)), step=1.0)

    st.markdown("---")

    # Services
    st.markdown('<p class="section-header">📡 Services</p>', unsafe_allow_html=True)
    phone          = st.selectbox(FEATURE_LABELS["PhoneService"],    FEATURE_OPTIONS["PhoneService"])
    multi_lines    = st.selectbox(FEATURE_LABELS["MultipleLines"],   FEATURE_OPTIONS["MultipleLines"])
    internet       = st.selectbox(FEATURE_LABELS["InternetService"], FEATURE_OPTIONS["InternetService"])
    online_sec     = st.selectbox(FEATURE_LABELS["OnlineSecurity"],  FEATURE_OPTIONS["OnlineSecurity"])
    online_bak     = st.selectbox(FEATURE_LABELS["OnlineBackup"],    FEATURE_OPTIONS["OnlineBackup"])
    device_prot    = st.selectbox(FEATURE_LABELS["DeviceProtection"],FEATURE_OPTIONS["DeviceProtection"])
    tech_sup       = st.selectbox(FEATURE_LABELS["TechSupport"],     FEATURE_OPTIONS["TechSupport"])
    stream_tv      = st.selectbox(FEATURE_LABELS["StreamingTV"],     FEATURE_OPTIONS["StreamingTV"])
    stream_movies  = st.selectbox(FEATURE_LABELS["StreamingMovies"], FEATURE_OPTIONS["StreamingMovies"])

    st.markdown("---")

    n_cfs = st.slider("Number of 'What-if' scenarios", 2, 5, 3)
    predict_btn = st.button("🔍 Run Prediction")


# ── Main area ─────────────────────────────────────────────────────────────────
st.markdown("# 📡 Telecoms Customer Churn Intelligence")
st.markdown("*Enter customer details in the sidebar, then click **Run Prediction**.*")
st.markdown("---")

if not artifacts_loaded:
    st.error(f"""
    **Could not load model files.** Make sure these files are in the same folder as `app.py`:
    - `churn_model_pipeline.pkl`
    - `target_encoder.pkl`
    - `df_cleaned_raw.csv`

    Error: `{load_error}`
    """)
    st.stop()

if not predict_btn:
    # Landing state
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""<div class="metric-card">
            <h3 style="color:#a78bfa;margin:0">Step 1</h3>
            <p style="color:#94a3b8;margin:8px 0 0">Fill in customer details in the sidebar</p>
        </div>""", unsafe_allow_html=True)
    with col2:
        st.markdown("""<div class="metric-card">
            <h3 style="color:#a78bfa;margin:0">Step 2</h3>
            <p style="color:#94a3b8;margin:8px 0 0">Click <strong>Run Prediction</strong></p>
        </div>""", unsafe_allow_html=True)
    with col3:
        st.markdown("""<div class="metric-card">
            <h3 style="color:#a78bfa;margin:0">Step 3</h3>
            <p style="color:#94a3b8;margin:8px 0 0">If churn risk is high, explore retention scenarios</p>
        </div>""", unsafe_allow_html=True)
    st.stop()


# ── Build input & predict ─────────────────────────────────────────────────────
inputs = {
    "gender":           gender,
    "SeniorCitizen":    senior,
    "Partner":          partner,
    "Dependents":       dependents,
    "PhoneService":     phone,
    "MultipleLines":    multi_lines,
    "InternetService":  internet,
    "OnlineSecurity":   online_sec,
    "OnlineBackup":     online_bak,
    "DeviceProtection": device_prot,
    "TechSupport":      tech_sup,
    "StreamingTV":      stream_tv,
    "StreamingMovies":  stream_movies,
    "Contract":         contract,
    "PaperlessBilling": paperless,
    "PaymentMethod":    payment,
    "tenure":           tenure,
    "MonthlyCharges":   monthly,
    "TotalCharges":     total,
}

query_df = build_input_df(inputs)

with st.spinner("Running prediction..."):
    churn_prob, churn_label = predict(query_df)

will_churn = churn_label == 1

# ── Result banner ─────────────────────────────────────────────────────────────
col_result, col_gauge = st.columns([2, 1])

with col_result:
    if will_churn:
        st.markdown(f"""
        <div class="churn-card">
            <div style="font-size:3rem">⚠️</div>
            <h2 style="color:#f87171;margin:8px 0">High Churn Risk</h2>
            <p style="color:#fca5a5;font-size:1.1rem;margin:0">
                This customer is likely to leave
            </p>
        </div>""", unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="safe-card">
            <div style="font-size:3rem">✅</div>
            <h2 style="color:#4ade80;margin:8px 0">Low Churn Risk</h2>
            <p style="color:#86efac;font-size:1.1rem;margin:0">
                This customer is likely to stay
            </p>
        </div>""", unsafe_allow_html=True)

with col_gauge:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.markdown(f"**Churn Probability**")
    pct = int(churn_prob * 100)
    bar_color = "#ef4444" if pct >= 50 else "#22c55e"
    st.markdown(f"""
    <div style="font-size:2.5rem;font-weight:700;color:{bar_color};text-align:center">{pct}%</div>
    <div class="probability-bar-container">
        <div style="width:{pct}%;height:100%;background:{bar_color};border-radius:8px;transition:width 0.5s"></div>
    </div>
    <p style="color:#94a3b8;font-size:0.82rem;text-align:center;margin:4px 0">
        {'Above 50% = predicted churn' if pct >= 50 else 'Below 50% = predicted to stay'}
    </p>""", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")

# ── Customer summary ──────────────────────────────────────────────────────────
with st.expander("📋 Customer Profile Summary", expanded=False):
    c1, c2, c3 = st.columns(3)
    demo_items    = ["gender","SeniorCitizen","Partner","Dependents"]
    account_items = ["tenure","Contract","PaperlessBilling","PaymentMethod","MonthlyCharges","TotalCharges"]
    service_items = ["PhoneService","MultipleLines","InternetService","OnlineSecurity",
                     "OnlineBackup","DeviceProtection","TechSupport","StreamingTV","StreamingMovies"]

    with c1:
        st.markdown("**Demographics**")
        for k in demo_items:
            st.markdown(f"- **{FEATURE_LABELS[k]}:** {inputs[k]}")
    with c2:
        st.markdown("**Account**")
        for k in account_items:
            st.markdown(f"- **{FEATURE_LABELS[k]}:** {inputs[k]}")
    with c3:
        st.markdown("**Services**")
        for k in service_items:
            st.markdown(f"- **{FEATURE_LABELS[k]}:** {inputs[k]}")


# ── Counterfactual section (only if churn predicted) ─────────────────────────
if will_churn:
    st.markdown("## 💡 Retention Scenarios: What Would Keep This Customer?")
    st.markdown(
        "The model found these changes to the customer's profile that would flip the prediction to **Stay**. "
        "Unchanged fields are greyed out. Green = favourable change, Red = increase in charges."
    )

    with st.spinner(f"Generating {n_cfs} retention scenarios... (this may take 15–30 seconds)"):
        try:
            dice_result = run_dice(query_df, n_cfs=n_cfs)
            cf_df = dice_result.cf_examples_list[0].final_cfs_df

            if cf_df is None or cf_df.empty:
                st.warning("DiCE could not find valid counterfactuals. Try adjusting the customer profile.")
            else:
                # Drop Churn column if present
                cf_df = cf_df.drop(columns=["Churn"], errors="ignore")

                for scenario_idx, (_, cf_row) in enumerate(cf_df.iterrows(), 1):
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
                        unsafe_allow_html=True
                    )

                    # Show only the changed features prominently
                    if changed_cols:
                        cols = st.columns(min(len(changed_cols), 3))
                        for idx, col in enumerate(changed_cols):
                            with cols[idx % 3]:
                                original_val = inputs.get(col, "—")
                                new_val      = cf_row.get(col, "—")
                                if isinstance(new_val, float):
                                    new_val = round(new_val, 2)

                                # Determine arrow color
                                if col == "MonthlyCharges":
                                    arrow = "↓" if float(new_val) < float(original_val) else "↑"
                                    arrow_color = "#4ade80" if arrow == "↓" else "#f87171"
                                else:
                                    arrow = "→"
                                    arrow_color = "#a78bfa"

                                st.markdown(f"""
                                <div class="cf-card">
                                    <div style="color:#94a3b8;font-size:0.78rem;text-transform:uppercase;letter-spacing:0.05em">
                                        {FEATURE_LABELS.get(col, col)}
                                    </div>
                                    <div style="color:#cbd5e1;font-size:0.9rem;margin:6px 0 2px;text-decoration:line-through">
                                        {original_val}
                                    </div>
                                    <div style="font-size:1.4rem;color:{arrow_color};font-weight:700">
                                        {arrow} {new_val}
                                    </div>
                                </div>""", unsafe_allow_html=True)
                    st.markdown("---")

        except Exception as e:
            st.error(f"DiCE encountered an error: {e}")
            st.info("Tip: Make sure `df_cleaned_raw.csv` matches the training data used to build the pipeline.")

else:
    # Not churning – show positive reinforcement
    st.markdown("## ✅ Retention Actions")
    st.markdown("""
    <div class="metric-card">
        <p style="color:#86efac;font-size:1rem;margin:0">
            This customer is <strong>not predicted to churn</strong>. No immediate intervention needed.<br><br>
            💡 <strong>Tip:</strong> Continue monitoring if their contract is month-to-month or their 
            monthly charges are high — those are the strongest churn signals in this model.
        </p>
    </div>""", unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown(
    '<p style="color:#475569;text-align:center;font-size:0.8rem">'
    'Churn Intelligence Dashboard · Powered by Logistic Regression + DiCE Counterfactuals'
    '</p>',
    unsafe_allow_html=True
)
