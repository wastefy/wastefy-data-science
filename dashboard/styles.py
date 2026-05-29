import streamlit as st
CUSTOM_CSS = """
    <style>
    .main-header {
        font-size: 2rem;
        font-weight: bold;
        color: #2E7D32;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
    }
    .sidebar-divider {
        border-top: 1px solid #ddd;
        margin: 1rem 0;
    }
    </style>
"""


def inject_css():
    """Inject custom CSS ke halaman Streamlit."""
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)