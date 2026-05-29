import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
import pandas as pd

def render(df):
    st.markdown("##Food Waste Risk Analysis")

    if 'sisa_hari' not in df.columns or 'label' not in df.columns:
        st.error("⚠️ Kolom `sisa_hari` atau `label` tidak ditemukan.")
        return

    st.markdown("### 1. Distribusi Barang Berdasarkan Kondisi Kesegaran")

    label_counts  = df['label'].value_counts()
    colors_label  = ['#66BB6A', '#FFA726', '#EF5350', '#42A5F5', '#AB47BC']

    fig, axes = plt.subplots(1, 2, figsize=(13, 5))
    axes[0].pie(
        label_counts, labels=label_counts.index, autopct='%1.1f%%',
        startangle=90, colors=colors_label[:len(label_counts)]
    )
    axes[0].set_title('Proporsi Label Kondisi')

    label_counts.plot(
        kind='bar', ax=axes[1],
        color=colors_label[:len(label_counts)], edgecolor='white'
    )
    axes[1].set(title='Jumlah per Label Kondisi', xlabel='Label', ylabel='Jumlah')
    axes[1].tick_params(axis='x', rotation=30)
    for p in axes[1].patches:
        axes[1].annotate(
            f'{int(p.get_height()):,}',
            (p.get_x() + p.get_width() / 2, p.get_height()),
            ha='center', va='bottom', fontweight='bold'
        )

    plt.suptitle('Analisis Label Kondisi Item', fontsize=14, fontweight='bold')
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

    # Metrics ringkas
    c1, c2, c3 = st.columns(3)
    with c1:
        busuk_n = label_counts.get('Busuk', 0)
        st.metric("🔴 Busuk", f"{busuk_n:,}")
    with c2:
        segar_n = label_counts.get('Segar', 0)
        st.metric("🟢 Segar", f"{segar_n:,}")
    with c3:
        kritis_n = int((df['sisa_hari'] < 3).sum())
        st.metric("⚠️ Kritis (< 3 hari)", f"{kritis_n:,}")

    st.markdown("---")

    st.markdown("### 2. Kombinasi Jenis Item & Lokasi Penyimpanan Paling Berisiko Food Waste")

    critical_df = df[df['sisa_hari'] < 3]

    if critical_df.empty:
        st.success("Tidak ada item dengan sisa hari < 3 hari dalam data yang difilter.")
    else:
        risk_combo = (
            critical_df.groupby(['jenis_item', 'lokasi_penyimpanan'])
            .size().reset_index(name='jumlah_kritis')
            .sort_values('jumlah_kritis', ascending=False)
        )
        st.dataframe(risk_combo, use_container_width=True)

        heatmap_risk = pd.pivot_table(
            critical_df, values='sisa_hari',
            index='jenis_item', columns='lokasi_penyimpanan', aggfunc='count'
        ).fillna(0)

        fig, ax = plt.subplots(figsize=(9, 5))
        sns.heatmap(heatmap_risk, annot=True, fmt='.0f', cmap='Reds', linewidths=0.5, ax=ax)
        ax.set(
            title='Heatmap Risiko Food Waste (Jumlah Item dengan Sisa < 3 Hari)',
            xlabel='Lokasi Penyimpanan',
            ylabel='Jenis Item'
        )
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()

        top_risk = risk_combo.iloc[0]
        st.error(
            f"🚨 Kombinasi paling berisiko: **{top_risk['jenis_item']}** di "
            f"**{top_risk['lokasi_penyimpanan']}** dengan "
            f"**{int(top_risk['jumlah_kritis'])}** item kritis."
        )

    st.markdown("---")

    # ── 3. Item Rata-rata Sisa Hari Paling Rendah ─────────────────────────────
    st.markdown("### 3. Item dengan Rata-rata Sisa Hari Paling Rendah")

    avg_sisa_item = (
        df.groupby(['nama_item', 'jenis_item'])['sisa_hari']
        .mean().reset_index().sort_values('sisa_hari')
    )

    fig, ax = plt.subplots(figsize=(12, 5))
    bar_colors = ['#FF7043' if t == 'Buah' else '#4CAF50' for t in avg_sisa_item['jenis_item']]
    bars = ax.bar(avg_sisa_item['nama_item'], avg_sisa_item['sisa_hari'],
                  color=bar_colors, edgecolor='white')
    ax.set(
        title='Rata-rata Sisa Hari per Item',
        xlabel='Nama Item',
        ylabel='Rata-rata Sisa Hari'
    )
    ax.tick_params(axis='x', rotation=30)
    for bar in bars:
        ax.annotate(
            f'{bar.get_height():.1f}',
            (bar.get_x() + bar.get_width() / 2, bar.get_height()),
            ha='center', va='bottom'
        )
    ax.legend(handles=[
        mpatches.Patch(color='#FF7043', label='Buah'),
        mpatches.Patch(color='#4CAF50', label='Sayur')
    ])
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

    st.markdown("#### 🏆 Top 5 Item Paling Berisiko Waste")
    top5 = (
        avg_sisa_item.head(5)[['nama_item', 'jenis_item', 'sisa_hari']]
        .rename(columns={
            'nama_item' : 'Nama Item',
            'jenis_item': 'Jenis',
            'sisa_hari' : 'Rata-rata Sisa Hari'
        })
        .set_index('Nama Item')
    )
    st.dataframe(top5, use_container_width=True)

    st.markdown("---")

    # ── 4. Tren Sisa Hari vs Hari Sejak Pembelian ─────────────────────────────
    if 'hari_sejak_pembelian' not in df.columns:
        return

    st.markdown("### 4. Tren Sisa Hari vs Hari Sejak Pembelian per Lokasi Penyimpanan")

    lokasi_list = df['lokasi_penyimpanan'].unique()
    n_loc       = len(lokasi_list)

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
