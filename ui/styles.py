"""
ui/styles.py
------------
Injects the global custom CSS. Call inject_styles() once from app.py
before rendering any other component.
"""

import streamlit as st

_CSS = """
<style>
    /* ── Layout ── */
    .stApp { background-color: #0f1117; }

    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1d2e 0%, #12141f 100%);
        border-right: 1px solid #2a2d3e;
    }
    [data-testid="stSidebar"] .stMarkdown h2,
    [data-testid="stSidebar"] .stMarkdown h3 {
        color: #a78bfa;
    }

    /* ── Cards ── */
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

    /* ── Typography helpers ── */
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

    /* ── Diff badges ── */
    .change-badge-pos {
        background: #1a3d26; border: 1px solid #2d7a4a;
        color: #4ade80; border-radius: 20px;
        padding: 2px 10px; font-size: 0.82rem; font-weight: 500;
        display: inline-block; margin: 2px;
    }
    .change-badge-neg {
        background: #3d1a1a; border: 1px solid #7a2d2d;
        color: #f87171; border-radius: 20px;
        padding: 2px 10px; font-size: 0.82rem; font-weight: 500;
        display: inline-block; margin: 2px;
    }
    .change-badge-neutral {
        background: #1e2130; border: 1px solid #3a3d50;
        color: #94a3b8; border-radius: 20px;
        padding: 2px 10px; font-size: 0.82rem; font-weight: 500;
        display: inline-block; margin: 2px;
    }

    /* ── Probability bar ── */
    .probability-bar-container {
        background: #1e2130;
        border-radius: 8px;
        height: 12px;
        margin: 10px 0;
        overflow: hidden;
    }

    /* ── Button ── */
    .stButton > button {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        color: white; border: none; border-radius: 8px;
        padding: 12px 32px; font-weight: 600; font-size: 1rem;
        width: 100%; transition: opacity 0.2s;
    }
    .stButton > button:hover { opacity: 0.88; }

    /* ── Form widget labels ── */
    div[data-testid="stSelectbox"] label,
    div[data-testid="stNumberInput"] label,
    div[data-testid="stSlider"] label {
        color: #cbd5e1 !important;
        font-size: 0.88rem;
    }

    /* ── Tabs ── */
    .stTabs [data-baseweb="tab"]          { color: #94a3b8; font-weight: 500; }
    .stTabs [aria-selected="true"]        { color: #a78bfa !important; }
</style>
"""


def inject_styles() -> None:
    """Inject global CSS into the Streamlit page. Call once at app startup."""
    st.markdown(_CSS, unsafe_allow_html=True)
