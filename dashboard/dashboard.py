import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
import warnings

warnings.filterwarnings('ignore')

st.set_page_config(
    page_title="Dashboard Inventori Sayur & Buah",
    page_icon="🌱",
    layout="wide"
)

@st.cache_data
def load_data():
    df = pd.read_csv('../dataset/sayur_buah_bersih.csv')
    df['hari_sejak_pembelian'] = (
        df.groupby('jenis_item')['hari_sejak_pembelian']
        .transform(lambda x: x.fillna(x.median()))
    )
    return df

df_clean = load_data()

warna_item = {'Buah': '#FF7043', 'Sayur': '#4CAF50'}

# Custom styling for better appearance
st.markdown("""
    <style>
    /* Style untuk metric cards */
    div[data-testid="stMetricValue"] {
        color: #1f1f1f !important;
        font-weight: bold !important;
    }
    
    div[data-testid="stMetricLabel"] {
        color: #333333 !important;
        font-weight: 500 !important;
    }
    
    div[data-testid="stMetricDelta"] {
        color: #666666 !important;
    }
    
    /* Background untuk metric container */
    div[data-testid="stMetric"] {
        background-color: #f8f9fa !important;
        padding: 15px !important;
        border-radius: 10px !important;
        border: 1px solid #e0e0e0 !important;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1) !important;
    }
    
    /* Hover effect */
    div[data-testid="stMetric"]:hover {
        background-color: #ffffff !important;
        box-shadow: 0 2px 5px rgba(0,0,0,0.15) !important;
        transition: all 0.3s ease !important;
    }
    </style>
""", unsafe_allow_html=True)

st.title("Dashboard Inventori & Kesegaran Sayur Buah")
st.markdown("Visualisasi komposisi inventori, lokasi penyimpanan, dan analisis masa simpan item.")

# Metrics Row
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Inventori", f"{df_clean.shape[0]} Item")
with col2:
    st.metric("Total Jenis Item", df_clean['nama_item'].nunique())

st.divider()

# SECTION 1: Komposisi dan Distribusi Inventori
st.header("1. Komposisi dan Distribusi Inventori")

tab1, tab2, tab3 = st.tabs(["📊 Distribusi Jenis Item", "📍 Lokasi Penyimpanan", "🥬 Komposisi Item"])

# Tab 1: Distribusi Jenis Item
with tab1:
    col_a, col_b = st.columns([1, 1])
    
    with col_a:
        st.subheader("Distribusi Jenis Item")
        counts = df_clean['jenis_item'].value_counts()
        
        fig1, ax1 = plt.subplots(figsize=(5, 4))
        bars = ax1.bar(
            counts.index,
            counts.values,
            color=['#66BB6A', '#FF8A65'],
            width=0.4,
            edgecolor='white',
            linewidth=2
        )
        
        ax1.set_ylabel('Jumlah', fontsize=10)
        ax1.spines['top'].set_visible(False)
        ax1.spines['right'].set_visible(False)
        ax1.grid(axis='y', linestyle='--', alpha=0.3)
        
        for bar in bars:
            h = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2, h + 20, f'{h:,}', 
                    ha='center', fontsize=10, fontweight='bold')
        
        st.pyplot(fig1)
        plt.close(fig1)
    
    with col_b:
        st.subheader("Proporsi Jenis Item")
        fig2, ax2 = plt.subplots(figsize=(5, 4))
        wedges, texts, autotexts = ax2.pie(
            counts,
            labels=counts.index,
            autopct='%1.1f%%',
            startangle=90,
            colors=['#66BB6A', '#FF8A65'],
            wedgeprops={'edgecolor': 'white', 'linewidth': 2}
        )
        
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
            autotext.set_fontsize(10)
        
        st.pyplot(fig2)
        plt.close(fig2)

# Tab 2: Lokasi Penyimpanan
with tab2:
    col_a, col_b = st.columns([1, 1])
    
    with col_a:
        st.subheader("Distribusi Lokasi Penyimpanan")
        storage_counts = df_clean['lokasi_penyimpanan'].value_counts()
        
        fig3, ax3 = plt.subplots(figsize=(5, 4))
        bars = ax3.bar(
            storage_counts.index,
            storage_counts.values,
            color=sns.color_palette('Set2', 3),
            edgecolor='white',
            linewidth=2,
            width=0.4
        )
        
        ax3.set_ylabel('Jumlah', fontsize=10)
        ax3.tick_params(axis='x', rotation=10, labelsize=9)
        ax3.spines['top'].set_visible(False)
        ax3.spines['right'].set_visible(False)
        ax3.grid(axis='y', linestyle='--', alpha=0.3)
        
        for bar in bars:
            h = bar.get_height()
            ax3.text(bar.get_x() + bar.get_width()/2, h + 10, f'{int(h):,}', 
                    ha='center', fontsize=9, fontweight='bold')
        
        st.pyplot(fig3)
        plt.close(fig3)
    
    with col_b:
        st.subheader("Proporsi Lokasi")
        fig4, ax4 = plt.subplots(figsize=(5, 4))
        wedges, texts, autotexts = ax4.pie(
            storage_counts,
            labels=storage_counts.index,
            autopct='%1.1f%%',
            startangle=90,
            colors=sns.color_palette('Set2', 3),
            wedgeprops={'edgecolor': 'white', 'linewidth': 2}
        )
        
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
            autotext.set_fontsize(10)
        
        st.pyplot(fig4)
        plt.close(fig4)

# Tab 3: Komposisi Item
with tab3:
    # Row 1: Item Unik dan Top 10
    col_a, col_b = st.columns([1, 1])
    
    with col_a:
        st.subheader("Item Unik per Kategori")
        unique_items = df_clean.groupby('jenis_item')['nama_item'].nunique().sort_values(ascending=False)
        
        fig5, ax5 = plt.subplots(figsize=(4, 3))
        bars = ax5.bar(
            unique_items.index,
            unique_items.values,
            color=['#66BB6A', '#FF8A65'],
            width=0.4,
            edgecolor='white',
            linewidth=2
        )
        
        ax5.set_ylabel('Jumlah', fontsize=9)
        ax5.spines['top'].set_visible(False)
        ax5.spines['right'].set_visible(False)
        ax5.grid(axis='y', linestyle='--', alpha=0.3)
        
        for bar in bars:
            h = bar.get_height()
            ax5.text(bar.get_x() + bar.get_width()/2, h + 0.3, f'{int(h)}', 
                    ha='center', fontsize=9, fontweight='bold')
        
        st.pyplot(fig5)
        plt.close(fig5)
    
    with col_b:
        st.subheader("Top 10 Item Terbanyak")
        top_items = df_clean['nama_item'].value_counts().head(10)
        
        fig6, ax6 = plt.subplots(figsize=(4, 3))
        bars = ax6.barh(range(len(top_items)), top_items.values, color='#5C9DF5')
        ax6.set_yticks(range(len(top_items)))
        ax6.set_yticklabels(top_items.index, fontsize=8)
        ax6.set_xlabel('Jumlah', fontsize=9)
        ax6.spines['top'].set_visible(False)
        ax6.spines['right'].set_visible(False)
        ax6.grid(axis='x', linestyle='--', alpha=0.3)
        
        for i, (bar, val) in enumerate(zip(bars, top_items.values)):
            ax6.text(val + 5, bar.get_y() + bar.get_height()/2, f'{val}', 
                    va='center', fontsize=8, fontweight='bold')
        
        st.pyplot(fig6)
        plt.close(fig6)
    
    # Row 2: Distribusi Buah dan Sayur
    col_c, col_d = st.columns([1, 1])
    
    with col_c:
        st.subheader("Top 8 Buah")
        buah_counts = df_clean[df_clean['jenis_item'] == 'Buah']['nama_item'].value_counts().head(8)
        
        fig7, ax7 = plt.subplots(figsize=(4, 3))
        bars = ax7.barh(range(len(buah_counts)), buah_counts.values, color='#FF8A65')
        ax7.set_yticks(range(len(buah_counts)))
        ax7.set_yticklabels(buah_counts.index, fontsize=8)
        ax7.set_xlabel('Jumlah', fontsize=9)
        ax7.spines['top'].set_visible(False)
        ax7.spines['right'].set_visible(False)
        ax7.grid(axis='x', linestyle='--', alpha=0.3)
        
        for i, (bar, val) in enumerate(zip(bars, buah_counts.values)):
            ax7.text(val + 2, bar.get_y() + bar.get_height()/2, f'{val}', 
                    va='center', fontsize=8, fontweight='bold')
        
        st.pyplot(fig7)
        plt.close(fig7)
    
    with col_d:
        st.subheader("Top 8 Sayur")
        sayur_counts = df_clean[df_clean['jenis_item'] == 'Sayur']['nama_item'].value_counts().head(8)
        
        fig8, ax8 = plt.subplots(figsize=(4, 3))
        bars = ax8.barh(range(len(sayur_counts)), sayur_counts.values, color='#66BB6A')
        ax8.set_yticks(range(len(sayur_counts)))
        ax8.set_yticklabels(sayur_counts.index, fontsize=8)
        ax8.set_xlabel('Jumlah', fontsize=9)
        ax8.spines['top'].set_visible(False)
        ax8.spines['right'].set_visible(False)
        ax8.grid(axis='x', linestyle='--', alpha=0.3)
        
        for i, (bar, val) in enumerate(zip(bars, sayur_counts.values)):
            ax8.text(val + 2, bar.get_y() + bar.get_height()/2, f'{val}', 
                    va='center', fontsize=8, fontweight='bold')
        
        st.pyplot(fig8)
        plt.close(fig8)

st.divider()

# SECTION 2: Analisis Masa Simpan & Kesegaran
st.header("2. Analisis Masa Simpan & Kesegaran")

# Heatmap and Trend Analysis
col_c, col_d = st.columns([1, 1])

with col_c:
    st.subheader("Rata-rata Sisa Hari per Lokasi")
    heatmap_data = df_clean.pivot_table(
        values='sisa_hari',
        index='jenis_item',
        columns='lokasi_penyimpanan',
        aggfunc='mean'
    )
    
    fig9, ax9 = plt.subplots(figsize=(6, 4))
    sns.heatmap(heatmap_data, annot=True, fmt='.1f', cmap='Blues', 
                linewidths=0.5, ax=ax9, cbar_kws={'label': 'Rata-rata Sisa Hari'})
    ax9.set_title('Rata-rata Sisa Hari: Jenis vs Lokasi', fontsize=11, fontweight='bold')
    ax9.set_xlabel('Lokasi Penyimpanan', fontsize=9)
    ax9.set_ylabel('Jenis Item', fontsize=9)
    st.pyplot(fig9)
    plt.close(fig9)

with col_d:
    st.subheader("Tren Sisa Hari")
    if 'lokasi_penyimpanan' in df_clean.columns:
        lokasi_list = df_clean['lokasi_penyimpanan'].unique()
        pilih_lokasi = st.selectbox("Pilih Lokasi Penyimpanan:", lokasi_list, key="lokasi_trend")
        
        fig10, ax10 = plt.subplots(figsize=(6, 4))
        group = df_clean[df_clean['lokasi_penyimpanan'] == pilih_lokasi]
        
        for item, color in zip(['Buah', 'Sayur'], ['#FF7043', '#4CAF50']):
            trend = group[group['jenis_item'] == item].groupby('hari_sejak_pembelian')['sisa_hari'].mean()
            if not trend.empty:
                ax10.plot(trend.index, trend.values, marker='o', label=item, color=color, linewidth=2, markersize=4)
        
        ax10.set_title(f'Tren Kesegaran di {pilih_lokasi}', fontsize=11, fontweight='bold')
        ax10.set_xlabel('Hari Sejak Pembelian', fontsize=9)
        ax10.set_ylabel('Rata-rata Sisa Hari', fontsize=9)
        ax10.legend(loc='best', fontsize=9)
        ax10.grid(True, alpha=0.3, linestyle='--')
        st.pyplot(fig10)
        plt.close(fig10)

st.divider()

# SECTION 3: Analisis Kategori Kesegaran
st.subheader("Analisis Kategori Kesegaran")

# Function for categorization
def kategori_kesegaran(sisa_hari):
    """Categorize based on remaining days"""
    if sisa_hari <= 0:
        return 'Kadaluarsa'
    elif 1 <= sisa_hari <= 2:
        return 'Busuk'
    elif 3 <= sisa_hari <= 4:
        return 'Hampir Busuk'
    elif 5 <= sisa_hari <= 7:
        return 'Terlalu Matang'
    elif 8 <= sisa_hari <= 14:
        return 'Matang'
    elif 15 <= sisa_hari <= 21:
        return 'Setengah Matang'
    elif 22 <= sisa_hari <= 30:
        return 'Mentah'
    else:
        return 'Sangat Segar'

# Check if required column exists
if 'sisa_hari' in df_clean.columns:
    # Add category column
    df_clean['kategori_kesegaran'] = df_clean['sisa_hari'].apply(kategori_kesegaran)
    
    # Create two columns for metrics and chart
    col_e1, col_e2 = st.columns([1, 1])
    
    with col_e1:
        # Calculate category counts and percentages
        kategori_count = df_clean['kategori_kesegaran'].value_counts()
        kategori_percent = df_clean['kategori_kesegaran'].value_counts(normalize=True) * 100
        
        # Display as dataframe
        kategori_df = pd.DataFrame({
            'Kategori': kategori_count.index,
            'Jumlah': kategori_count.values,
            'Persentase (%)': kategori_percent.round(1).values
        })
        kategori_df = kategori_df.reset_index(drop=True)
        
        st.dataframe(kategori_df, use_container_width=True, hide_index=True)
    
    with col_e2:
        # Create pie chart
        fig11, ax11 = plt.subplots(figsize=(5, 4))
        colors = plt.cm.Set3(range(len(kategori_count)))
        wedges, texts, autotexts = ax11.pie(
            kategori_count.values,
            labels=kategori_count.index,
            autopct='%1.1f%%',
            colors=colors,
            startangle=90,
            textprops={'fontsize': 9}
        )
        
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
            autotext.set_fontsize(9)
        
        ax11.set_title('Persentase Kategori Kesegaran', fontsize=11, fontweight='bold')
        st.pyplot(fig11)
        plt.close(fig11)
    
    # Summary metrics
    st.markdown("---")
    st.subheader("Ringkasan Statistik")
    
    col_f1, col_f2, col_f3, col_f4 = st.columns(4)
    
    with col_f1:
        most_common = kategori_count.index[0] if len(kategori_count) > 0 else "N/A"
        st.metric("Kategori Terbanyak", most_common, 
                  f"{kategori_percent.iloc[0]:.1f}%")
    
    with col_f2:
        avg_freshness = df_clean['sisa_hari'].mean()
        st.metric("Rata-rata Sisa Hari", f"{avg_freshness:.1f} hari")
    
    with col_f3:
        min_freshness = df_clean['sisa_hari'].min()
        st.metric("Sisa Hari Terendah", f"{min_freshness:.0f} hari")
    
    with col_f4:
        max_freshness = df_clean['sisa_hari'].max()
        st.metric("Sisa Hari Tertinggi", f"{max_freshness:.0f} hari")
    
else:
    st.error("Kolom 'sisa_hari' tidak ditemukan dalam data. Pastikan data telah diproses dengan benar.")

st.divider()

# Fungsi kategorisasi
def kategori_buah(sisa_hari):
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

# Tambahkan kolom kategori
df_clean['kategori_buah'] = df_clean['sisa_hari'].apply(kategori_buah)

# Hitung jumlah tiap kategori
kategori_count = df_clean['kategori_buah'].value_counts()

# Hitung persentase
kategori_percent = (
    df_clean['kategori_buah']
    .value_counts(normalize=True) * 100
)

# Print hasil
print("Jumlah tiap kategori:")
print(kategori_count)

print("\nPersentase tiap kategori:")
print(kategori_percent)

# Pie chart
plt.figure(figsize=(5,5))

plt.pie(
    kategori_count,
    labels=kategori_count.index,
    autopct='%1.1f%%'
)

plt.title('Persentase Kategori Buah Berdasarkan Sisa Hari')
plt.show()
st.divider()

# ==========================================
# 3. ANALISIS EFEKTIVITAS PENYIMPANAN  ← BARU
# ==========================================
st.header("3. Analisis Efektivitas Penyimpanan")
st.markdown(
    "Mengukur seberapa efektif setiap lokasi penyimpanan dalam mempertahankan kesegaran item "
    "berdasarkan rasio sisa hari terhadap hari sejak pembelian."
)


col_e, col_f = st.columns(2)

with col_e:
    st.subheader("Lokasi Penyimpanan paling efektif untuk menjaga sisa umur simpan")
    

with col_f:
    st.subheader("Variabilitas Efektivitas (Std Dev)")
    fig7, ax7 = plt.subplots(figsize=(8, 5))
    pivot_std = efek_lokasi.pivot(index='lokasi_penyimpanan', columns='jenis_item', values='std_efektivitas')
    pivot_std.plot(kind='bar', ax=ax7, color=['#FF7043', '#4CAF50'], edgecolor='white', width=0.6, alpha=0.85)
    ax7.set_ylabel('Standar Deviasi Efektivitas (%)')
    ax7.set_xlabel('Lokasi Penyimpanan')
    ax7.set_title('Konsistensi Penyimpanan (Semakin Rendah = Lebih Konsisten)')
    ax7.tick_params(axis='x', rotation=30)
    ax7.legend(title='Jenis Item')
    st.pyplot(fig7)

# — Boxplot distribusi efektivitas —
st.subheader("Distribusi Efektivitas per Lokasi")
fig8, ax8 = plt.subplots(figsize=(12, 5))
sns.boxplot(
    data=df_clean,
    x='lokasi_penyimpanan',
    y='efektivitas_pct',
    hue='jenis_item',
    palette=warna_item,
    ax=ax8,
    width=0.5,
    flierprops=dict(marker='o', markersize=3, alpha=0.5)
)
ax8.axhline(50, color='red', linestyle='--', linewidth=1, label='Threshold 50%')
ax8.set_title('Distribusi Efektivitas Penyimpanan per Lokasi')
ax8.set_xlabel('Lokasi Penyimpanan')
ax8.set_ylabel('Efektivitas (%)')
ax8.legend(title='Jenis Item')
st.pyplot(fig8)

# — Tabel ringkasan efektivitas —
with st.expander("📋 Lihat Tabel Ringkasan Efektivitas"):
    tabel_efek = (
        df_clean.groupby(['lokasi_penyimpanan', 'jenis_item'])['efektivitas_pct']
        .describe()
        .round(2)
        .reset_index()
    )
    st.dataframe(tabel_efek, use_container_width=True)

st.divider()

# ==========================================
# 4. FOOD WASTE RISK ANALYSIS  ← BARU
# ==========================================
st.header("4. Food Waste Risk Analysis")
st.markdown(
    "Identifikasi item dengan risiko terbuang berdasarkan sisa hari yang tersedia. "
    "Item dikategorikan ke dalam tiga level risiko."
)

# — Definisi level risiko —
def klasifikasi_risiko(sisa):
    if sisa <= 2:
        return '🔴 Tinggi (≤2 hari)'
    elif sisa <= 5:
        return '🟡 Sedang (3–5 hari)'
    else:
        return '🟢 Rendah (>5 hari)'

df_clean['risiko_waste'] = df_clean['sisa_hari'].apply(klasifikasi_risiko)

RISIKO_ORDER = ['🔴 Tinggi (≤2 hari)', '🟡 Sedang (3–5 hari)', '🟢 Rendah (>5 hari)']
RISIKO_COLOR = {
    '🔴 Tinggi (≤2 hari)': '#e53935',
    '🟡 Sedang (3–5 hari)': '#FFA726',
    '🟢 Rendah (>5 hari)': '#43A047',
}

# — Metrik risiko —
n_tinggi  = (df_clean['risiko_waste'] == '🔴 Tinggi (≤2 hari)').sum()
n_sedang  = (df_clean['risiko_waste'] == '🟡 Sedang (3–5 hari)').sum()
n_rendah  = (df_clean['risiko_waste'] == '🟢 Rendah (>5 hari)').sum()
total     = len(df_clean)

r1, r2, r3 = st.columns(3)
with r1:
    st.error(f"🔴 **Risiko Tinggi**\n\n**{n_tinggi}** item &nbsp;|&nbsp; {n_tinggi/total*100:.1f}%")
with r2:
    st.warning(f"🟡 **Risiko Sedang**\n\n**{n_sedang}** item &nbsp;|&nbsp; {n_sedang/total*100:.1f}%")
with r3:
    st.success(f"🟢 **Risiko Rendah**\n\n**{n_rendah}** item &nbsp;|&nbsp; {n_rendah/total*100:.1f}%")

col_g, col_h = st.columns(2)

with col_g:
    st.subheader("Distribusi Risiko per Jenis Item")
    risk_jenis = (
        df_clean.groupby(['jenis_item', 'risiko_waste'])
        .size()
        .reset_index(name='jumlah')
    )
    fig9, ax9 = plt.subplots(figsize=(8, 5))
    bottom_vals = {j: 0 for j in df_clean['jenis_item'].unique()}
    for risiko in RISIKO_ORDER:
        subset = risk_jenis[risk_jenis['risiko_waste'] == risiko]
        ax9.bar(
            subset['jenis_item'],
            subset['jumlah'],
            bottom=[bottom_vals[j] for j in subset['jenis_item']],
            color=RISIKO_COLOR[risiko],
            label=risiko,
            edgecolor='white',
            width=0.5
        )
        for _, row in subset.iterrows():
            ax9.text(
                row['jenis_item'],
                bottom_vals[row['jenis_item']] + row['jumlah'] / 2,
                str(int(row['jumlah'])),
                ha='center', va='center', fontsize=9, color='white', fontweight='bold'
            )
            bottom_vals[row['jenis_item']] += row['jumlah']
    ax9.set_title('Distribusi Level Risiko per Jenis Item')
    ax9.set_xlabel('Jenis Item')
    ax9.set_ylabel('Jumlah Item')
    ax9.legend(title='Level Risiko', bbox_to_anchor=(1, 1))
    st.pyplot(fig9)

with col_h:
    st.subheader("Risiko per Lokasi Penyimpanan")
    risk_lokasi = (
        df_clean.groupby(['lokasi_penyimpanan', 'risiko_waste'])
        .size()
        .reset_index(name='jumlah')
    )
    fig10, ax10 = plt.subplots(figsize=(8, 5))
    lokasi_list_all = df_clean['lokasi_penyimpanan'].unique()
    bottom_vals2 = {l: 0 for l in lokasi_list_all}
    for risiko in RISIKO_ORDER:
        subset = risk_lokasi[risk_lokasi['risiko_waste'] == risiko]
        ax10.bar(
            subset['lokasi_penyimpanan'],
            subset['jumlah'],
            bottom=[bottom_vals2[l] for l in subset['lokasi_penyimpanan']],
            color=RISIKO_COLOR[risiko],
            label=risiko,
            edgecolor='white',
            width=0.5
        )
        for _, row in subset.iterrows():
            ax10.text(
                row['lokasi_penyimpanan'],
                bottom_vals2[row['lokasi_penyimpanan']] + row['jumlah'] / 2,
                str(int(row['jumlah'])),
                ha='center', va='center', fontsize=9, color='white', fontweight='bold'
            )
            bottom_vals2[row['lokasi_penyimpanan']] += row['jumlah']
    ax10.set_title('Distribusi Level Risiko per Lokasi')
    ax10.set_xlabel('Lokasi Penyimpanan')
    ax10.set_ylabel('Jumlah Item')
    ax10.tick_params(axis='x', rotation=30)
    ax10.legend(title='Level Risiko', bbox_to_anchor=(1, 1))
    st.pyplot(fig10)

# — Top item berisiko tinggi —
st.subheader("🔴 Item dengan Risiko Waste Tertinggi")
col_filter1, col_filter2 = st.columns(2)
with col_filter1:
    filter_jenis = st.multiselect(
        "Filter Jenis Item:", df_clean['jenis_item'].unique(),
        default=df_clean['jenis_item'].unique().tolist()
    )
with col_filter2:
    filter_lokasi = st.multiselect(
        "Filter Lokasi:", df_clean['lokasi_penyimpanan'].unique(),
        default=df_clean['lokasi_penyimpanan'].unique().tolist()
    )

df_risiko_tinggi = df_clean[
    (df_clean['risiko_waste'] == '🔴 Tinggi (≤2 hari)') &
    (df_clean['jenis_item'].isin(filter_jenis)) &
    (df_clean['lokasi_penyimpanan'].isin(filter_lokasi))
][['nama_item', 'jenis_item', 'lokasi_penyimpanan', 'sisa_hari', 'hari_sejak_pembelian', 'efektivitas_pct']] \
    .sort_values('sisa_hari') \
    .reset_index(drop=True)

if df_risiko_tinggi.empty:
    st.success("✅ Tidak ada item berisiko tinggi pada filter yang dipilih.")
else:
    st.dataframe(
        df_risiko_tinggi.style
            .background_gradient(subset=['sisa_hari'], cmap='Reds_r')
            .format({'efektivitas_pct': '{:.1f}%', 'sisa_hari': '{:.0f}', 'hari_sejak_pembelian': '{:.0f}'}),
        use_container_width=True
    )

# — Heatmap risiko: nama item vs lokasi —
st.subheader("Heatmap Rata-rata Sisa Hari: Item vs Lokasi")
heatmap_waste = df_clean.pivot_table(
    values='sisa_hari',
    index='nama_item',
    columns='lokasi_penyimpanan',
    aggfunc='mean'
).round(1)

fig11, ax11 = plt.subplots(figsize=(12, max(5, len(heatmap_waste) * 0.4)))
sns.heatmap(
    heatmap_waste,
    annot=True, fmt='.1f',
    cmap='RdYlGn',
    linewidths=0.4,
    ax=ax11,
    cbar_kws={'label': 'Rata-rata Sisa Hari'}
)
ax11.set_title('Rata-rata Sisa Hari per Nama Item & Lokasi Penyimpanan\n(Merah = Berisiko, Hijau = Aman)')
ax11.set_xlabel('Lokasi Penyimpanan')
ax11.set_ylabel('Nama Item')
ax11.tick_params(axis='y', labelsize=8)
st.pyplot(fig11)

# — Rekomendasi otomatis —
st.subheader("💡 Rekomendasi Penanganan")
if n_tinggi > 0:
    nama_tinggi = df_clean[df_clean['risiko_waste'] == '🔴 Tinggi (≤2 hari)']['nama_item'].value_counts()
    top3 = nama_tinggi.head(3).index.tolist()
    st.error(
        f"**Segera tangani:** {', '.join(top3)} memiliki jumlah unit terbanyak dengan sisa ≤2 hari. "
        "Prioritaskan untuk dikonsumsi, diolah, atau didistribusikan."
    )

efek_terendah = (
    df_clean.groupby('lokasi_penyimpanan')['efektivitas_pct']
    .mean()
    .idxmin()
)
st.warning(
    f"**Evaluasi lokasi '{efek_terendah}':** Lokasi ini memiliki rata-rata efektivitas penyimpanan terendah. "
    "Pertimbangkan penyesuaian suhu, kelembaban, atau metode penyimpanan."
)
st.info(
    "**Tip umum:** Item dengan efektivitas <50% sebaiknya dipindahkan ke lokasi penyimpanan yang lebih optimal "
    "atau jadwalkan rotasi stok lebih sering."
)

st.divider()
st.caption("🍎 Dashboard Inventori Sayur & Buah · Dibuat dengan Streamlit & Matplotlib/Seaborn")