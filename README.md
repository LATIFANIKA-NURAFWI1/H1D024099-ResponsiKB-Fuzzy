# README – Sistem Fuzzy
## Rekomendasi Program Studi & Universitas

---

## Identitas Mahasiswa

| | |
|---|---|
| **Nama** | [LATIFANIKA NURAFWI] |
| **NIM** | [H1D024099] |
| **Program Studi** | [Informatika] |
| **Fakultas** | [Teknik] |
| **Universitas** | [Universitas Jenderal Soedirman] |
| **Mata Kuliah** | Sistem Pakar / Kecerdasan Buatan |
| **Tahun** | 2026 |

---

## Deskripsi Singkat

Aplikasi web berbasis **Python + Flask** yang menggunakan **Logika Fuzzy Mamdani** untuk merekomendasikan program studi dan universitas PTN yang paling sesuai bagi calon mahasiswa. Sistem mempertimbangkan faktor minat, bakat, nilai rapor, kondisi ekonomi, jarak, dan prospek kerja.

## Link
[Link Website](https://h1d024099-responsi-kb-fuzzy.vercel.app/)   

---

## Fitur Utama

- 38 pilihan prodi dari 15 PTN ternama di Indonesia
- 12 jenis minat & 10 jenis bakat (dengan tabel penjelasan)
- 25 aturan fuzzy (inferensi Mamdani, defuzzifikasi Weighted Average)
- Output: skor kesesuaian 0–100 + label + penjelasan per prodi
- Estimasi jarak dari 18 kota asal ke lokasi kampus

---

## Struktur Folder

```
fuzzy_app/
├── app.py              ← Logika fuzzy & routing Flask
├── requirements.txt
├── templates/
│   ├── index.html      ← Form input
│   └── hasil.html      ← Halaman hasil rekomendasi
└── static/
    └── style.css
```

---

## Cara Menjalankan

```bash
# 1. Masuk ke folder
cd fuzzy_app

# 2. Install dependensi
pip install flask

# 3. Jalankan aplikasi
python app.py

# 4. Buka browser
http://localhost:5001
```

---

## Dependensi

```
flask>=3.0.0
```

---

## Metode yang Digunakan

| Komponen | Metode |
|---|---|
| Fuzzifikasi | Fungsi segitiga & trapesium |
| Inferensi | Mamdani (operator min/max) |
| Defuzzifikasi | Weighted Average |
| Aturan | 25 aturan IF-THEN |

---

> ⚠️ Hasil rekomendasi bersifat **edukatif**, bukan jaminan penerimaan resmi.
