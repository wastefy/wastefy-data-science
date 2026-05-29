import pandas as pd
import streamlit as st
@st.cache_data
def load_data():
    df = pd.read_csv('../dataset/clean/sayur_buah_bersih.csv')

    if 'hari_sejak_pembelian' in df.columns:
        df['hari_sejak_pembelian'] = (
            df.groupby('jenis_item')['hari_sejak_pembelian']
            .transform(lambda x: x.fillna(x.median()))
        )

    if 'sisa_hari' in df.columns:
        df['kategori_buah'] = df['sisa_hari'].apply(_kategori_buah)

    return df


def apply_filters(df, kategori, lokasi):
    df_f = df.copy()
    if kategori != "Semua":
        df_f = df_f[df_f['jenis_item'] == kategori]
    if lokasi != "Semua":
        df_f = df_f[df_f['lokasi_penyimpanan'] == lokasi]
    return df_f


def _kategori_buah(sisa_hari):
    """Kategorikan buah berdasarkan sisa hari."""
    if 0 <= sisa_hari <= 2:
        return 'Busuk'
    elif 4 <= sisa_hari <= 8:
        return 'Terlalu Matang'
    elif 10 <= sisa_hari <= 20:
        return 'Matang'
    elif 14 <= sisa_hari <= 28:
        return 'Mentah'
    else:
        return 'Lainnya'