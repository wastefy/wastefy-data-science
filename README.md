# Wastefy - Data Science ♻️📊

Repositori ini berfokus pada pengumpulan, pemrosesan data, analisis data eksploratif (EDA), dan pembuatan dahshboard menggunakan streamlit.

## 📌 Ringkasan

Wastefy bertujuan untuk mengurangi limbah makanan berupa sayuran dan buah dengan menganalisis karakteristik makanan, umur simpan, dan kondisi penyimpanan untuk menghasilkan wawasan yang dapat ditindaklanjuti.

## 👥 Tim

- <a href="https://github.com/alifanshar">Muhammad Alif Anshar </a>
- <a href="https://github.com/AryaGoberto">Arya Gunavaro Goberto</a>


## 📊 Data Dictionary
| Nama Kolom             | Tipe Data            | Deskripsi                                | Contoh Nilai                                                             |
| ---------------------- | -------------------- | ---------------------------------------- | ------------------------------------------------------------------------ |
| `nama_item`            | String (kategorikal) | Nama buah atau sayur                     | Mangga, Timun, Apel, Wortel, Cabe, Jeruk, Anggur, Pisang, Kentang, Tomat |
| `jenis_item`           | String (kategorikal) | Kategori item                            | Buah, Sayur                                                              |
| `lokasi_penyimpanan`   | String (kategorikal) | Lokasi penyimpanan                       | Pembeku, Suhu Ruang, Pendingin                                           |
| `hari_sejak_pembelian` | Numerik (integer)    | Jumlah hari sejak pembelian (dibulatkan) | 0, 1, 2, 3, 4, 5, 6, dst.                                                |
| `sisa_hari`            | Numerik (integer)    | Perkiraan sisa umur simpan dalam hari    | 1, 2, 11, 30, dst.                                                       |
| `label`                | String (kategorikal) | Kondisi item saat pengamatan             | Matang, Busuk, Mentah, Terlalu Matang, Segar                             |

## ⚙️ Tech Stack

Python, Pandas, NumPy, Matplotlib, Seaborn, Scikit-learn

## 🚀 Setup

1. Clone Repositori

```bash
git clone https://github.com/wastefy/wastefy-data-science.git
cd wastefy-data-science
```

2. Buat virtual environment

```bash
python -m venv venv
```

3. Aktifkan virtual environment

- Windows

```bash
venv\Scripts\activate.ps1
```

- Mac/Linux

```bash
source venv/bin/activate..ps1
```

4. Install Dependensi

```bash
pip install -r requirements.txt
```

## Langkah Jalankan Dashboard

1. Clone this repository

```bash
cd dashboard
```

2. Create virtual environment

```bash
streamlit run app.py
```