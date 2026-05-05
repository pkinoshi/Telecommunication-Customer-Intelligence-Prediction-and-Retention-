# Customer Churn Intelligence App

A Streamlit web app for predicting telecom customer churn and generating
retention scenarios using DiCE counterfactual explanations.

---

## Setup

### 1. Export model files from your Colab notebook
Add these cells at the end of your notebook and run them:

```python
# Already in your notebook — just make sure these ran:
joblib.dump(model_pipeline, "churn_model_pipeline.pkl")
joblib.dump(target_encoder, "target_encoder.pkl")
df_raw.to_csv("df_cleaned_raw.csv", index=False)
```

Download all three files from Colab:
```python
from google.colab import files
files.download("churn_model_pipeline.pkl")
files.download("target_encoder.pkl")
files.download("df_cleaned_raw.csv")
```

### 2. Place files in the same folder as app.py
```
churn_app/
├── app.py
├── requirements.txt
├── churn_model_pipeline.pkl   ← from Colab
├── target_encoder.pkl          ← from Colab
└── df_cleaned_raw.csv          ← from Colab
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the app
```bash
streamlit run app.py
```

The app will open at http://localhost:8501

---

## How it works

1. **Fill in customer details** in the left sidebar — all fields use
   dropdowns and sliders, no codes or numbers for categorical fields.

2. **Click Run Prediction** — the model returns a churn probability
   and a clear High / Low risk verdict.

3. **If churn risk is high**, DiCE automatically generates 2–5
   "What-if" scenarios showing the minimum changes needed to flip
   the customer from "Likely to Leave" → "Likely to Stay".

   - 🟢 Green = a favourable change (e.g. longer contract, lower charges)
   - 🔴 Red = a cost increase required
   - ⬜ Grey = no change needed for this feature

---

## Features fixed (immutable in counterfactuals)
- Gender, Senior Citizen status, Partner, Dependents

## Features varied by DiCE
- Contract type, Internet/Phone services, Payment method,
  Online Security/Backup, Tech Support, Streaming, Monthly Charges
