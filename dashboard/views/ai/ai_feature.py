import streamlit as st
import requests
import datetime

def render(df_clean, HF_BASE_URL):
    st.markdown("### AI Smart-Scan & Prediksi Masa Simpan")
    st.info(
        "Silakan unggah foto bahan makanan. Sistem akan mendeteksi jenis, kondisi fisik, menghitung estimasi sisa hari simpan, dan menghasilkan panduan penyimpanan."
    )

    with st.container(border=True):
        left_cfg, right_cfg = st.columns([3, 2], vertical_alignment="bottom")
        with left_cfg:
            api_key = st.text_input(
                "X-API-Key",
                type="password",
                placeholder="Masukkan API key",
            )
        with right_cfg:
            tanggal_beli_date = st.date_input(
                "Tanggal Pembelian",
                value=datetime.date.today(),
                max_value=datetime.date.today(),
                help="Pilih tanggal pembelian",
            )
        tanggal_beli = tanggal_beli_date.isoformat()

        uploaded_file = st.file_uploader(
            "Upload gambar produk sayur/buah",
            type=["jpg", "jpeg", "png"],
            label_visibility="collapsed",
        )

    if uploaded_file is None:
        return

    if not api_key:
        st.warning("Masukkan API-Key dulu sebelum menjalankan vision/regression.")
        return

    # Preview gambar dibuat lebih ringkas untuk file besar
    size_bytes = len(uploaded_file.getvalue())
    img_preview_kwargs = {"width": 320} if size_bytes > 300_000 else {"use_container_width": True}

    main_left, main_right = st.columns([1.05, 1.15], vertical_alignment="top")

    with main_left:
        with st.container(border=True):
            st.markdown("##### Preview Gambar")
            st.image(uploaded_file, caption="Gambar Bahan Makanan", **img_preview_kwargs)

    with main_right:
        with st.container(border=True):
            st.markdown("##### Hasil Vision")
            jenis_item, nama_item, kondisi_fisik = _call_vision_api(uploaded_file, HF_BASE_URL, api_key)
            if jenis_item is None:
                return

            if kondisi_fisik in ["Busuk", "Expired"]:
                st.error("Kondisi fisik kritis")
            elif kondisi_fisik == "Terlalu Matang":
                st.warning(f"{nama_item} perlu segera diproses")
            else:
                st.success("Kondisi fisik relatif aman")

        st.markdown("")

        with st.container(border=True):
            st.markdown("##### Hasil Regresi")
            sisa_hari = _call_regression_api(
                df_clean, HF_BASE_URL, api_key, nama_item, kondisi_fisik, jenis_item, tanggal_beli
            )

            metric_col_1, metric_col_2, metric_col_3 = st.columns(3)
            with metric_col_1:
                st.metric(
                    "Estimasi Sisa Hari",
                    f"{sisa_hari} Hari",
                    delta="Kritis! Segera Olah" if sisa_hari < 3 else "Aman untuk Stok",
                    delta_color="inverse" if sisa_hari < 3 else "normal",
                )


# Private Helpers
def _call_vision_api(uploaded_file, HF_BASE_URL, api_key):
    with st.spinner("Menganalisis gambar.."):
        try:
            headers = {"X-API-Key": api_key} if api_key else None
            response = requests.post(
                f"{HF_BASE_URL}/predict/vision",
                files={"file_foto": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)},
                headers=headers,
                timeout=30
            )

            if response.status_code == 401:
                st.error("API Key tidak valid atau tidak ada.")
                return None, None, None

            if response.status_code == 422:
                st.error("Format atau ukuran file tidak valid (maks 5MB, JPEG/PNG).")
                return None, None, None

            if response.status_code != 200:
                st.error(f"Vision API error: {response.status_code}")
                return None, None, None

            data = response.json()
            result = data.get("data", {})

            # Cek apakah gambar di luar scope dataset
            if result.get("out_of_scope"):
                st.warning("Gambar tidak dikenali sebagai sayur atau buah yang didukung.")
                return None, None, None

            jenis_item = result.get("jenis_item")
            nama_item = result.get("nama_item")
            kondisi_fisik = result.get("kondisi_fisik")
            confidence = result.get("confidence", 0)

            st.success("Deteksi visual berhasil!")
            st.markdown(f"**Jenis Kategori:** {jenis_item}")
            st.markdown(f"**Nama Komoditas:** {nama_item}")
            st.markdown(f"**Kondisi Fisik:** {kondisi_fisik}")
            st.markdown(f"**Confidence:** {confidence:.2%}")

           

            return jenis_item, nama_item, kondisi_fisik

        except Exception as e:
            st.error(f"Gagal terhubung ke Vision API: {e}")
            return None, None, None

def _call_regression_api(df_clean, HF_BASE_URL, api_key, nama_item, kondisi_fisik, jenis_item, tanggal_beli):
    with st.spinner("Menghitung estimasi sisa hari..."):
        try:
            headers = {"X-API-Key": api_key} if api_key else None
            lokasi_match = df_clean.loc[
                df_clean['nama_item'].str.lower() == nama_item.lower(), 'lokasi_penyimpanan'
            ].dropna()
            lokasi_penyimpanan = lokasi_match.mode().iloc[0] if not lokasi_match.mode().empty else "Suhu Ruang"

            response = requests.post(
                f"{HF_BASE_URL}/predict/regression",
                headers=headers,
                json={
                    "nama_item"          : nama_item,
                    "jenis_item"         : jenis_item,
                    "kondisi_fisik"      : kondisi_fisik,
                    "lokasi_penyimpanan" : lokasi_penyimpanan,
                    "tanggal_beli"       : tanggal_beli
                },
                timeout=30
            )

            if response.status_code == 401:
                st.error("API Key tidak valid atau tidak ada.")
                return _fallback_sisa_hari(df_clean, nama_item, kondisi_fisik)

            if response.status_code != 200:
                st.error(f"Regression API error: {response.status_code}")
                return _fallback_sisa_hari(df_clean, nama_item, kondisi_fisik)

            data = response.json()
            if data.get("status") == "success":
                sisa_hari = int(data["data"]["sisa_hari"])
                st.success("Prediksi regresi berhasil!")
                return sisa_hari

        except Exception as e:
            st.warning(f"Regression API gagal, menggunakan data historis. ({e})")

        # Fallback ke median dataset CSV
        st.caption("Menggunakan fallback data historis.")
        return _fallback_sisa_hari(df_clean, nama_item, kondisi_fisik)


def _fallback_sisa_hari(df_clean, nama_item, kondisi_fisik):
    """Hitung median sisa hari dari dataset sebagai fallback."""
    matched = df_clean[df_clean['nama_item'].str.lower() == nama_item.lower()]
    if matched.empty:
        return 3

    cond_matched = matched[matched['label'] == kondisi_fisik]
    if not cond_matched.empty:
        return int(cond_matched['sisa_hari'].median())

    return int(matched['sisa_hari'].median())
