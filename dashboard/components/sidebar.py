# components/sidebar.py
import streamlit as st
from PIL import Image
from pathlib import Path


def render_sidebar(df_clean):
    try:
        base_dir = Path(__file__).resolve().parents[1]
        logo_path = base_dir / "logo" / "logo_wastefy.png"
        if logo_path.exists():
            logo = Image.open(logo_path)
            has_logo = True
        else:
            has_logo = False
    except Exception:
        has_logo = False

    with st.sidebar:
        col1, col2 = st.columns([1, 3], vertical_alignment="center")
        with col1:
            if has_logo:
                st.image(logo, width=100)

        with col2:
            st.markdown("### Wastefy Data Dashboard")

        _divider()
        st.text("Dashboard ini berfungsi untuk menampilkan hasil EDA "
                "dan simulasi model yang dibuat oleh tim AI")
        _divider()

        st.markdown("### Navigasi")
        page = st.radio(
            "Pilih Halaman",
            options=["Analisis Data (EDA)", "Fitur AI"],
            label_visibility="collapsed"
        )

        _divider()

        st.markdown("### Filter Data")
        kategori = st.selectbox(
            "Pilih Kategori",
            options=["Semua"] + sorted(df_clean['jenis_item'].unique().tolist()),
            help="Filter berdasarkan jenis produk"
        )
        lokasi = st.selectbox(
            "Pilih Lokasi Penyimpanan",
            options=["Semua"] + sorted(df_clean['lokasi_penyimpanan'].unique().tolist()),
            help="Filter berdasarkan lokasi penyimpanan"
        )

        if st.button("Reset Filter", use_container_width=True):
            st.cache_data.clear()
            st.rerun()

        _divider()

        st.caption("© 2026 Wastefy Team")

    return page, kategori, lokasi


def _divider():
    st.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)