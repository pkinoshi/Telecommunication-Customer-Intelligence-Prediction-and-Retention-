"""
pages/2_Methodology.py
----------------------
End-to-end data science methodology:
dataset overview, feature reference, visual pipeline, class imbalance,
model selection rationale, explainability tools, and evaluation results.
"""

import streamlit as st
from ui.styles import inject_styles

inject_styles()

st.markdown("# 🔬 Methodology")
st.markdown("*How the churn model was built.....  from raw data to actionable predictions.*")
st.markdown("---")

# ── 1. Dataset ────────────────────────────────────────────────────────────────
st.markdown("## 1 · Dataset")

col_desc, col_stats = st.columns([3, 2])
with col_desc:
    st.markdown("""
    <div class="metric-card">
    <p style="color:#cbd5e1;line-height:1.75;margin:0 0 12px">
    The model was trained on the
    <strong style="color:#a78bfa">IBM Telco Customer Churn</strong> dataset —
    a widely-used benchmark capturing one month of activity for a fictional
    US telecom provider, recording which customers cancelled at month-end.
    </p>
    <p style="color:#94a3b8;font-size:0.88rem;line-height:1.7;margin:0">
    Each row represents one customer. The target variable <code>Churn</code>
    is binary: <strong>Yes</strong> (left) or <strong>No</strong> (stayed).
    The dataset is moderately imbalanced — roughly <strong style="color:#f87171">26 % churn</strong>
    vs 74 % no-churn — which is addressed explicitly by SMOTE inside the pipeline.
    </p>
    </div>""", unsafe_allow_html=True)

with col_stats:
    st.markdown("""
    <div class="metric-card">
    <p style="color:#94a3b8;font-size:0.78rem;text-transform:uppercase;
              letter-spacing:0.07em;margin:0 0 12px;font-weight:600">Dataset at a glance</p>
    <table style="width:100%;color:#cbd5e1;font-size:0.88rem;border-collapse:collapse">
        <tr><td style="padding:7px 0;color:#94a3b8;border-bottom:1px solid #2a2d3e">Rows</td>
            <td style="padding:7px 0;text-align:right;color:#a78bfa;font-weight:700;border-bottom:1px solid #2a2d3e">7,043</td></tr>
        <tr><td style="padding:7px 0;color:#94a3b8;border-bottom:1px solid #2a2d3e">Features used</td>
            <td style="padding:7px 0;text-align:right;color:#a78bfa;font-weight:700;border-bottom:1px solid #2a2d3e">19</td></tr>
        <tr><td style="padding:7px 0;color:#94a3b8;border-bottom:1px solid #2a2d3e">Categorical</td>
            <td style="padding:7px 0;text-align:right;color:#a78bfa;font-weight:700;border-bottom:1px solid #2a2d3e">16</td></tr>
        <tr><td style="padding:7px 0;color:#94a3b8;border-bottom:1px solid #2a2d3e">Numeric</td>
            <td style="padding:7px 0;text-align:right;color:#a78bfa;font-weight:700;border-bottom:1px solid #2a2d3e">3</td></tr>
        <tr><td style="padding:7px 0;color:#94a3b8;border-bottom:1px solid #2a2d3e">Churn rate</td>
            <td style="padding:7px 0;text-align:right;color:#f87171;font-weight:700;border-bottom:1px solid #2a2d3e">26.5 %</td></tr>
        <tr><td style="padding:7px 0;color:#94a3b8">Missing values</td>
            <td style="padding:7px 0;text-align:right;color:#4ade80;font-weight:700">11 → imputed</td></tr>
    </table>
    </div>""", unsafe_allow_html=True)

st.markdown("---")

# ── 2. Features ───────────────────────────────────────────────────────────────
st.markdown("## 2 · Feature Reference")

tabs = st.tabs(["👤 Demographics", "📄 Account", "📡 Services", "🔢 Numeric"])

with tabs[0]:
    st.markdown("""
    <div class="metric-card" style="margin-top:12px">
    <p style="color:#94a3b8;font-size:0.85rem;margin:0">
    These four features describe <em>who</em> the customer is.
    They are marked <strong style="color:#f87171">immutable</strong> in the
    counterfactual engine — the model never recommends changing them because
    no business can ethically or practically ask a customer to change their demographics.
    </p>
    </div>""", unsafe_allow_html=True)
    rows = [
        ("gender", "Female / Male", "🔒 Immutable", "#f87171",
         "Biological sex. No significant difference in churn rate in this dataset."),
        ("SeniorCitizen", "No / Yes", "🔒 Immutable", "#f87171",
         "Age 65 or older. Senior customers show a slightly higher churn rate, possibly due to digital service friction."),
        ("Partner", "No / Yes", "🔒 Immutable", "#f87171",
         "Whether the customer has a partner. Customers with partners churn slightly less."),
        ("Dependents", "No / Yes", "🔒 Immutable", "#f87171",
         "Whether the customer supports dependants. Customers with dependants are more stable."),
    ]
    for feat, vals, badge, badge_col, desc in rows:
        st.markdown(
            f'<div style="padding:12px 0;border-bottom:1px solid #2a2d3e;display:flex;gap:12px;align-items:flex-start">'
            f'<div style="min-width:160px">'
            f'<span style="color:#a78bfa;font-weight:600;font-family:monospace;font-size:0.9rem">{feat}</span><br>'
            f'<span style="color:#475569;font-size:0.75rem">{vals}</span><br>'
            f'<span style="color:{badge_col};font-size:0.72rem;font-weight:600">{badge}</span>'
            f'</div>'
            f'<div style="color:#94a3b8;font-size:0.86rem;line-height:1.6;padding-top:2px">{desc}</div>'
            f'</div>',
            unsafe_allow_html=True,
        )

with tabs[1]:
    st.markdown("""
    <div class="metric-card" style="margin-top:12px">
    <p style="color:#94a3b8;font-size:0.85rem;margin:0">
    Account features capture the customer's commercial relationship.
    <strong style="color:#4ade80">Contract type</strong> and
    <strong style="color:#4ade80">tenure</strong> are the two strongest
    single predictors of churn in this dataset. These are
    <strong style="color:#4ade80">actionable</strong> — DiCE is allowed to
    suggest changes to them.
    </p>
    </div>""", unsafe_allow_html=True)
    rows = [
        ("tenure", "0–72 months", "✅ Actionable", "#4ade80",
         "Months with the company. Strong negative correlation with churn — the longer a customer stays, the less likely they are to leave."),
        ("Contract", "Month-to-month / One year / Two year", "✅ Actionable", "#4ade80",
         "Month-to-month customers churn at 3× the rate of two-year customers. Upgrading the contract is the single most impactful retention lever."),
        ("PaperlessBilling", "No / Yes", "✅ Actionable", "#4ade80",
         "Paperless billing customers churn slightly more — possibly correlated with being digitally-native and more willing to switch."),
        ("PaymentMethod", "4 options", "✅ Actionable", "#4ade80",
         "Electronic check payers churn at the highest rate. Automatic payment methods (bank transfer, credit card) are associated with lower churn — more inertia."),
        ("MonthlyCharges", "$18–$120", "✅ Actionable", "#4ade80",
         "Strong churn signal at higher values, especially combined with month-to-month contracts."),
        ("TotalCharges", "$0–$8,684", "📌 Derived", "#f59e0b",
         "Closely correlated with tenure × MonthlyCharges. Provides a signal for lifetime value."),
    ]
    for feat, vals, badge, badge_col, desc in rows:
        st.markdown(
            f'<div style="padding:12px 0;border-bottom:1px solid #2a2d3e;display:flex;gap:12px;align-items:flex-start">'
            f'<div style="min-width:180px">'
            f'<span style="color:#a78bfa;font-weight:600;font-family:monospace;font-size:0.9rem">{feat}</span><br>'
            f'<span style="color:#475569;font-size:0.75rem">{vals}</span><br>'
            f'<span style="color:{badge_col};font-size:0.72rem;font-weight:600">{badge}</span>'
            f'</div>'
            f'<div style="color:#94a3b8;font-size:0.86rem;line-height:1.6;padding-top:2px">{desc}</div>'
            f'</div>',
            unsafe_allow_html=True,
        )

with tabs[2]:
    st.markdown("""
    <div class="metric-card" style="margin-top:12px">
    <p style="color:#94a3b8;font-size:0.85rem;margin:0">
    Service add-on flags. Many use three values: <code>No</code>, <code>Yes</code>,
    and <code>No internet/phone service</code> for customers not subscribed to the
    base tier. These are the primary <strong style="color:#4ade80">retention levers</strong>
    the counterfactual engine proposes — upselling or cross-selling to deepen the relationship.
    </p>
    </div>""", unsafe_allow_html=True)
    rows = [
        ("PhoneService", "No / Yes", "Customers without a phone line are a small minority."),
        ("MultipleLines", "No / No phone service / Yes", "Customers with multiple lines are slightly less likely to churn."),
        ("InternetService", "DSL / Fiber optic / No", "⚠️ Fiber optic customers show the highest churn of any service type."),
        ("OnlineSecurity", "No / No internet service / Yes", "Customers with security add-ons are significantly less likely to churn."),
        ("OnlineBackup", "No / No internet service / Yes", "Value-added services generally correlate with lower churn across the board."),
        ("DeviceProtection", "No / No internet service / Yes", "Hardware insurance — moderate churn reduction effect."),
        ("TechSupport", "No / No internet service / Yes", "Strong negative churn signal — customers who use support feel more supported."),
        ("StreamingTV", "No / No internet service / Yes", "Streaming customers churn at a similar rate to non-streamers."),
        ("StreamingMovies", "No / No internet service / Yes", "Similar pattern to StreamingTV — engagement not strongly correlated."),
    ]
    for feat, vals, desc in rows:
        st.markdown(
            f'<div style="padding:12px 0;border-bottom:1px solid #2a2d3e;display:flex;gap:12px;align-items:flex-start">'
            f'<div style="min-width:190px">'
            f'<span style="color:#a78bfa;font-weight:600;font-family:monospace;font-size:0.9rem">{feat}</span><br>'
            f'<span style="color:#475569;font-size:0.75rem">{vals}</span>'
            f'</div>'
            f'<div style="color:#94a3b8;font-size:0.86rem;line-height:1.6;padding-top:2px">{desc}</div>'
            f'</div>',
            unsafe_allow_html=True,
        )

with tabs[3]:
    st.markdown("""
    <div class="metric-card" style="margin-top:12px">
    <p style="color:#94a3b8;font-size:0.85rem;margin:0">
    The three continuous columns are scaled with <code>StandardScaler</code>
    inside the <code>ColumnTransformer</code>. This ensures their magnitudes don't
    dominate logistic regression coefficients, and makes SHAP values comparable across features.
    </p>
    </div>""", unsafe_allow_html=True)
    for feat, rng, desc in [
        ("tenure", "0 – 72", "Months since first activation. Highly predictive — the churn hazard drops sharply after ~24 months."),
        ("MonthlyCharges", "$18 – $120", "Billed monthly for all active services. Strongly correlated with Internet type (Fiber → higher bills → higher churn)."),
        ("TotalCharges", "$0 – $8,684", "Running lifetime total. 11 rows had blank values (new activations with $0 charges) — these were imputed with the column median before training."),
    ]:
        st.markdown(
            f'<div style="padding:12px 0;border-bottom:1px solid #2a2d3e;display:flex;gap:12px;align-items:flex-start">'
            f'<div style="min-width:160px">'
            f'<span style="color:#a78bfa;font-weight:600;font-family:monospace;font-size:0.9rem">{feat}</span><br>'
            f'<span style="color:#475569;font-size:0.75rem">{rng}</span>'
            f'</div>'
            f'<div style="color:#94a3b8;font-size:0.86rem;line-height:1.6;padding-top:2px">{desc}</div>'
            f'</div>',
            unsafe_allow_html=True,
        )

st.markdown("---")

# ── 3. Visual pipeline ────────────────────────────────────────────────────────
st.markdown("## 3 · The ML Pipeline")
st.markdown('<p style="color:#94a3b8;margin-bottom:20px">Everything runs inside a single <code>imblearn.Pipeline</code> — no data leakage is possible because the pipeline\'s <code>.fit()</code> applies each step sequentially only to training data.</p>', unsafe_allow_html=True)

# Visual pipeline diagram
node_colors = ["#6366f1", "#8b5cf6", "#a78bfa", "#c4b5fd", "#e9d5ff"]
nodes = [
    ("📥", "Raw Data", "7,043 rows\n19 features + target"),
    ("🗂️", "Label Encoding", "Categorical → integers\nvia stored mappings"),
    ("⚖️", "SMOTE", "Minority class\noversampled to 50/50"),
    ("📏", "StandardScaler", "Numerics → mean=0\nstd=1"),
    ("🤖", "Logistic Regression", "max_iter=1000\nrandom_state=42"),
]

n_cols = len(nodes) * 2 - 1
cols = st.columns(n_cols)
for i, (icon, title, sub) in enumerate(nodes):
    col_idx = i * 2
    color = node_colors[i]
    with cols[col_idx]:
        st.markdown(f"""
        <div style="background:linear-gradient(135deg,#1e2130,#252840);
                    border:1px solid #2a2d3e;border-top:3px solid {color};
                    border-radius:10px;padding:14px 10px;text-align:center;min-height:110px;
                    display:flex;flex-direction:column;align-items:center;justify-content:center">
            <div style="font-size:1.6rem;margin-bottom:6px">{icon}</div>
            <div style="color:{color};font-weight:700;font-size:0.82rem;margin-bottom:4px">{title}</div>
            <div style="color:#64748b;font-size:0.72rem;line-height:1.4;white-space:pre-line">{sub}</div>
        </div>""", unsafe_allow_html=True)
    if i < len(nodes) - 1:
        with cols[col_idx + 1]:
            st.markdown(
                '<div style="display:flex;align-items:center;justify-content:center;'
                'height:110px;color:#475569;font-size:1.6rem;margin-top:4px">→</div>',
                unsafe_allow_html=True,
            )

st.markdown("")

# Expandable detail per step
with st.expander("📖 Detailed step explanations"):
    steps = [
        ("📥", "#6366f1", "1 · Raw Data",
         "The dataset is loaded and cleaned: <code>customerID</code> is dropped, whitespace is stripped "
         "from all string columns, <code>TotalCharges</code> is coerced to float (11 blank entries become NaN "
         "and are filled with the column median), and <code>SeniorCitizen</code> is remapped from 0/1 to "
         "No/Yes for consistency."),
        ("🗂️", "#8b5cf6", "2 · Label Encoding",
         "A <code>mappings</code> dictionary is built by fitting <code>LabelEncoder</code> on each categorical "
         "column of the <em>full</em> dataset (before splitting). At inference, the app applies the same "
         "stored mappings to the user's input, ensuring identical integer encodings at train and predict time."),
        ("⚖️", "#a78bfa", "3 · SMOTE",
         "<strong>Synthetic Minority Oversampling Technique</strong> generates artificial churner examples "
         "by interpolating between existing churn cases in feature space. Applied <em>inside</em> the pipeline "
         "so it only ever sees training data — never validation or test rows. After resampling, the training "
         "distribution is 50/50 churn vs no-churn."),
        ("📏", "#c4b5fd", "4 · StandardScaler",
         "Scales numeric features to mean=0, variance=1 using statistics computed <em>only</em> on training "
         "data. The fitted scaler is then reused at inference so the app transforms new inputs consistently. "
         "This step makes logistic regression coefficients directly comparable across features."),
        ("🤖", "#e9d5ff", "5 · Logistic Regression",
         "The final estimator. <code>max_iter=1000</code> ensures convergence. Chosen over tree-based models "
         "for three reasons: (1) coefficients are directly interpretable as log-odds, (2) SHAP's "
         "<code>LinearExplainer</code> produces exact (not approximate) Shapley values, and (3) DiCE's "
         "gradient-based counterfactual search requires a differentiable model."),
    ]
    for icon, color, title, body in steps:
        st.markdown(f"""
        <div style="display:flex;gap:14px;margin-bottom:14px;align-items:flex-start">
            <div style="min-width:36px;height:36px;border-radius:50%;background:{color};
                        display:flex;align-items:center;justify-content:center;
                        font-size:1rem;flex-shrink:0">{icon}</div>
            <div style="background:linear-gradient(135deg,#1e2130,#252840);border:1px solid #2a2d3e;
                        border-left:3px solid {color};border-radius:0 10px 10px 0;padding:12px 16px;flex:1">
                <div style="color:#e2e8f0;font-weight:600;font-size:0.9rem;margin-bottom:6px">{title}</div>
                <div style="color:#94a3b8;font-size:0.84rem;line-height:1.65">{body}</div>
            </div>
        </div>""", unsafe_allow_html=True)

st.markdown("---")

# ── 4. Class Imbalance ────────────────────────────────────────────────────────
st.markdown("## 4 · Handling Class Imbalance")

col_a, col_b, col_c = st.columns(3)
with col_a:
    st.markdown("""
    <div class="metric-card" style="border-top:3px solid #f87171">
    <h4 style="color:#f87171;margin:0 0 10px">😟 The Problem</h4>
    <p style="color:#94a3b8;font-size:0.86rem;line-height:1.7;margin:0">
    With only <strong style="color:#fca5a5">26 %</strong> churners, a model
    that predicts <em>nobody churns</em> achieves 74 % accuracy while being
    completely useless. Standard classifiers learn to favour the majority class.
    </p>
    </div>""", unsafe_allow_html=True)

with col_b:
    st.markdown("""
    <div class="metric-card" style="border-top:3px solid #f59e0b">
    <h4 style="color:#f59e0b;margin:0 0 10px">🔬 How SMOTE Works</h4>
    <p style="color:#94a3b8;font-size:0.86rem;line-height:1.7;margin:0">
    For each minority-class (churn) sample, SMOTE picks a random nearest
    neighbour and creates a new synthetic point somewhere along the line
    between them,thereby adding diversity rather than just duplicating.
    </p>
    </div>""", unsafe_allow_html=True)

with col_c:
    st.markdown("""
    <div class="metric-card" style="border-top:3px solid #4ade80">
    <h4 style="color:#4ade80;margin:0 0 10px">✅ The Result</h4>
    <p style="color:#94a3b8;font-size:0.86rem;line-height:1.7;margin:0">
    After SMOTE the training set is <strong style="color:#86efac">50/50</strong>.
    The model learns both classes equally, dramatically improving recall on
    the minority class, which is exactly what  retention teams need.
    </p>
    </div>""", unsafe_allow_html=True)

# Before/after visual
bc1, bc2 = st.columns(2)
with bc1:
    st.markdown("""
    <div style="background:#1a1d2e;border:1px solid #2a2d3e;border-radius:10px;padding:16px">
    <p style="color:#94a3b8;font-size:0.78rem;text-transform:uppercase;letter-spacing:0.06em;margin:0 0 10px;font-weight:600">
        Before SMOTE — Training set
    </p>
    <div style="margin-bottom:8px">
        <div style="display:flex;justify-content:space-between;margin-bottom:3px">
            <span style="color:#4ade80;font-size:0.82rem">No Churn</span>
            <span style="color:#4ade80;font-size:0.82rem">73.5 %</span>
        </div>
        <div style="background:#2a2d3e;border-radius:4px;height:10px">
            <div style="width:73.5%;background:#4ade80;border-radius:4px;height:10px"></div>
        </div>
    </div>
    <div>
        <div style="display:flex;justify-content:space-between;margin-bottom:3px">
            <span style="color:#f87171;font-size:0.82rem">Churn</span>
            <span style="color:#f87171;font-size:0.82rem">26.5 %</span>
        </div>
        <div style="background:#2a2d3e;border-radius:4px;height:10px">
            <div style="width:26.5%;background:#f87171;border-radius:4px;height:10px"></div>
        </div>
    </div>
    </div>""", unsafe_allow_html=True)

with bc2:
    st.markdown("""
    <div style="background:#1a1d2e;border:1px solid #2a2d3e;border-radius:10px;padding:16px">
    <p style="color:#94a3b8;font-size:0.78rem;text-transform:uppercase;letter-spacing:0.06em;margin:0 0 10px;font-weight:600">
        After SMOTE — Training set
    </p>
    <div style="margin-bottom:8px">
        <div style="display:flex;justify-content:space-between;margin-bottom:3px">
            <span style="color:#4ade80;font-size:0.82rem">No Churn</span>
            <span style="color:#4ade80;font-size:0.82rem">50 %</span>
        </div>
        <div style="background:#2a2d3e;border-radius:4px;height:10px">
            <div style="width:50%;background:#4ade80;border-radius:4px;height:10px"></div>
        </div>
    </div>
    <div>
        <div style="display:flex;justify-content:space-between;margin-bottom:3px">
            <span style="color:#f87171;font-size:0.82rem">Churn (+ synthetic)</span>
            <span style="color:#f87171;font-size:0.82rem">50 %</span>
        </div>
        <div style="background:#2a2d3e;border-radius:4px;height:10px">
            <div style="width:50%;background:#f87171;border-radius:4px;height:10px"></div>
        </div>
    </div>
    </div>""", unsafe_allow_html=True)

st.markdown("---")

# ── 5. Why Logistic Regression ────────────────────────────────────────────────
st.markdown("## 5 · Model Selection")
st.markdown('<p style="color:#94a3b8;margin-bottom:16px">Several classifiers were evaluated. Logistic Regression was selected as the production model for the reasons below.</p>', unsafe_allow_html=True)

cols = st.columns(3)
reasons = [
    ("📐", "#6366f1", "Interpretable Coefficients",
     "Each feature's coefficient maps directly to its contribution to the churn log-odds. "
     "A manager can understand why a prediction was made without a PhD."),
    ("⚡", "#8b5cf6", "Exact SHAP Values",
     "SHAP's <code>LinearExplainer</code> computes mathematically exact Shapley values for "
     "linear models in O(features) time; no Monte Carlo sampling or approximations."),
    ("🎲", "#a78bfa", "DiCE Compatible",
     "DiCE's gradient-based counterfactual generation requires a differentiable model. "
     "Logistic regression's smooth decision boundary enables fast, valid counterfactuals."),
]
for col, (icon, color, title, body) in zip(cols, reasons):
    with col:
        st.markdown(f"""
        <div class="metric-card" style="text-align:center;border-top:3px solid {color}">
            <div style="font-size:2rem;margin-bottom:10px">{icon}</div>
            <h4 style="color:{color};margin:0 0 8px;font-size:0.95rem">{title}</h4>
            <p style="color:#94a3b8;font-size:0.84rem;margin:0;line-height:1.65">{body}</p>
        </div>""", unsafe_allow_html=True)

with st.expander("🔎 Model comparison — what else was tried"):
    models = [
        ("Logistic Regression", "✅ Selected", "#4ade80",
         "Best balance of interpretability, SHAP/DiCE compatibility, and performance. Recall ~77 %, ROC-AUC ~85 %."),
        ("Random Forest", "🔄 Evaluated", "#f59e0b",
         "Slightly higher accuracy but tree-based SHAP approximation is slower and DiCE counterfactuals are less stable."),
        ("XGBoost", "🔄 Evaluated", "#f59e0b",
         "Strong AUC performance but harder to explain to non-technical stakeholders. Selected against for interpretability reasons."),
        ("Decision Tree", "❌ Rejected", "#f87171",
         "High variance, overfits the training data. Low generalisation. Abandoned early."),
        ("Naïve Bayes", "❌ Rejected", "#f87171",
         "Independence assumption violated by correlated telecom features. Poor calibration."),
    ]
    for name, status, color, desc in models:
        st.markdown(f"""
        <div style="display:flex;gap:12px;padding:10px 0;border-bottom:1px solid #2a2d3e;align-items:flex-start">
            <span style="color:{color};font-size:0.82rem;font-weight:700;min-width:100px">{status}</span>
            <div>
                <div style="color:#e2e8f0;font-weight:600;font-size:0.88rem">{name}</div>
                <div style="color:#94a3b8;font-size:0.83rem;margin-top:3px;line-height:1.55">{desc}</div>
            </div>
        </div>""", unsafe_allow_html=True)

st.markdown("---")

# ── 6. Explainability ─────────────────────────────────────────────────────────
st.markdown("## 6 · Explainability Stack")

col_shap, col_dice = st.columns(2)
with col_shap:
    st.markdown("""
    <div class="metric-card" style="border-top:3px solid #6366f1">
    <h4 style="color:#a78bfa;margin:0 0 10px">📊 SHAP — Feature Attribution</h4>
    <p style="color:#94a3b8;font-size:0.87rem;line-height:1.7;margin:0 0 12px">
    <strong style="color:#cbd5e1">SHapley Additive exPlanations</strong> uses
    cooperative game theory to attribute each feature's fair contribution to
    a given prediction. For linear models, these values are exact — not approximations.
    </p>
    <div style="background:#13111c;border-radius:8px;padding:12px;margin-bottom:12px">
        <div style="color:#64748b;font-size:0.75rem;text-transform:uppercase;letter-spacing:0.06em;margin-bottom:8px">What SHAP answers</div>
        <div style="color:#94a3b8;font-size:0.83rem;line-height:1.6">
            📈 <strong style="color:#cbd5e1">Global:</strong> Which features matter most across all customers?<br>
            🎯 <strong style="color:#cbd5e1">Local:</strong> Why did <em>this specific customer</em> get this score?
        </div>
    </div>
    <p style="color:#64748b;font-size:0.8rem;margin:0">
        Uses <code>shap.LinearExplainer</code> — O(features) complexity, exact values.
    </p>
    </div>""", unsafe_allow_html=True)

with col_dice:
    st.markdown("""
    <div class="metric-card" style="border-top:3px solid #8b5cf6">
    <h4 style="color:#a78bfa;margin:0 0 10px">🎲 DiCE — Counterfactual Reasoning</h4>
    <p style="color:#94a3b8;font-size:0.87rem;line-height:1.7;margin:0 0 12px">
    <strong style="color:#cbd5e1">Diverse Counterfactual Explanations</strong>
    answers: <em>"What is the minimum change needed to flip this prediction?"</em>
    </p>
    <div style="background:#13111c;border-radius:8px;padding:12px;margin-bottom:12px">
        <div style="color:#64748b;font-size:0.75rem;text-transform:uppercase;letter-spacing:0.06em;margin-bottom:8px">Design choices</div>
        <div style="color:#94a3b8;font-size:0.83rem;line-height:1.6">
            🔒 <strong style="color:#cbd5e1">Immutable:</strong> Demographics never change<br>
            🎯 <strong style="color:#cbd5e1">Diverse:</strong> Each scenario takes a different path<br>
            ✅ <strong style="color:#cbd5e1">Actionable:</strong> Only real-world feasible values
        </div>
    </div>
    <p style="color:#64748b;font-size:0.8rem;margin:0">
        Generates 2–5 scenarios per customer. Runtime: ~15–30 seconds.
    </p>
    </div>""", unsafe_allow_html=True)

st.markdown("---")

# ── 7. Evaluation ─────────────────────────────────────────────────────────────
st.markdown("## 7 · Model Evaluation")

st.markdown("""
<div class="metric-card">
<p style="color:#94a3b8;font-size:0.88rem;line-height:1.7;margin:0">
Evaluated on a <strong>stratified 80/20 train-test split</strong>.
Stratification preserves the 26/74 class ratio in both sets.
Primary metric is <strong style="color:#a78bfa">Recall</strong> for the churn class —
missing a churner (false negative) is more costly than a false alarm (false positive)
in a retention context.
</p>
</div>""", unsafe_allow_html=True)

metric_cols = st.columns(4)
metrics = [
    ("Accuracy", "~80 %", "#a78bfa",
     "Correct predictions / total. Less meaningful given class imbalance."),
    ("Precision", "~65 %", "#6366f1",
     "Of all predicted churners, ~65 % actually churned."),
    ("Recall", "~77 %", "#4ade80",
     "Of all real churners, ~77 % were correctly identified. Primary metric."),
    ("ROC-AUC", "~85 %", "#f59e0b",
     "Probability that the model ranks a churner higher than a non-churner."),
]
for col, (name, val, color, desc) in zip(metric_cols, metrics):
    with col:
        st.markdown(f"""
        <div class="metric-card" style="text-align:center;border-top:3px solid {color}">
            <div style="font-size:2rem;font-weight:800;color:{color}">{val}</div>
            <div style="color:#cbd5e1;font-size:0.88rem;font-weight:600;margin:4px 0">{name}</div>
            <div style="color:#64748b;font-size:0.75rem;line-height:1.5">{desc}</div>
        </div>""", unsafe_allow_html=True)

st.markdown("""
<div style="padding:12px 16px;background:#1a1d2e;border:1px solid #2a2d3e;
     border-left:3px solid #f59e0b;border-radius:0 8px 8px 0;
     color:#94a3b8;font-size:0.82rem;margin-top:4px">
    ℹ️ These values are approximate. Exact figures vary slightly per training run.
    Consult the notebook's classification report cell for precise per-run values.
</div>""", unsafe_allow_html=True)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown(
    '<p style="color:#475569;text-align:center;font-size:0.8rem">'
    "Churn Intelligence Dashboard · Powered by Logistic Regression + DiCE Counterfactuals"
    "</p>",
    unsafe_allow_html=True,
)
