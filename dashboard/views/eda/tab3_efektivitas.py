# pages/eda/tab3_efektivitas.py
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import pandas as pd

def render(df):
    st.markdown("## Analisis Efektivitas Penyimpanan")

    if 'sisa_hari' not in df.columns:
        st.error("Kolom `sisa_hari` tidak ditemukan dalam dataset.")
        return

    st.markdown("### 1. Lokasi Penyimpanan yang Paling Efektif Menjaga Sisa Umur Simpan")

    storage_stats = (
        df.groupby('lokasi_penyimpanan')['sisa_hari']
        .agg(['mean', 'median', 'std']).round(2)
        .sort_values('mean', ascending=False)
    )
    st.dataframe(storage_stats, use_container_width=True)

    fig, ax = plt.subplots(figsize=(10, 5))
    storage_stats['mean'].plot(
        kind='bar',
        color=sns.color_palette('Set2', len(storage_stats)),
        edgecolor='white', width=0.5, ax=ax
    )
    ax.set(
        title='Rata-rata Sisa Hari per Lokasi Penyimpanan',
        xlabel='Lokasi Penyimpanan',
        ylabel='Rata-rata Sisa Hari'
    )
    ax.tick_params(axis='x', rotation=15)
    for p in ax.patches:
        ax.annotate(
            f'{p.get_height():.1f}',
            (p.get_x() + p.get_width() / 2, p.get_height()),
            ha='center', va='bottom', fontweight='bold'
        )
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

    best_loc = storage_stats.index[0]
    st.success(
        f"**{best_loc}** memiliki rata-rata sisa hari tertinggi "
        f"({storage_stats.loc[best_loc, 'mean']:.1f} hari) — lokasi paling efektif menjaga kesegaran."
    )

    st.markdown("---")

    st.markdown("### 2. Perbedaan Signifikan Sisa Hari Antar Lokasi Penyimpanan")
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.boxplot(data=df, x='lokasi_penyimpanan', y='sisa_hari', palette='Set2', ax=ax)
    ax.set(
        title='Distribusi Sisa Hari per Lokasi Penyimpanan',
        xlabel='Lokasi Penyimpanan',
        ylabel='Sisa Hari'
    )
    ax.tick_params(axis='x', rotation=15)
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

    groups = [
        grp['sisa_hari'].values
        for _, grp in df.groupby('lokasi_penyimpanan')
        if len(grp) > 1
    ]
    if len(groups) >= 2:
        f_stat, p_val = stats.f_oneway(*groups)
        c1, c2 = st.columns(2)
        with c1:
            st.metric("F-statistic (ANOVA)", f"{f_stat:.4f}")
        with c2:
            st.metric("p-value", f"{p_val:.4f}")

        if p_val < 0.05:
            st.success("Terdapat perbedaan signifikan sisa hari antar lokasi penyimpanan (p < 0.05).")
        else:
            st.info("Tidak terdapat perbedaan signifikan antar lokasi penyimpanan (p ≥ 0.05).")

    st.markdown("---")

    st.markdown("### 3. Distribusi Jenis Item di Setiap Lokasi Penyimpanan")

    cross_tab = pd.crosstab(df['jenis_item'], df['lokasi_penyimpanan'])

    fig, ax = plt.subplots(figsize=(8, 5))
    sns.heatmap(cross_tab, annot=True, fmt='d', cmap='Blues', linewidths=0.5, ax=ax)
    ax.set(
        title='Jumlah Item: Jenis vs Lokasi Penyimpanan',
        xlabel='Lokasi Penyimpanan',
        ylabel='Jenis Item'
    )
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

    st.markdown("---")

    st.markdown("### 4. Kombinasi Jenis Item & Lokasi yang Tampak Tidak Sesuai")

    pivot = df.pivot_table(
        values='sisa_hari', index='jenis_item',
        columns='lokasi_penyimpanan', aggfunc='mean'
    )

    fig, ax = plt.subplots(figsize=(8, 5))
    sns.heatmap(pivot, annot=True, fmt='.1f', cmap='RdYlGn', linewidths=0.5, ax=ax)
    ax.set(
        title='Rata-rata Sisa Hari: Jenis vs Lokasi',
        xlabel='Lokasi Penyimpanan',
        ylabel='Jenis Item'
    )
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

    st.markdown("""
    #### Cara membaca heatmap:
    - **Hijau** = rata-rata sisa hari tinggi → penyimpanan efektif
    - **Merah** = rata-rata sisa hari rendah → potensi mismatch lokasi atau item memang cepat habis
    """)

    st.markdown("---")

    if 'hari_sejak_pembelian' not in df.columns:
        return

    st.markdown("### 5. Tren Sisa Hari vs Hari Sejak Pembelian per Lokasi Penyimpanan")

    lokasi_list = df['lokasi_penyimpanan'].unique()
    n_loc = len(lokasi_list)

    fig, axes = plt.subplots(1, n_loc, figsize=(6 * n_loc, 5), sharey=True)
    if n_loc == 1:
        axes = [axes]

    for ax, loc in zip(axes, lokasi_list):
        group = df[df['lokasi_penyimpanan'] == loc]
        for item, color in zip(['Buah', 'Sayur'], ['#FF7043', '#4CAF50']):
            sub = group[group['jenis_item'] == item]
            if not sub.empty:
                trend = sub.groupby('hari_sejak_pembelian')['sisa_hari'].mean()
                ax.plot(trend.index, trend.values, marker='o', label=item, color=color)
        ax.set(
            title=f'Lokasi: {loc}',
            xlabel='Hari Sejak Pembelian',
            ylabel='Rata-rata Sisa Hari'
        )
        ax.legend()

    plt.suptitle('Tren Sisa Hari vs Hari Sejak Pembelian', fontsize=14, fontweight='bold')
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()