# Showcase Aplikasi Soft Computing

Selamat datang di repositori Showcase Aplikasi Soft Computing! Proyek ini adalah aplikasi web yang dibangun menggunakan **Flask** (framework Python) untuk mendemonstrasikan beberapa konsep dan algoritma dari bidang *soft computing* secara interaktif.
![image alt](https://github.com/AhmdMaulidan/Filter-Citra/blob/433a319ef0202481f67581fcded94ff3a3ea88f8/contoh%20image.png)

## 🌟 Fitur Utama

Aplikasi ini memiliki beberapa modul utama:

1.  **Kalkulator Fuzzy Sugeno**
    -   Sebuah alat interaktif untuk menghitung persentase tip yang ideal berdasarkan dua input: kualitas pelayanan (*service*) dan kualitas makanan (*food*).
    -   Mengimplementasikan sistem inferensi fuzzy model Sugeno, mulai dari fuzzifikasi input, evaluasi aturan (rules), hingga defuzzifikasi untuk menghasilkan output yang konkret.
    -   Pengguna dapat menambahkan, mengubah, atau menghapus aturan fuzzy secara dinamis untuk melihat bagaimana perubahan tersebut memengaruhi hasil akhir.

2.  **Optimasi Masalah Knapsack dengan Algoritma Genetika**
    -   Menyelesaikan masalah klasik *0/1 Knapsack*, di mana tujuannya adalah memaksimalkan total nilai barang yang dimasukkan ke dalam tas tanpa melebihi kapasitas beratnya.
    -   Menggunakan Algoritma Genetika untuk mencari solusi optimal atau mendekati optimal.
    -   Pengguna dapat mendefinisikan daftar barang (beserta berat dan nilainya) dan kapasitas maksimal tas. Aplikasi akan menampilkan barang-barang terpilih, total berat, total nilai, dan grafik evolusi fitness dari generasi ke generasi.

3.  **Sistem Manajemen Tugas Sederhana**
    -   Fitur CRUD (*Create, Read, Update, Delete*) dasar untuk mengelola artikel atau catatan tugas.
    -   Dibangun menggunakan Flask dan SQLAlchemy dengan database SQLite.

## 🛠️ Teknologi yang Digunakan

-   **Backend**:
    -   [Python 3](https://www.python.org/)
    -   [Flask](https://flask.palletsprojects.com/)
    -   [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/)
-   **Frontend**:
    -   HTML5
    -   CSS3
    -   JavaScript
-   **Database**:
    -   SQLite

## 📂 Struktur Proyek

```
.
├── app.py                  # File utama aplikasi Flask (routing, view logic)
├── genetic_knapsack.py     # Modul berisi implementasi Algoritma Genetika untuk Knapsack
├── requirements.txt        # Daftar dependensi Python yang dibutuhkan
├── static/                 # Aset statis (CSS, JS, gambar)
│   └── uploads/
├── templates/              # File-file template HTML (Jinja2)
│   ├── index.html
│   ├── project.html
│   ├── knapsack_calculator.html
│   ├── sugeno_calculator.html
│   └── ... (template lainnya)
└── tasks.db                # File database SQLite (dibuat otomatis saat pertama kali dijalankan)
```

## 🚀 Cara Menjalankan Proyek Secara Lokal

Ikuti langkah-langkah berikut untuk menjalankan aplikasi ini di komputer Anda.

### 1. Prasyarat

Pastikan Anda sudah menginstal **Python 3.8** atau versi yang lebih baru.

### 2. Kloning Repositori

```bash
git clone https://github.com/NAMA_USER_ANDA/NAMA_REPOSITORI_ANDA.git
cd NAMA_REPOSITORI_ANDA
```

### 3. Buat dan Aktifkan Virtual Environment

Sangat disarankan untuk menggunakan *virtual environment* agar tidak mengganggu instalasi Python global Anda.

```bash
# Untuk Windows
python -m venv venv
.\venv\Scripts\activate

# Untuk macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 4. Instal Dependensi

Instal semua pustaka Python yang diperlukan menggunakan file `requirements.txt`.

```bash
pip install -r requirements.txt
```

### 5. Jalankan Aplikasi

Setelah semua dependensi terinstal, jalankan aplikasi Flask.

```bash
python app.py
```

Buka browser Anda dan kunjungi alamat `http://127.0.0.1:5000` untuk melihat aplikasi berjalan.
