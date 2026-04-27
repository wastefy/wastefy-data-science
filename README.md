# Wastefy - Data Science ♻️📊

Selamat datang di repositori Data Science untuk proyek **Wastefy**. Repositori ini difokuskan pada pengolahan data, analisis, eksperimen model machine learning, hingga pembuatan dashboard visualisasi untuk mendukung sistem manajemen inventaris makanan berbasis AI.

## 👥 Tim Data Science
- **Alif**
- **Arya**

---

## 🌿 Strategi Branching
Kami menggunakan dua branch utama untuk menjaga stabilitas kode:
* **`main`**: Digunakan hanya untuk versi final dan rilis produksi.
* **`dev`**: Branch utama untuk proses pengembangan. Semua fitur baru harus digabungkan ke sini terlebih dahulu.

### Penamaan Branch Fitur
Gunakan format `feature/ds-<nama-fitur>`. Contoh yang tersedia:
- `feature/ds-cleaning`
- `feature/ds-eda`
- `feature/ds-dashboard`
- `feature/ds-ab-testing`

---

## 🚀 Alur Kerja (Workflow)
Ikuti langkah-langkah berikut untuk mulai mengerjakan fitur baru:

1.  **Update lokal:**
    ```bash
    git checkout dev
    git pull origin dev
    ```
2.  **Buat branch baru:**
    ```bash
    git checkout -b feature/ds-nama-fitur
    ```
3.  **Lakukan perubahan/coding.**
4.  **Simpan perubahan:**
    ```bash
    git add .
    git commit -m "feat: deskripsi singkat"
    ```
5.  **Push ke remote:**
    ```bash
    git push origin feature/ds-nama-fitur
    ```
6.  **Buat Pull Request (PR)** ke branch `dev`.

---

## 📝 Aturan Commit & Pull Request

### Format Commit Message
Kami menggunakan standar *Conventional Commits*:
- `feat:` (fitur baru)
- `fix:` (perbaikan bug)
- `docs:` (perubahan dokumentasi/README)
- `refactor:` (perubahan kode yang bukan fitur maupun bug)
- `style:` (format, semicolon, dll; bukan perubahan logika)
- `test:` (menambah atau memperbaiki test)
- `chore:` (update build task, package manager, dll)

**Contoh:** `git commit -m "feat: implement logic for data cleaning"`

### Panduan Pull Request (PR)
Saat membuat PR, pastikan:
1.  **Judul PR:** `type(scope): deskripsi`. Contoh: `feat(ds): add k-medoids clustering script`
2.  **Deskripsi PR:**
    - **Apa** yang dibuat/diubah?
    - **Kenapa** perubahan ini diperlukan?
    - **Cara Test:** Langkah untuk menjalankan script/notebook tersebut.
    - **Screenshot:** (Opsional) Lampirkan visualisasi atau hasil output jika perlu.

---

## ✅ Review Rules
Sebelum sebuah PR dapat di-merge ke `dev`, harus memenuhi syarat:
- minimal **1 reviewer** memberikan *Approve*.
- **No Conflict** dengan branch tujuan.
- **Build Passing** (jika ada automated testing).
- Tidak merusak fitur/script yang sudah ada.

### 🚫 Larangan Keras
- ❌ **Push langsung ke `main`**.
- ❌ Coding langsung di branch `dev` tanpa melalui PR.
- ❌ Penamaan branch asal-asalan (contoh: `test123`, `fixaja`, `baru`).
- ❌ Commit message random/tidak bermakna.
- ❌ Merge PR sendiri tanpa ada review.

---

## 🛠 Penanganan Konflik (Merge Conflict)
Jika terjadi konflik saat akan melakukan PR, lakukan langkah berikut di lokal:
```bash
git checkout dev
git pull
git checkout feature/branch-kamu
git merge dev
# Selesaikan konflik secara manual di file yang bersangkutan
git add .
git commit -m "chore: resolve merge conflict with dev"
git push
```

---

## 📂 Pengaturan Lingkungan (Gitignore)
File-file berikut **tidak boleh** di-commit ke repositori karena alasan keamanan dan efisiensi. Pastikan `.gitignore` Anda mencakup:
- `.env` (Environment variables)
- `node_modules/`
- `venv/` atau `.venv/` (Python virtual environment)
- `__pycache__/`
- `secret.json` atau file kredensial lainnya (GCP Key, Database password, dll)

---

**Wastefy Project 2026** - *Better management for better future.*
