# README - Dataset Kualitas Buah dan Sayur

## 📁 Nama File
`sayur_buah_bersih.csv`

## 📌 Deskripsi Singkat
Dataset ini berisi informasi tentang kondisi buah dan sayur berdasarkan jenis item, lokasi penyimpanan, lama penyimpanan, serta sisa umur simpan. Data telah melalui proses pembersihan (missing values, outlier, dan inkonsistensi label) sehingga siap digunakan untuk analisis.

## 📊 Data Dictionary

| Nama Kolom | Tipe Data | Deskripsi | Contoh Nilai |
|------------|-----------|-----------|----------------|
| `nama_item` | String (kategorikal) | Nama buah atau sayur | Mangga, Timun, Apel, Wortel, Cabe, Jeruk, Anggur, Pisang, Kentang, Tomat |
| `jenis_item` | String (kategorikal) | Kategori item | Buah, Sayur |
| `lokasi_penyimpanan` | String (kategorikal) | Lokasi penyimpanan | Pembeku, Suhu Ruang, Pendingin |
| `hari_sejak_pembelian` | Numerik (integer) | Jumlah hari sejak pembelian (dibulatkan) | 0, 1, 2, 3, 4, 5, 6, dst. |
| `sisa_hari` | Numerik (float) | Perkiraan sisa umur simpan dalam hari | 0.1, 1.3, 2.5, 11.5, 30.6, dst. |
| `label` | String (kategorikal) | Kondisi item saat pengamatan | Matang, Busuk, Mentah, Terlalu Matang, Segar |

## 📈 Statistik Ringkas (berdasarkan data bersih)

- **Jumlah baris**: 3723 (setelah pembersihan)
- **Jumlah kolom**: 6
- **Tidak ada nilai kosong** pada keenam kolom.
- **Label yang tersedia**:
  - `Matang`
  - `Busuk`
  - `Mentah`
  - `Terlalu Matang`
  - `Segar`

## 🧹 Proses Pembersihan yang Dilakukan (dari dataset kotor ke bersih)

1. Menghapus baris dengan nilai kosong pada kolom `nama_item`, `jenis_item`, `lokasi_penyimpanan`, atau `label`.
2. Menstandarisasi nilai kategori:
   - `Pembeku`, `Suhu Ruang`, `Pendingin` (untuk lokasi penyimpanan)
   - `Buah` dan `Sayur` (untuk jenis item)
3. Mengonversi `hari_sejak_pembelian` menjadi integer (pembulatan ke bawah).
4. Menghapus baris dengan nilai negatif atau sangat ekstrem (outlier) pada `hari_sejak_pembelian` dan `sisa_hari`.
5. Menyeragamkan label kondisi menjadi 5 kategori utama.

## 💡 Contoh Penggunaan

Dataset ini dapat digunakan untuk:
- Analisis pengaruh suhu penyimpanan terhadap ketahanan buah/sayur.
- Prediksi kondisi (klasifikasi) berdasarkan fitur penyimpanan dan waktu.
- Visualisasi distribusi sisa umur simpan per jenis item.

## 📥 Sumber Data
Dataset merupakan hasil cleaning dari file mentah `sayur_buah_kotor.csv`.

---
📅 Terakhir diperbarui: 23 Mei 2026