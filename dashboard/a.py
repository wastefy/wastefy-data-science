from PIL import Image
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

# Load logo
try:
    logo = Image.open("./logo/logo_wastefy.png")
    has_logo = True
except Exception:
    has_logo = False

# Page configuration
st.set_page_config(
    page_title="Wastefy Data Dashboard",
    page_icon="📊",
    layout="wide"
)

# Custom CSS
st.markdown("""
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
""", unsafe_allow_html=True)


@st.cache_data
def load_data():
    df = pd.read_csv('../dataset/sayur_buah_bersih.csv')

    if 'hari_sejak_pembelian' in df.columns:
        df['hari_sejak_pembelian'] = (
            df.groupby('jenis_item')['hari_sejak_pembelian']
            .transform(lambda x: x.fillna(x.median()))
        )
    if 'sisa_hari' in df.columns:
        def _kategori(sisa_hari):
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
        df['kategori_buah'] = df['sisa_hari'].apply(_kategori)

    return df


df_clean = load_data()

# Sidebar
with st.sidebar:
    col1, col2 = st.columns([1, 3], vertical_alignment="center")
    with col1:
        if has_logo:
            st.image(logo, width=50)
        else:
            st.markdown("🌿")
    with col2:
        st.markdown("### Wastefy Data Dashboard")

    st.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)
    st.info("📊 Dashboard ini berfungsi untuk menampilkan hasil EDA dan simulasi model yang dibuat oleh tim AI")
    st.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)

    st.markdown("### Navigasi")
    page = st.radio(
        "Pilih Halaman",
        options=["Analisis Data (EDA)", "Fitur AI"],
        label_visibility="collapsed"
    )

    st.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)
    st.markdown("### Filter Data")

    kategori = st.selectbox(
        "Pilih Kategori",
        options=["Semua"] + sorted(df_clean['jenis_item'].unique().tolist()),
        help="Filter berdasarkan jenis produk"
    )

    lokasi_options = ["Semua"] + sorted(df_clean['lokasi_penyimpanan'].unique().tolist())
    jenis_katering = st.selectbox(
        "Pilih Lokasi Penyimpanan",
        options=lokasi_options,
        help="Filter berdasarkan lokasi penyimpanan"
    )

    if st.button("Reset Filter", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

    st.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)
    st.caption("© 2024 Wastefy AI Team")
    st.caption("Version 1.0.0")

def apply_filters(df):
    df_f = df.copy()
    if kategori != "Semua":
        df_f = df_f[df_f['jenis_item'] == kategori]
    if jenis_katering != "Semua":
        df_f = df_f[df_f['lokasi_penyimpanan'] == jenis_katering]
    return df_f


df_filtered = apply_filters(df_clean)

st.markdown(f'<div class="main-header">{page}</div>', unsafe_allow_html=True)


if page == "Analisis Data (EDA)":

    tab1, tab2, tab3, tab4 = st.tabs([
        "Komposisi & Distribusi Inventory",
        "Analisis Masa Simpan & Kesegaran",
        "Analisis Efektivitas Penyimpanan",
        "Food Waste Risk Analysis"
    ])

    # ── TAB 1: Komposisi & Distribusi Inventory ──────────────────────────────
    with tab1:
        st.markdown("##Komposisi & Distribusi Inventory")
        st.info(f"Menampilkan data dari **{len(df_filtered):,}** baris | **{df_filtered['nama_item'].nunique()}** item unik")

        # 1. Jenis Item
        st.markdown("### 1. Jenis Item yang Mendominasi Inventori")
        counts = df_filtered['jenis_item'].value_counts()

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

        # 2. Lokasi Penyimpanan
        st.markdown("### 2. Distribusi Barang Berdasarkan Lokasi Penyimpanan")
        storage_counts = df_filtered['lokasi_penyimpanan'].value_counts()

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

        # 3. Item Unik per Kategori
        st.markdown("### 3. Jumlah Item Unik per Kategori")
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))

        unique_items = (
            df_filtered.groupby('jenis_item')['nama_item']
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

        all_counts = df_filtered['nama_item'].value_counts()
        all_counts.plot(kind='bar', ax=axes[0, 1], edgecolor='white', color='#66BB6A')
        axes[0, 1].set(title='Frekuensi Semua Item', xlabel='Nama Item', ylabel='Jumlah')
        axes[0, 1].tick_params(axis='x', rotation=45)

        if 'Buah' in df_filtered['jenis_item'].values:
            buah_counts = (
                df_filtered[df_filtered['jenis_item'] == 'Buah']['nama_item'].value_counts()
            )
            buah_counts.plot(kind='bar', ax=axes[1, 0], color='#FF7043', edgecolor='white')
            axes[1, 0].set(title='Distribusi Jenis Buah', xlabel='Nama Buah', ylabel='Jumlah')
            axes[1, 0].tick_params(axis='x', rotation=30)
        else:
            axes[1, 0].text(0.5, 0.5, 'Tidak ada data Buah', ha='center', va='center', transform=axes[1, 0].transAxes)
            axes[1, 0].set_title('Distribusi Jenis Buah')

        if 'Sayur' in df_filtered['jenis_item'].values:
            sayur_counts = (
                df_filtered[df_filtered['jenis_item'] == 'Sayur']['nama_item'].value_counts()
            )
            sayur_counts.plot(kind='bar', ax=axes[1, 1], color='#4CAF50', edgecolor='white')
            axes[1, 1].set(title='Distribusi Jenis Sayur', xlabel='Nama Sayur', ylabel='Jumlah')
            axes[1, 1].tick_params(axis='x', rotation=30)
        else:
            axes[1, 1].text(0.5, 0.5, 'Tidak ada data Sayur', ha='center', va='center', transform=axes[1, 1].transAxes)
            axes[1, 1].set_title('Distribusi Jenis Sayur')

        plt.suptitle('Komposisi Item dalam Inventori', fontsize=14, fontweight='bold')
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()

        # Ringkasan Statistik
        st.markdown("### 📊 Ringkasan Statistik")
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.metric("Total Item", f"{len(df_filtered):,}")
        with c2:
            st.metric("Item Unik", f"{df_filtered['nama_item'].nunique():,}")
        with c3:
            st.metric("Kategori", f"{df_filtered['jenis_item'].nunique()}")
        with c4:
            st.metric("Lokasi", f"{df_filtered['lokasi_penyimpanan'].nunique()}")

    # ── TAB 2: Analisis Masa Simpan & Kesegaran ───────────────────────────────
    with tab2:
        st.markdown("## 🌿 Analisis Masa Simpan & Kesegaran")

        required_cols = ['hari_sejak_pembelian', 'label', 'sisa_hari']
        missing_cols = [c for c in required_cols if c not in df_filtered.columns]

        if missing_cols:
            st.error(f"⚠️ Kolom berikut tidak ditemukan: **{', '.join(missing_cols)}**")
            st.write("Kolom yang tersedia:", list(df_filtered.columns))
        else:
            # 1. Rata-rata hari_sejak_pembelian
            st.markdown("### 1. Rata-rata `hari_sejak_pembelian` per Kategori Barang")

            avg_days = (
                df_filtered.groupby('jenis_item')['hari_sejak_pembelian']
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
                data=df_filtered, x='jenis_item', y='hari_sejak_pembelian',
                ax=axes[1], palette=colors_bar[:len(df_filtered['jenis_item'].unique())]
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

            # 2. Distribusi Label Kondisi
            st.markdown("### 2. Distribusi Label Kondisi per Jenis Item & Lokasi Penyimpanan")

            label_dist = (
                df_filtered.groupby(['jenis_item', 'label'])
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
                df_filtered.groupby(['lokasi_penyimpanan', 'label'])
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

            st.markdown("#### 💡 Insight Label Kondisi")
            for item_type in label_dist.index:
                top_label = label_dist.loc[item_type].idxmax()
                top_pct = label_dist.loc[item_type, top_label] / label_dist.loc[item_type].sum() * 100
                st.info(f"**{item_type}:** Sebagian besar item ({top_pct:.1f}%) berada dalam kondisi **{top_label}**.")

            st.markdown("---")

            # 3. Persentase Kategori Buah Berdasarkan Sisa Hari
            st.markdown("### 3. Persentase Buah Berdasarkan Kategori Kematangan (Sisa Hari)")

            if 'Buah' in df_filtered['jenis_item'].values:
                df_buah = df_filtered[df_filtered['jenis_item'] == 'Buah'].copy()
                kategori_count = df_buah['kategori_buah'].value_counts()
                kategori_percent = df_buah['kategori_buah'].value_counts(normalize=True) * 100

                result_df = pd.DataFrame({
                    'Jumlah': kategori_count,
                    'Persentase (%)': kategori_percent.round(2)
                })
                st.dataframe(result_df, use_container_width=True)

                colors_pie_map = {
                    'Busuk': '#FF6B6B', 'Terlalu Matang': '#FFA94D',
                    'Matang': '#51CF66', 'Mentah': '#4DABF7', 'Lainnya': '#CED4DA'
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

    # ── TAB 3: Analisis Efektivitas Penyimpanan ───────────────────────────────
    with tab3:
        st.markdown("## 🏪 Analisis Efektivitas Penyimpanan")

        if 'sisa_hari' not in df_filtered.columns:
            st.error("⚠️ Kolom `sisa_hari` tidak ditemukan dalam dataset.")
        else:
            # 1. Lokasi paling efektif
            st.markdown("### 1. Lokasi Penyimpanan yang Paling Efektif Menjaga Sisa Umur Simpan")

            storage_stats = (
                df_filtered.groupby('lokasi_penyimpanan')['sisa_hari']
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
            ax.set_title('Rata-rata Sisa Hari per Lokasi Penyimpanan')
            ax.set_xlabel('Lokasi Penyimpanan')
            ax.set_ylabel('Rata-rata Sisa Hari')
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
                f"✅ **{best_loc}** memiliki rata-rata sisa hari tertinggi "
                f"({storage_stats.loc[best_loc, 'mean']:.1f} hari) — lokasi paling efektif menjaga kesegaran."
            )

            st.markdown("---")

            # 2. Boxplot + ANOVA
            st.markdown("### 2. Perbedaan Signifikan Sisa Hari Antar Lokasi Penyimpanan")

            fig, ax = plt.subplots(figsize=(10, 5))
            sns.boxplot(data=df_filtered, x='lokasi_penyimpanan', y='sisa_hari', palette='Set2', ax=ax)
            ax.set_title('Distribusi Sisa Hari per Lokasi Penyimpanan')
            ax.set_xlabel('Lokasi Penyimpanan')
            ax.set_ylabel('Sisa Hari')
            ax.tick_params(axis='x', rotation=15)
            plt.tight_layout()
            st.pyplot(fig)
            plt.close()

            groups = [
                grp['sisa_hari'].values
                for _, grp in df_filtered.groupby('lokasi_penyimpanan')
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
                    st.success("✅ Terdapat perbedaan signifikan sisa hari antar lokasi penyimpanan (p < 0.05).")
                else:
                    st.info("ℹ️ Tidak terdapat perbedaan signifikan antar lokasi penyimpanan (p ≥ 0.05).")

            st.markdown("---")

            # 3. Crosstab heatmap
            st.markdown("### 3. Distribusi Jenis Item di Setiap Lokasi Penyimpanan")

            cross_tab = pd.crosstab(df_filtered['jenis_item'], df_filtered['lokasi_penyimpanan'])
            fig, ax = plt.subplots(figsize=(8, 5))
            sns.heatmap(cross_tab, annot=True, fmt='d', cmap='Blues', linewidths=0.5, ax=ax)
            ax.set_title('Jumlah Item: Jenis vs Lokasi Penyimpanan')
            ax.set_xlabel('Lokasi Penyimpanan')
            ax.set_ylabel('Jenis Item')
            plt.tight_layout()
            st.pyplot(fig)
            plt.close()

            st.markdown("---")

            # 4. Pivot rata-rata sisa hari
            st.markdown("### 4. Kombinasi Jenis Item & Lokasi yang Tampak Tidak Sesuai")

            pivot = df_filtered.pivot_table(
                values='sisa_hari', index='jenis_item',
                columns='lokasi_penyimpanan', aggfunc='mean'
            )
            fig, ax = plt.subplots(figsize=(8, 5))
            sns.heatmap(pivot, annot=True, fmt='.1f', cmap='RdYlGn', linewidths=0.5, ax=ax)
            ax.set_title('Rata-rata Sisa Hari: Jenis vs Lokasi')
            ax.set_xlabel('Lokasi Penyimpanan')
            ax.set_ylabel('Jenis Item')
            plt.tight_layout()
            st.pyplot(fig)
            plt.close()

            st.markdown("""
            #### 💡 Cara membaca heatmap:
            - 🟢 **Hijau** = rata-rata sisa hari tinggi → penyimpanan efektif
            - 🔴 **Merah** = rata-rata sisa hari rendah → potensi mismatch lokasi atau item memang cepat habis
            """)

            st.markdown("---")

            # 5. Tren sisa hari vs hari sejak pembelian
            if 'hari_sejak_pembelian' in df_filtered.columns:
                st.markdown("### 5. Tren Sisa Hari vs Hari Sejak Pembelian per Lokasi Penyimpanan")

                lokasi_list = df_filtered['lokasi_penyimpanan'].unique()
                n_loc = len(lokasi_list)
                fig, axes = plt.subplots(1, n_loc, figsize=(6 * n_loc, 5), sharey=True)
                if n_loc == 1:
                    axes = [axes]

                for ax, loc in zip(axes, lokasi_list):
                    group = df_filtered[df_filtered['lokasi_penyimpanan'] == loc]
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

    # ── TAB 4: Food Waste Risk Analysis ──────────────────────────────────────
    with tab4:
        st.markdown("## 🚨 Food Waste Risk Analysis")

        if 'sisa_hari' not in df_filtered.columns or 'label' not in df_filtered.columns:
            st.error("⚠️ Kolom `sisa_hari` atau `label` tidak ditemukan.")
        else:
            # 1. Distribusi label keseluruhan
            st.markdown("### 1. Distribusi Barang Berdasarkan Kondisi Kesegaran")

            label_counts = df_filtered['label'].value_counts()
            colors_label = ['#66BB6A', '#FFA726', '#EF5350', '#42A5F5', '#AB47BC']

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
                st.metric("🔴 Busuk", f"{busuk_n:,}", delta=f"{busuk_n/len(df_filtered)*100:.1f}%", delta_color="inverse")
            with c2:
                segar_n = label_counts.get('Segar', 0)
                st.metric("🟢 Segar", f"{segar_n:,}", delta=f"{segar_n/len(df_filtered)*100:.1f}%")
            with c3:
                kritis_n = int((df_filtered['sisa_hari'] < 3).sum())
                st.metric("⚠️ Kritis (< 3 hari)", f"{kritis_n:,}", delta=f"{kritis_n/len(df_filtered)*100:.1f}%", delta_color="inverse")

            st.markdown("---")

            # 2. Kombinasi berisiko
            st.markdown("### 2. Kombinasi Jenis Item & Lokasi Penyimpanan Paling Berisiko Food Waste")

            critical_df = df_filtered[df_filtered['sisa_hari'] < 3]
            if len(critical_df) > 0:
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
                ax.set_title('Heatmap Risiko Food Waste (Jumlah Item dengan Sisa < 3 Hari)', fontweight='bold')
                ax.set_xlabel('Lokasi Penyimpanan')
                ax.set_ylabel('Jenis Item')
                plt.tight_layout()
                st.pyplot(fig)
                plt.close()

                top_risk = risk_combo.iloc[0]
                st.error(
                    f"🚨 Kombinasi paling berisiko: **{top_risk['jenis_item']}** di "
                    f"**{top_risk['lokasi_penyimpanan']}** dengan **{int(top_risk['jumlah_kritis'])}** item kritis."
                )
            else:
                st.success("✅ Tidak ada item dengan sisa hari < 3 hari dalam data yang difilter.")

            st.markdown("---")

            # 3. Item rata-rata sisa hari paling rendah
            st.markdown("### 3. Item dengan Rata-rata Sisa Hari Paling Rendah")

            avg_sisa_item = (
                df_filtered.groupby(['nama_item', 'jenis_item'])['sisa_hari']
                .mean().reset_index().sort_values('sisa_hari')
            )

            fig, ax = plt.subplots(figsize=(12, 5))
            bar_colors = ['#FF7043' if t == 'Buah' else '#4CAF50' for t in avg_sisa_item['jenis_item']]
            bars = ax.bar(avg_sisa_item['nama_item'], avg_sisa_item['sisa_hari'],
                          color=bar_colors, edgecolor='white')
            ax.set_title('Rata-rata Sisa Hari per Item', fontweight='bold')
            ax.set_xlabel('Nama Item')
            ax.set_ylabel('Rata-rata Sisa Hari')
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
                .rename(columns={'nama_item': 'Nama Item', 'jenis_item': 'Jenis', 'sisa_hari': 'Rata-rata Sisa Hari'})
                .set_index('Nama Item')
            )
            st.dataframe(top5, use_container_width=True)

            st.markdown("---")

            # 4. Tren sisa hari per lokasi
            if 'hari_sejak_pembelian' in df_filtered.columns:
                st.markdown("### 4. Tren Sisa Hari vs Hari Sejak Pembelian per Lokasi Penyimpanan")

                lokasi_list = df_filtered['lokasi_penyimpanan'].unique()
                n_loc = len(lokasi_list)
                fig, axes = plt.subplots(1, n_loc, figsize=(6 * n_loc, 5), sharey=True)
                if n_loc == 1:
                    axes = [axes]

                for ax, loc in zip(axes, lokasi_list):
                    group = df_filtered[df_filtered['lokasi_penyimpanan'] == loc]
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


else:
    st.markdown("### 🤖 AI Smart-Scan: Deteksi Waste Makanan")
    st.info("💡 Fitur AI Smart-Scan akan segera hadir! Gunakan kamera untuk mendeteksi dan mengidentifikasi waste makanan.")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### 📸 Upload Gambar")
        uploaded_file = st.file_uploader(
            "Upload gambar produk sayur/buah",
            type=['jpg', 'jpeg', 'png'],
            help="Upload gambar untuk dikenali oleh AI"
        )
        if uploaded_file is not None:
            st.image(uploaded_file, caption="Gambar yang diupload", width=300)
            st.success("✅ AI akan menganalisis gambar ini...")

    with col2:
        st.markdown("#### 🎯 Hasil Deteksi")
        st.markdown("""
        **Fitur yang akan tersedia:**
        - Identifikasi jenis sayur/buah
        - Deteksi tingkat kematangan
        - Prediksi umur simpan
        - Rekomendasi penyimpanan
        """)
        if uploaded_file is not None:
            st.markdown("---")
            st.markdown("**Hasil Analisis Sementara:**")
            st.metric("Status", "Menunggu analisis...")

    st.markdown("---")
    st.markdown("#### 📊 Statistik Smart-Scan")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("Total Scan", "0", "Mulai gunakan")
    with c2:
        st.metric("Akurasi Model", "95%")
    with c3:
        st.metric("Waste Terdeteksi", "0 kg", "Belum ada data")

# Footer
st.markdown("---")
st.caption("💡 Tips: Gunakan filter di sidebar untuk melihat data yang lebih spesifik")