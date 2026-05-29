import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

def render(df):
    st.markdown("## Analisis Masa Simpan & Kesegaran")

    required_cols = ['hari_sejak_pembelian', 'label', 'sisa_hari']
    missing_cols  = [c for c in required_cols if c not in df.columns]

    if missing_cols:
        st.error(f"Kolom berikut tidak ditemukan: **{', '.join(missing_cols)}**")
        st.write("Kolom yang tersedia:", list(df.columns))
        return 

    st.markdown("### 1. Rata-rata hari_sejak_pembelian per Kategori Barang")

    avg_days = (
        df.groupby('jenis_item')['hari_sejak_pembelian']
        .agg(['mean', 'median', 'std']).round(2)
    )
    st.dataframe(avg_days, use_container_width=True)

    fig, axes = plt.subplots(1, 2, figsize=(13, 5))
    colors_bar = ['#4CAF50', '#FF7043'][:len(avg_days)]

    avg_days['mean'].plot(
        kind='bar', ax=axes[0], color=colors_bar, edgecolor='white', width=0.5
    )
    axes[0].set(title='Rata-rata Hari Sejak Pembelian', xlabel='Jenis Item', ylabel='Rata-rata Hari')
    axes[0].tick_params(axis='x', rotation=0)
    for p in axes[0].patches:
        axes[0].annotate(
            f'{p.get_height():.2f}',
            (p.get_x() + p.get_width() / 2, p.get_height()),
            ha='center', va='bottom', fontweight='bold'
        )

    sns.boxplot(
        data=df, x='jenis_item', y='hari_sejak_pembelian',
        ax=axes[1], palette=colors_bar[:len(df['jenis_item'].unique())]
    )
    axes[1].set(title='Distribusi Hari Sejak Pembelian', xlabel='Jenis Item', ylabel='Hari Sejak Pembelian')

    plt.suptitle('Analisis Hari Sejak Pembelian', fontsize=14, fontweight='bold')
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

    c1, c2 = st.columns(2)
    with c1:
        buah_val = f"{avg_days.loc['Buah', 'mean']:.2f}" if 'Buah' in avg_days.index else 'N/A'
        st.info(f"**Buah:** rata-rata {buah_val} hari sejak pembelian")
    with c2:
        sayur_val = f"{avg_days.loc['Sayur', 'mean']:.2f}" if 'Sayur' in avg_days.index else 'N/A'
        st.info(f"**Sayur:** rata-rata {sayur_val} hari sejak pembelian")

    st.markdown("---")
    st.markdown("### 2. Distribusi Label Kondisi per Jenis Item & Lokasi Penyimpanan")

    label_dist = (
        df.groupby(['jenis_item', 'label'])
        .size().unstack(fill_value=0)
    )
    st.dataframe(label_dist, use_container_width=True)

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    label_dist.plot(kind='bar', stacked=True, ax=axes[0], edgecolor='white', width=0.6)
    axes[0].set(title='Distribusi Label Kondisi per Jenis Item', xlabel='Jenis Item', ylabel='Jumlah')
    axes[0].tick_params(axis='x', rotation=0)
    axes[0].legend(title='Label', bbox_to_anchor=(1.01, 1), loc='upper left')
    for container in axes[0].containers:
        axes[0].bar_label(container, label_type='center', fontsize=9)

    label_storage = (
        df.groupby(['lokasi_penyimpanan', 'label'])
        .size().unstack(fill_value=0)
    )
    label_storage.plot(kind='bar', stacked=True, ax=axes[1], edgecolor='white', width=0.6)
    axes[1].set(title='Distribusi Label Kondisi per Lokasi Penyimpanan', xlabel='Lokasi Penyimpanan', ylabel='Jumlah')
    axes[1].tick_params(axis='x', rotation=15)
    axes[1].legend(title='Label', bbox_to_anchor=(1.01, 1), loc='upper left')
    for container in axes[1].containers:
        axes[1].bar_label(container, label_type='center', fontsize=9)

    plt.suptitle('Analisis Label Kondisi Item', fontsize=14, fontweight='bold')
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

    st.markdown("#### Insight Label Kondisi:")
    for item_type in label_dist.index:
        top_label = label_dist.loc[item_type].idxmax()
        top_pct   = label_dist.loc[item_type, top_label] / label_dist.loc[item_type].sum() * 100
        st.text(f"{item_type}: Sebagian besar item ({top_pct:.1f}%) berada dalam kondisi {top_label}.")

    st.markdown("---")

    st.markdown("### 3. Persentase Buah Berdasarkan Kategori Kematangan (Sisa Hari)")

    if 'Buah' not in df['jenis_item'].values:
        st.warning("Tidak ada data Buah dalam filter yang dipilih.")
        return

    df_buah          = df[df['jenis_item'] == 'Buah'].copy()
    kategori_count   = df_buah['kategori_buah'].value_counts()
    kategori_percent = df_buah['kategori_buah'].value_counts(normalize=True) * 100

    result_df = pd.DataFrame({
        'Jumlah'          : kategori_count,
        'Persentase (%)'  : kategori_percent.round(2)
    })
    st.dataframe(result_df, use_container_width=True)

    colors_pie_map = {
        'Busuk'         : '#FF6B6B',
        'Terlalu Matang': '#FFA94D',
        'Matang'        : '#51CF66',
        'Mentah'        : '#4DABF7',
        'Lainnya'       : '#CED4DA',
    }
    pie_colors = [colors_pie_map.get(l, '#CED4DA') for l in kategori_count.index]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    ax1.pie(
        kategori_count, labels=kategori_count.index, autopct='%1.1f%%',
        colors=pie_colors, startangle=90,
        explode=[0.05] * len(kategori_count)
    )
    ax1.set_title('Persentase Kategori Buah Berdasarkan Sisa Hari', fontsize=12, fontweight='bold')

    kategori_count.plot(kind='bar', ax=ax2, color=pie_colors, edgecolor='white', width=0.5)
    ax2.set(title='Jumlah Buah per Kategori', xlabel='Kategori', ylabel='Jumlah')
    ax2.tick_params(axis='x', rotation=0)
    for p in ax2.patches:
        ax2.annotate(
            f'{int(p.get_height())}',
            (p.get_x() + p.get_width() / 2, p.get_height()),
            ha='center', va='bottom', fontweight='bold'
        )

    plt.suptitle('Analisis Kematangan Buah', fontsize=14, fontweight='bold')
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()
