import streamlit as st
from config import HF_BASE_URL
from data_loader import load_data, apply_filters
from components.sidebar import render_sidebar
from styles import inject_css

# app.py
from views.eda.tab1_komposisi   import render as render_tab1
from views.eda.tab2_masa_simpan import render as render_tab2
from views.eda.tab3_efektivitas import render as render_tab3
from views.eda.tab4_waste_risk  import render as render_tab4
from views.ai.ai_feature       import render as render_ai

st.set_page_config(page_title="Wastefy Data Dashboard", page_icon="📊", layout="wide")

inject_css()  # ← cukup ini, tidak perlu argumen apapun

df_clean    = load_data()
page, kategori, lokasi = render_sidebar(df_clean)
df_filtered = apply_filters(df_clean, kategori, lokasi)

st.markdown(f'<div class="main-header">{page}</div>', unsafe_allow_html=True)  # ← st.markdown, bukan inject_css

if page == "Analisis Data (EDA)":
    tab1, tab2, tab3, tab4 = st.tabs([
        "Komposisi & Distribusi Inventory",
        "Analisis Masa Simpan & Kesegaran",
        "Analisis Efektivitas Penyimpanan",
        "Food Waste Risk Analysis"
    ])
    with tab1: render_tab1(df_filtered)
    with tab2: render_tab2(df_filtered)
    with tab3: render_tab3(df_filtered)
    with tab4: render_tab4(df_filtered)
else:
    render_ai(df_clean, HF_BASE_URL)