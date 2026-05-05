"""
model.py
--------
All ML logic: loading artifacts, making predictions, and running DiCE
counterfactual generation. No Streamlit imports here — pure Python.
"""

import warnings
warnings.filterwarnings("ignore")

import joblib
import pandas as pd
import streamlit as st
import dice_ml
from dice_ml import Dice

from config import (
    COLUMN_ORDER,
    CONTINUOUS_FEATURES,
    IMMUTABLE_FEATURES,
    FEATURES_TO_VARY,
    DICE_PERMITTED_RANGE,
    PIPELINE_PATH,
    TARGET_ENCODER_PATH,
    RAW_DATA_PATH,
)


# ── Artifact loading ──────────────────────────────────────────────────────────
@st.cache_resource(show_spinner=False)
def load_artifacts() -> tuple:
    """
    Load and cache the model pipeline, target encoder, and raw training data.
    Returns (model_pipeline, target_encoder, df_raw) or raises on failure.
    """
    pipeline     = joblib.load(PIPELINE_PATH)
    tgt_encoder  = joblib.load(TARGET_ENCODER_PATH)
    df_raw       = pd.read_csv(RAW_DATA_PATH)
    return pipeline, tgt_encoder, df_raw


# ── Prediction ────────────────────────────────────────────────────────────────
def build_input_df(inputs: dict) -> pd.DataFrame:
    """Convert a flat inputs dict into a single-row DataFrame in pipeline column order."""
    return pd.DataFrame([inputs])[COLUMN_ORDER]


def predict(model_pipeline, df: pd.DataFrame) -> tuple[float, int]:
    """
    Run the pipeline and return (churn_probability, predicted_label).
    churn_probability is the probability of class 1 (churn).
    predicted_label is 0 (stay) or 1 (churn).
    """
    prob  = model_pipeline.predict_proba(df)[0][1]
    label = int(model_pipeline.predict(df)[0])
    return prob, label


# ── Counterfactual generation ─────────────────────────────────────────────────
def run_dice(
    model_pipeline,
    df_raw: pd.DataFrame,
    query_df: pd.DataFrame,
    n_cfs: int = 3,
):
    """
    Generate DiCE counterfactuals for a single customer predicted to churn.

    Returns a DiCE CounterfactualExamples result object, or raises on failure.
    The caller is responsible for catching exceptions and rendering errors.
    """
    dice_data = dice_ml.Data(
        dataframe=df_raw,
        continuous_features=CONTINUOUS_FEATURES,
        outcome_name="Churn",
        immutable_features=IMMUTABLE_FEATURES,
    )
    dice_model = dice_ml.Model(model=model_pipeline, backend="sklearn")
    explainer  = Dice(dice_data, dice_model)

    result = explainer.generate_counterfactuals(
        query_df,
        total_CFs=n_cfs,
        desired_class="opposite",
        features_to_vary=FEATURES_TO_VARY,
        permitted_range=DICE_PERMITTED_RANGE,
    )
    return result
