"""
config.py
---------
Single source of truth for all feature definitions, column ordering,
and DiCE configuration. Nothing is hard-coded anywhere else.
"""

# ── Categorical option lists ──────────────────────────────────────────────────
BINARY_YES_NO     = ["No", "Yes"]
YES_NO_NOPHONE    = ["No", "No phone service", "Yes"]
YES_NO_NOINTERNET = ["No", "No internet service", "Yes"]

FEATURE_OPTIONS: dict[str, list] = {
    "gender":           ["Female", "Male"],
    "SeniorCitizen":    BINARY_YES_NO,
    "Partner":          BINARY_YES_NO,
    "Dependents":       BINARY_YES_NO,
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
    "PaymentMethod": [
        "Bank transfer (automatic)",
        "Credit card (automatic)",
        "Electronic check",
        "Mailed check",
    ],
}

# ── Human-readable labels ─────────────────────────────────────────────────────
FEATURE_LABELS: dict[str, str] = {
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

# ── Column order expected by the pipeline ─────────────────────────────────────
COLUMN_ORDER: list[str] = [
    "gender", "SeniorCitizen", "Partner", "Dependents", "PhoneService",
    "MultipleLines", "InternetService", "OnlineSecurity", "OnlineBackup",
    "DeviceProtection", "TechSupport", "StreamingTV", "StreamingMovies",
    "Contract", "PaperlessBilling", "PaymentMethod",
    "tenure", "MonthlyCharges", "TotalCharges",
]

# ── Numeric feature bounds ────────────────────────────────────────────────────
NUMERIC_BOUNDS: dict[str, dict] = {
    "tenure":         {"min": 0,    "max": 72,   "default": 12,   "step": 1},
    "MonthlyCharges": {"min": 18.0, "max": 120.0,"default": 65.0, "step": 0.5},
    "TotalCharges":   {"min": 0.0,  "max": 9000.0,"default": 780.0,"step": 1.0},
}

# ── DiCE configuration ────────────────────────────────────────────────────────
CONTINUOUS_FEATURES: list[str] = ["tenure", "MonthlyCharges", "TotalCharges"]

# Features DiCE is NOT allowed to change (demographics / identity)
IMMUTABLE_FEATURES: list[str] = ["gender", "SeniorCitizen", "Partner", "Dependents"]

# Features DiCE is allowed to vary when searching for retention scenarios
FEATURES_TO_VARY: list[str] = [
    "PhoneService", "MultipleLines", "InternetService", "OnlineSecurity",
    "OnlineBackup", "DeviceProtection", "TechSupport", "StreamingTV",
    "StreamingMovies", "Contract", "PaperlessBilling", "PaymentMethod",
    "MonthlyCharges",
]

DICE_PERMITTED_RANGE: dict[str, list] = {
    "MonthlyCharges": [18, 120],
}

# ── Artifact file paths ───────────────────────────────────────────────────────
PIPELINE_PATH      = "churn_model_pipeline.pkl"
TARGET_ENCODER_PATH = "target_encoder.pkl"
RAW_DATA_PATH      = "df_cleaned_raw.csv"
