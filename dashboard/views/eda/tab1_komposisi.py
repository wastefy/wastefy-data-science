import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

def render(df):
    st.markdown("## Komposisi & Distribusi Inventory")
    st.info(f"Menampilkan data dari **{len(df):,}** baris | **{df['nama_item'].nunique()}** item unik")

    st.markdown("### 1. Jenis Item yang Mendominasi Inventori")
    counts = df['jenis_item'].value_counts()

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    counts.plot(
        kind='bar', ax=axes[0],
        color=['#4CAF50', '#FF7043'][:len(counts)],
        edgecolor='white', width=0.5
    )
    axes[0].set(title='Distribusi Jenis Item', xlabel='Jenis Item', ylabel='Jumlah Baris')
    axes[0].tick_params(axis='x', rotation=0)
    for p in axes[0].patches:
        axes[0].annotate(
            f'{int(p.get_height()):,}',
            (p.get_x() + p.get_width() / 2, p.get_height()),
            ha='center', va='bottom', fontweight='bold'
        )
    axes[1].pie(
        counts, labels=counts.index, autopct='%1.1f%%',
        startangle=90, colors=['#4CAF50', '#FF7043'][:len(counts)]
    )
    axes[1].set_title('Proporsi Jenis Item')
    plt.suptitle('Komposisi Inventori — Jenis Item', fontsize=14, fontweight='bold')
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

    st.markdown("### 2. Distribusi Barang Berdasarkan Lokasi Penyimpanan")
    storage_counts = df['lokasi_penyimpanan'].value_counts()

    fig, axes = plt.subplots(1, 2, figsize=(10, 5))
    storage_counts.plot(
        kind='bar', ax=axes[0],
        color=sns.color_palette('Set2', len(storage_counts)),
        edgecolor='white', width=0.5
    )
    axes[0].set(
        title='Jumlah Barang per Lokasi Penyimpanan',
        xlabel='Lokasi Penyimpanan', ylabel='Jumlah Barang'
    )
    axes[0].tick_params(axis='x', rotation=15)
    for p in axes[0].patches:
        axes[0].annotate(
            f'{int(p.get_height()):,}',
            (p.get_x() + p.get_width() / 2, p.get_height()),
            ha='center', va='bottom', fontweight='bold'
        )
    axes[1].pie(
        storage_counts, labels=storage_counts.index, autopct='%1.1f%%',
        startangle=90, colors=sns.color_palette('Set2', len(storage_counts))
    )
    axes[1].set_title('Proporsi Lokasi Penyimpanan')
    plt.suptitle('Distribusi Lokasi Penyimpanan', fontsize=14, fontweight='bold')
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

    st.markdown("### 3. Jumlah Item Unik per Kategori")
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    unique_items = (
        df.groupby('jenis_item')['nama_item']
        .nunique().sort_values(ascending=False)
    )
    unique_items.plot(
        kind='bar', ax=axes[0, 0],
        color=['#4CAF50', '#FF7043'][:len(unique_items)],
        edgecolor='white', width=0.5
    )
    axes[0, 0].set(title='Jumlah Item Unik per Kategori', xlabel='Jenis Item', ylabel='Jumlah Item Unik')
    axes[0, 0].tick_params(axis='x', rotation=0)
    for p in axes[0, 0].patches:
        axes[0, 0].annotate(
            str(int(p.get_height())),
            (p.get_x() + p.get_width() / 2, p.get_height()),
            ha='center', va='bottom', fontweight='bold'
        )

    all_counts = df['nama_item'].value_counts()
    all_counts.plot(kind='bar', ax=axes[0, 1], edgecolor='white', color='#66BB6A')
    axes[0, 1].set(title='Frekuensi Semua Item', xlabel='Nama Item', ylabel='Jumlah')
    axes[0, 1].tick_params(axis='x', rotation=45)

    if 'Buah' in df['jenis_item'].values:
        buah_counts = df[df['jenis_item'] == 'Buah']['nama_item'].value_counts()
        buah_counts.plot(kind='bar', ax=axes[1, 0], color='#FF7043', edgecolor='white')
        axes[1, 0].set(title='Distribusi Jenis Buah', xlabel='Nama Buah', ylabel='Jumlah')
        axes[1, 0].tick_params(axis='x', rotation=30)
    else:
        axes[1, 0].text(0.5, 0.5, 'Tidak ada data Buah',
                        ha='center', va='center', transform=axes[1, 0].transAxes)
        axes[1, 0].set_title('Distribusi Jenis Buah')

    if 'Sayur' in df['jenis_item'].values:
        sayur_counts = df[df['jenis_item'] == 'Sayur']['nama_item'].value_counts()
        sayur_counts.plot(kind='bar', ax=axes[1, 1], color='#4CAF50', edgecolor='white')
        axes[1, 1].set(title='Distribusi Jenis Sayur', xlabel='Nama Sayur', ylabel='Jumlah')
        axes[1, 1].tick_params(axis='x', rotation=30)
    else:
        axes[1, 1].text(0.5, 0.5, 'Tidak ada data Sayur',
                        ha='center', va='center', transform=axes[1, 1].transAxes)
        axes[1, 1].set_title('Distribusi Jenis Sayur')

    plt.suptitle('Komposisi Item dalam Inventori', fontsize=14, fontweight='bold')
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

    st.markdown("### Ringkasan Statistik")
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("Total Item", f"{len(df):,}")
    with c2:
        st.metric("Kategori", f"{df['jenis_item'].nunique()}")
    with c3:
        st.metric("Item Unik", f"{df['nama_item'].nunique():,}")
    with c4:
        st.metric("Lokasi", f"{df['lokasi_penyimpanan'].nunique()}")
