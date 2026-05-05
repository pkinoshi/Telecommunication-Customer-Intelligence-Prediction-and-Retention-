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

    /* ── Hero banner ── */
    .hero-banner {
        background: linear-gradient(135deg, #13111c 0%, #1a1040 50%, #0f1a2e 100%);
        border: 1px solid #2a2d3e;
        border-radius: 16px;
        padding: 48px 40px;
        text-align: center;
        position: relative;
        overflow: hidden;
        margin-bottom: 24px;
    }
    .hero-banner::before {
        content: "";
        position: absolute;
        top: -60px; right: -60px;
        width: 220px; height: 220px;
        background: radial-gradient(circle, rgba(99,102,241,0.18) 0%, transparent 70%);
        border-radius: 50%;
    }
    .hero-banner::after {
        content: "";
        position: absolute;
        bottom: -40px; left: -40px;
        width: 180px; height: 180px;
        background: radial-gradient(circle, rgba(167,139,250,0.14) 0%, transparent 70%);
        border-radius: 50%;
    }

    /* ── Stat pill ── */
    .stat-pill {
        display: inline-block;
        background: rgba(99,102,241,0.15);
        border: 1px solid rgba(99,102,241,0.35);
        border-radius: 24px;
        padding: 6px 18px;
        color: #a78bfa;
        font-size: 0.85rem;
        font-weight: 600;
        margin: 4px;
    }

    /* ── Pipeline node ── */
    .pipeline-node {
        background: linear-gradient(135deg, #1e2130, #252840);
        border: 1px solid #3b4fd4;
        border-top: 3px solid;
        border-radius: 10px;
        padding: 16px;
        text-align: center;
        height: 100%;
    }
    .pipeline-arrow {
        color: #475569;
        font-size: 1.4rem;
        display: flex;
        align-items: center;
        justify-content: center;
        height: 100%;
    }

    /* ── Highlight quote ── */
    .highlight-quote {
        border-left: 4px solid #6366f1;
        background: linear-gradient(135deg, #1a1d2e, #1e2240);
        border-radius: 0 10px 10px 0;
        padding: 16px 20px;
        margin: 16px 0;
        color: #cbd5e1;
        font-style: italic;
        font-size: 0.95rem;
        line-height: 1.7;
    }

    /* ── Risk zone bar ── */
    .risk-zone-bar {
        height: 16px;
        border-radius: 8px;
        background: linear-gradient(to right, #22c55e 0%, #f59e0b 50%, #ef4444 100%);
        margin: 8px 0 4px;
        position: relative;
    }

    /* ── Tag badge ── */
    .tag {
        display: inline-block;
        background: #1e2130;
        border: 1px solid #2a2d3e;
        border-radius: 6px;
        padding: 2px 8px;
        color: #94a3b8;
        font-size: 0.75rem;
        font-family: monospace;
        margin: 2px;
    }
</style>
"""


def inject_styles() -> None:
    """Inject global CSS into the Streamlit page. Call once at app startup."""
    st.markdown(_CSS, unsafe_allow_html=True)
