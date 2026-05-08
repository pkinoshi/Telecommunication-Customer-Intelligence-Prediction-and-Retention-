import streamlit as st
from ui.styles import inject_styles

inject_styles()

st.markdown("# About This Project")
st.markdown("---")

# ── Hero summary ──────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-banner" style="padding:36px 40px;text-align:left">
    <div style="display:flex;gap:20px;align-items:flex-start;flex-wrap:wrap">
        <div style="flex:1;min-width:260px">
            <h2 style="color:#f1f5f9;margin:0 0 10px;font-size:1.6rem">
                Customer Churn Intelligence Platform
            </h2>
            <p style="color:#94a3b8;font-size:0.92rem;line-height:1.75;margin:0 0 16px">
                An end-to-end ML application that predicts telecom customer churn,
                explains <em>why</em> a customer is at risk, and recommends the
                <strong style="color:#a78bfa">minimum actionable changes</strong>
                needed to retain them — all without requiring any technical knowledge from the user.
            </p>
            <div>
                <span class="stat-pill">Logistic Regression</span>
                <span class="stat-pill">DiCE Counterfactuals</span>
                <span class="stat-pill">SHAP Explainability</span>
                <span class="stat-pill">Streamlit</span>
            </div>
        </div>
        <div style="display:flex;flex-direction:column;gap:10px;min-width:180px">
            <div style="background:rgba(99,102,241,0.12);border:1px solid rgba(99,102,241,0.3);
                        border-radius:10px;padding:12px 16px;text-align:center">
                <div style="color:#a78bfa;font-size:1.6rem;font-weight:800">7,043</div>
                <div style="color:#64748b;font-size:0.78rem">training customers</div>
            </div>
            <div style="background:rgba(74,222,128,0.08);border:1px solid rgba(74,222,128,0.25);
                        border-radius:10px;padding:12px 16px;text-align:center">
                <div style="color:#4ade80;font-size:1.6rem;font-weight:800">~85 %</div>
                <div style="color:#64748b;font-size:0.78rem">ROC-AUC</div>
            </div>
        </div>
    </div>
</div>""", unsafe_allow_html=True)

st.markdown("---")

# ── Problem & motivation ──────────────────────────────────────────────────────
st.markdown("## Why This Exists")

c1, c2 = st.columns(2)
with c1:
    st.markdown("""
    <div class="metric-card" style="border-top:3px solid #f87171">
    <h4 style="color:#f87171;margin:0 0 10px">The Business Problem</h4>
    <p style="color:#94a3b8;font-size:0.88rem;line-height:1.75;margin:0 0 12px">
    Acquiring a new customer costs <strong style="color:#fca5a5">5–7×</strong>
    more than keeping an existing one. In telecoms — where switching is cheap,
    providers compete aggressively on price, and loyalty programmes are weak —
    churn is one of the highest-leverage metrics a business can move.
    </p>
    <p style="color:#94a3b8;font-size:0.88rem;line-height:1.75;margin:0">
    Most retention teams still operate <em>reactively</em>: they contact
    customers only after a cancellation request is filed, when it is usually
    too late. Proactive, data-driven retention is dramatically more effective.
    </p>
    </div>""", unsafe_allow_html=True)

with c2:
    st.markdown("""
    <div class="metric-card" style="border-top:3px solid #4ade80">
    <h4 style="color:#4ade80;margin:0 0 10px">What This App Does Differently</h4>
    <p style="color:#94a3b8;font-size:0.88rem;line-height:1.75;margin:0 0 12px">
    Most churn tools stop at a probability score. This platform goes two steps further:
    </p>
    <div style="margin-bottom:8px;padding-left:10px;border-left:2px solid #4ade80">
        <div style="color:#cbd5e1;font-size:0.86rem;font-weight:600">1. Explains the score</div>
        <div style="color:#94a3b8;font-size:0.83rem">SHAP values show exactly which features drove the prediction.</div>
    </div>
    <div style="padding-left:10px;border-left:2px solid #6366f1">
        <div style="color:#cbd5e1;font-size:0.86rem;font-weight:600">2. Recommends an action</div>
        <div style="color:#94a3b8;font-size:0.83rem">DiCE counterfactuals name the specific changes that would retain the customer.</div>
    </div>
    </div>""", unsafe_allow_html=True)

st.markdown("""
<div class="highlight-quote">
"The output is never just <em>'this customer will churn'</em> —
it is <em>'this customer will churn <strong>unless</strong> you offer them a one-year contract
and add online security'</em>."
</div>""", unsafe_allow_html=True)

st.markdown("---")

# ── How to use ────────────────────────────────────────────────────────────────
st.markdown("## 🗺️ How to Use the App")

steps = [
    ("1", "#6366f1", "🏠 Start on the Home page",
     "Read the churn driver summary to understand what signals the model responds to most."),
    ("2", "#8b5cf6", "Go to the Predict page",
     "Click '1 Predict' in the sidebar. The customer input form appears on the left."),
    ("3", "#a78bfa", "Fill in the customer profile",
     "All fields use plain dropdowns and sliders — no numeric codes, no encoding required. "
     "Demographics, account details, and service subscriptions are all covered."),
    ("4", "#c4b5fd", "Click Run Prediction",
     "The model scores the profile instantly. You'll see a High/Low risk verdict and an exact "
     "churn probability percentage."),
    ("5", "#e9d5ff", "Review retention scenarios (if High Risk)",
     "DiCE generates 2–5 'what-if' scenarios automatically. Each shows only the features that "
     "need to change, with the original value struck through and the recommended value in colour."),
    ("6", "#a78bfa", "Explore the Methodology page",
     "Understand how the model was built — the pipeline, SMOTE, feature encoding, and "
     "evaluation results — without needing to read the source code."),
]

for num, color, title, desc in steps:
    st.markdown(f"""
    <div style="display:flex;gap:14px;margin-bottom:10px;align-items:flex-start">
        <div style="min-width:34px;height:34px;border-radius:50%;background:{color};
                    display:flex;align-items:center;justify-content:center;
                    font-weight:700;color:#0f1117;font-size:0.85rem;flex-shrink:0">{num}</div>
        <div style="background:linear-gradient(135deg,#1e2130,#252840);border:1px solid #2a2d3e;
                    border-left:3px solid {color};border-radius:0 10px 10px 0;
                    padding:11px 15px;flex:1">
            <div style="color:#e2e8f0;font-weight:600;font-size:0.9rem">{title}</div>
            <div style="color:#94a3b8;font-size:0.84rem;margin-top:4px;line-height:1.6">{desc}</div>
        </div>
    </div>""", unsafe_allow_html=True)

st.markdown("---")

# ── Tech Stack ────────────────────────────────────────────────────────────────
st.markdown("## Tech Stack")

stack = [
    ( "Python 3.11",      "Core language"),
    ("Streamlit",         "Multi-page web app framework"),
    ("scikit-learn",      "Pipeline, preprocessing, Logistic Regression"),
    ("imbalanced-learn",  "SMOTE inside the pipeline"),
    ("DiCE-ml",           "Counterfactual explanation generation"),
    ("SHAP",              "Shapley-value feature attribution"),
    ("XGBoost",           "Evaluated but not selected"),
    ("pandas / NumPy",    "Data wrangling & numeric ops"),
    ("joblib",            "Model serialisation to disk"),
]

cols = st.columns(3)

for i, (name, role) in enumerate(stack):
    with cols[i % 3]:
        st.markdown(f"""
        <div style="background:#1e2130;border:1px solid #2a2d3e;border-radius:10px;
                    padding:12px 14px;margin-bottom:10px;">
            <div style="color:#e2e8f0;font-weight:600;font-size:0.88rem">{name}</div>
            <div style="color:#64748b;font-size:0.77rem;margin-top:2px">{role}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")

# ── Code architecture ─────────────────────────────────────────────────────────
st.markdown("## Code Architecture")

st.markdown("""
<div class="metric-card">
<p style="color:#94a3b8;font-size:0.85rem;margin:0 0 14px">
The app is fully modularised. Each file has one responsibility.
No ML logic in UI files. No UI logic in ML files. No hard-coded constants anywhere except <code>config.py</code>.
</p>
</div>
""", unsafe_allow_html=True)

st.code("""
churn_app/
├── app.py                    ← Home page + page config (must be here only)
├── config.py                 ← Every constant: features, bounds, file paths, DiCE config
├── model.py                  ← ML only: load artifacts, predict, run DiCE. Zero Streamlit imports.
├── requirements.txt
│
├── pages/
│   ├── 1_Predict.py          ← Customer form → prediction → counterfactuals
│   ├── 2_Methodology.py      ← Data science walkthrough (this methodology page)
│   └── 3_About.py            ← This page
│
└── ui/
    ├── __init__.py
    ├── styles.py             ← All CSS in one place. inject_styles() called once per page.
    ├── sidebar.py            ← Form rendering → returns plain inputs dict + controls
    ├── results.py            ← Verdict banner, probability gauge, profile summary expander
    └── counterfactuals.py    ← DiCE scenario cards + no-churn retention tip
""")

st.markdown("---")

# ── FAQ ───────────────────────────────────────────────────────────────────────
st.markdown("## ❓ Frequently Asked Questions")

faqs = [
    ("Why does the prediction sometimes feel wrong?",
     "The model was trained on one month of historical data from a fictional US telecom. It reflects the patterns in that dataset. If a customer profile is unusual or doesn't match the training distribution, the model's confidence may be misplaced. Always treat the score as a guide, not a final verdict."),

    ("Why do the retention scenarios take 15–30 seconds?",
     "DiCE searches a large combinatorial space to find diverse counterfactuals that are close to the original profile, feasible in the real world, and different from each other. This optimisation problem takes time — especially for profiles far from the decision boundary."),

    ("What does the churn probability number actually mean?",
     "It is the model's estimated probability (0–100 %) that this customer will churn, given their profile. A score of 78 % does not mean the customer will definitely leave — it means that among customers with similar profiles in the training data, roughly 78 % churned. It is a statistical signal, not a certainty."),

    ("Why can't DiCE suggest changing the customer's gender or age?",
     "Those features are marked immutable. A business cannot ethically or practically ask a customer to change their demographics. DiCE only suggests changes that a business could realistically offer — contract upgrades, service add-ons, payment method incentives."),

    ("How was the 0.5 churn threshold chosen?",
     "0.5 is the standard default. In practice the optimal threshold depends on the cost of false positives (wasted retention offers) vs false negatives (lost customers). If retaining a customer is worth more than the cost of a false alarm, the threshold should be lowered to capture more at-risk customers."),

    ("Can I retrain the model on my own data?",
     "Yes — the notebook is fully reproducible. Replace the CSV with your own customer data, ensure the column names match config.py, retrain, export the pkl files, and the app will use your model automatically. Update FEATURE_OPTIONS in config.py if your categories differ."),

    ("Why Logistic Regression and not XGBoost?",
     "XGBoost marginally outperforms Logistic Regression on raw accuracy metrics. However, Logistic Regression was selected because: (1) its coefficients are directly interpretable, (2) SHAP's LinearExplainer gives exact (not approximate) Shapley values, and (3) DiCE counterfactuals are more stable and faster on linear models."),

    ("Is the training data balanced?",
     "Not naturally — the dataset has a 26/74 churn split. SMOTE is applied inside the pipeline to create synthetic churn examples during training, balancing the classes to 50/50. The test set is never touched by SMOTE — it retains the original distribution so evaluation metrics reflect real-world performance."),
]

for q, a in faqs:
    with st.expander(f"🔹 {q}"):
        st.markdown(f'<p style="color:#94a3b8;font-size:0.88rem;line-height:1.75;margin:0">{a}</p>',
                    unsafe_allow_html=True)

st.markdown("---")

# ── Limitations ───────────────────────────────────────────────────────────────
st.markdown("## ⚠️ Honest Limitations")

caveats = [
    ("🗂️", "#f59e0b", "Dataset Scope",
     "Trained on one month of fictional US telecom data. May not generalise to different geographies, "
     "time periods, product catalogues, or pricing structures without retraining on local data."),
    ("📉", "#f87171", "Threshold Sensitivity",
     "The default 0.5 threshold treats false positives and false negatives as equally costly. "
     "In most real businesses, the optimal threshold is lower — missing a churner is more expensive "
     "than a wasted retention call."),
    ("🎲", "#a78bfa", "DiCE Runtime & Reliability",
     "Counterfactual generation takes 15–30 seconds and may fail for unusual customer profiles "
     "where DiCE cannot find a valid path to the opposite class within the permitted feature ranges."),
    ("🔄", "#6366f1", "Model Drift",
     "Customer behaviour, pricing, and competitive dynamics change over time. The model should be "
     "retrained on fresh data periodically to maintain predictive accuracy."),
    ("🔢", "#94a3b8", "Encoding Brittleness",
     "Label encodings are derived from the training data. Any new categorical value not seen at "
     "training time (e.g. a new payment method) will cause an error unless the encoder is retrained."),
]

for icon, color, title, body in caveats:
    st.markdown(f"""
    <div style="display:flex;gap:14px;margin-bottom:10px;padding:14px 16px;
                background:#1a1d2e;border:1px solid #2a2d3e;
                border-left:3px solid {color};border-radius:0 10px 10px 0;align-items:flex-start">
        <span style="font-size:1.4rem;flex-shrink:0">{icon}</span>
        <div>
            <div style="color:{color};font-weight:600;font-size:0.88rem;margin-bottom:5px">{title}</div>
            <div style="color:#94a3b8;font-size:0.84rem;line-height:1.65">{body}</div>
        </div>
    </div>""", unsafe_allow_html=True)

st.markdown("---")

# ── Data source ───────────────────────────────────────────────────────────────
st.markdown("## 📚 Data Source")
st.markdown("""
<div class="metric-card">
<div style="display:flex;gap:20px;flex-wrap:wrap">
    <div style="flex:2;min-width:220px">
        <p style="color:#94a3b8;font-size:0.88rem;line-height:1.75;margin:0 0 12px">
        <strong style="color:#cbd5e1">Dataset:</strong> IBM Sample Data Sets — Telco Customer Churn<br>
        <strong style="color:#cbd5e1">Available on:</strong> Kaggle · IBM Developer · GitHub<br>
        <strong style="color:#cbd5e1">License:</strong> Publicly available for educational and non-commercial use.
        </p>
        <p style="color:#94a3b8;font-size:0.88rem;line-height:1.75;margin:0">
        <strong style="color:#cbd5e1">Cleaning applied:</strong>
        <code>customerID</code> dropped · whitespace stripped from strings ·
        <code>TotalCharges</code> coerced to float with 11 NaNs filled by column median ·
        <code>SeniorCitizen</code> remapped 0/1 → No/Yes.
        </p>
    </div>
    <div style="flex:1;min-width:160px;background:#13111c;border-radius:8px;padding:14px;
                display:flex;flex-direction:column;gap:8px;justify-content:center">
        <span class="tag">IBM Telco Dataset</span>
        <span class="tag">7,043 rows</span>
        <span class="tag">21 original columns</span>
        <span class="tag">19 after cleaning</span>
        <span class="tag">Binary classification</span>
    </div>
</div>
</div>""", unsafe_allow_html=True)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown(
    '<p style="color:#475569;text-align:center;font-size:0.8rem">'
    "Churn Intelligence Dashboard · Powered by Logistic Regression + DiCE Counterfactuals"
    "</p>",
    unsafe_allow_html=True,
)
