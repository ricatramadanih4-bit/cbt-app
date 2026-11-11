# 📋 Panduan Lengkap CBT Exam System

> **Status Server:** 🟢 Berjalan di `http://127.0.0.1:8000`

---

## 🚀 Cara Menjalankan Server

### Mode Development (untuk testing)
Klik dua kali file `run.bat` di folder aplikasi, atau jalankan:
```
C:\Users\Hype G12\.gemini\antigravity\scratch\cbt_exam_app\run.bat
```
Akses di: **http://127.0.0.1:8000**

### Mode Produksi (untuk 1500 siswa, via jaringan sekolah)
Klik dua kali file `run_production.bat`, lalu:
- Bagikan alamat **http://[IP-KOMPUTER-SERVER]:8000** ke siswa
- Contoh: `http://192.168.1.10:8000`

> [!TIP] Gunakan `run_production.bat` saat hari ujian. Komputer yang menjalankan server harus terhubung ke jaringan yang sama dengan siswa (WiFi sekolah / LAN).

---

## 👤 Login Default

| Role | Username | Password |
|------|----------|----------|
| Guru / Pengawas | `guru` | `admin123` |
| Siswa contoh 1 | `siswa1` | `123456` |
| Siswa contoh 2 | `siswa2` | `123456` |
| Siswa contoh 3 | `siswa3` | `123456` |

---

## 👨‍🎓 Cara Import Nama Siswa (Per Kelas)

### Cara 1 — Upload File Excel (.xlsx) ✅ Paling Mudah

1. Login sebagai guru → masuk ke **Dashboard Pengawas**
2. Klik tab **"Siswa & Pengawas"**
3. Klik **"📥 Unduh Format Excel"** → download template
4. Isi template di Microsoft Excel / Google Sheets:

| NIS | Nama Lengkap | Password |
|-----|-------------|----------|
| 2024001 | Andi Pratama | 123456 |
| 2024002 | Budi Santoso | 123456 |

5. Simpan sebagai `.xlsx`
6. Klik **"📂 Upload File Excel"** → pilih file → klik Upload

> [!NOTE] Password bisa dikosongkan, akan otomatis pakai password default `123456`.

### Cara 2 — Copy-Paste dari Excel

1. Buka data siswa di Excel
2. Select kolom NIS, Nama, Password → Copy (Ctrl+C)
3. Di dashboard pengawas → klik **"📋 Copy-Paste Excel"**
4. Paste (Ctrl+V) di area teks → klik Import

### Cara 3 — Tambah Satu per Satu

Klik **"+ Manual 1 Siswa"** → isi form → Simpan.

---

## 📄 Cara Import Soal dari Word (.docx) ✅ Baru!

### Format Soal di Word

Buat dokumen Word dengan format seperti ini:

```
1. Protokol yang digunakan untuk mengirim email adalah...
A. HTTP
B. FTP
C. SMTP
D. DNS
E. DHCP
Jawaban: C

2. Perangkat yang menghubungkan dua jaringan berbeda adalah...
A. Switch
B. Hub
C. Router
D. Modem
E. Repeater
Jawaban: C
```

> [!IMPORTANT] Setiap soal WAJIB memiliki baris **"Jawaban: X"** (ganti X dengan huruf yang benar). Tanpa baris ini, soal akan dilewati.

### Langkah Import

1. Login sebagai guru → tab **"Bank Soal"**
2. Klik tombol hijau **"📄 Import dari Word"**
3. Klik **"Unduh Template Word"** untuk lihat contoh format yang benar
4. Upload file `.docx` Anda → klik **"Upload & Import Soal"**
5. Soal langsung masuk ke bank soal ujian aktif ✅

---

## 🌐 Mendukung 1500 Siswa Serentak

### Apa yang sudah dioptimasi:

| Fitur | Detail |
|-------|--------|
| **SQLite WAL Mode** | Multiple pembaca bisa akses DB bersamaan |
| **Cache 64 MB** | Query lebih cepat |
| **Memory-mapped I/O 256 MB** | Baca file DB tanpa disk I/O |
| **GZip Compression** | Response lebih kecil, hemat bandwidth |
| **Async I/O** | Ribuan koneksi diproses tanpa blocking |
| `--limit-concurrency 2000` | Batas koneksi bersamaan |
| `--backlog 2048` | Antrian koneksi masuk |

### Rekomendasi Jaringan untuk 1500 Siswa

```
Komputer Server
    ├── RAM minimal: 4 GB (ideal 8 GB)
    ├── CPU: 4 core+ (tersedia 12 core ✅)
    ├── Koneksi LAN: 1 Gbps ke switch
    └── Switch → WiFi AP (1 AP per ~50 siswa)
```

> [!WARNING] SQLite cocok untuk **hingga ~500-1000 user bersamaan** saat write-heavy. Untuk 1500 user aktif menulis jawaban serentak, disarankan upgrade ke PostgreSQL. Namun untuk ujian bertahap (kelas per kelas), SQLite + WAL cukup.

> [!TIP] Jalankan ujian **per kelas** (tidak 1500 orang sekaligus) untuk performa optimal. Contoh: 30 siswa × 50 kelas, ujian bergilir.

---

## 🔒 Fitur Anti-Kecurangan

| Fitur | Keterangan |
|-------|------------|
| **Fullscreen Lock** | Siswa tidak bisa keluar dari halaman ujian |
| **Tab Switch Detection** | Pindah tab = tercatat sebagai pelanggaran |
| **Alt+Tab Blocked** | Shortcut keyboard terblokir |
| **Right-click Disabled** | Klik kanan tidak aktif |
| **Auto Disqualifikasi** | Setelah X pelanggaran (bisa diatur guru) |
| **Live Monitoring** | Guru melihat status semua siswa real-time |
| **Audit Log** | Semua pelanggaran tercatat dengan timestamp |

---

## 📁 Struktur File Aplikasi

```
cbt_exam_app/
├── run.bat              ← Jalankan untuk development
├── run_production.bat   ← Jalankan untuk 1500 siswa (produksi)
├── main.py              ← Backend API (FastAPI)
├── database.py          ← Database SQLite + optimasi WAL
├── cbt.db               ← Database utama
├── templates/
│   ├── index.html       ← Halaman login siswa
│   ├── exam.html        ← Halaman ujian siswa
│   └── proctor.html     ← Dashboard pengawas/guru
└── static/
    ├── js/cbt_app.js    ← Anti-cheat engine
    └── css/style.css
```
