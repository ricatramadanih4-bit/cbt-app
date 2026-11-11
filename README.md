# Aplikasi CBT Siap Deploy ke Railway

## Fitur Baru:
1. **Import Siswa via Excel** (menggunakan pandas & openpyxl).
2. **Import Soal via Word** (menggunakan python-docx).
3. **Database Dinamis**: Otomatis menggunakan PostgreSQL jika di-deploy ke Railway (membuat aplikasi kuat diakses 1500 siswa bersamaan), atau SQLite jika dijalankan di laptop lokal.

## Cara Deploy ke Railway:
1. Upload folder ini ke GitHub repository Anda.
2. Buka https://railway.app dan buat project baru dari GitHub repo tersebut.
3. Di dalam project Railway, tambahkan Plugin **PostgreSQL**.
4. Railway otomatis akan menyuntikkan `DATABASE_URL` ke environment variables dan Gunicorn akan menjalankan aplikasi Anda.

## Cara Menjalankan Lokal (di Laptop):
1. Install requirements: `pip install -r requirements.txt`
2. Jalankan: `python main.py`
3. Buka browser: `http://localhost:5000/import`
