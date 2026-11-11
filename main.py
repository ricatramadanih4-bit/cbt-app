import os
import pandas as pd
from docx import Document
from flask import Flask, request, render_template
from database import db, init_db, Siswa, Soal

app = Flask(__name__)
app.secret_key = "cbt_super_secret_key"

# Inisialisasi Database
init_db(app)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return "Sistem CBT Siap. Buka /import untuk memasukkan data siswa dan soal."

@app.route('/import', methods=['GET', 'POST'])
def import_data():
    pesan = ""
    if request.method == 'POST':
        tipe = request.form.get('tipe')
        file = request.files.get('file')
        
        if not file:
            pesan = "File tidak ditemukan!"
        else:
            if tipe == 'siswa' and file.filename.endswith('.xlsx'):
                try:
                    df = pd.read_excel(file)
                    for index, row in df.iterrows():
                        nis = str(row.get('NIS', '')).strip()
                        nama = str(row.get('Nama', '')).strip()
                        kelas = str(row.get('Kelas', '')).strip()
                        password = str(row.get('Password', nis)).strip()
                        
                        if nis and nama:
                            existing = Siswa.query.filter_by(nis=nis).first()
                            if not existing:
                                siswa_baru = Siswa(nis=nis, nama=nama, kelas=kelas, password=password)
                                db.session.add(siswa_baru)
                    db.session.commit()
                    pesan = f"✅ Berhasil import {len(df)} data Siswa dari Excel!"
                except Exception as e:
                    pesan = f"❌ Gagal import siswa: {e}"

            elif tipe == 'soal' and file.filename.endswith('.docx'):
                try:
                    doc = Document(file)
                    soal_text = [p.text.strip() for p in doc.paragraphs if p.text.strip()]
                    
                    soal_masuk = 0
                    # Asumsi format: 1 baris soal, lalu 4 baris opsi, 1 baris kunci (Total 6 baris per soal)
                    for i in range(0, len(soal_text), 6):
                        if i + 5 < len(soal_text):
                            pertanyaan = soal_text[i]
                            a = soal_text[i+1]
                            b = soal_text[i+2]
                            c = soal_text[i+3]
                            d = soal_text[i+4]
                            kunci = soal_text[i+5].replace('Kunci:', '').strip()
                            
                            soal_baru = Soal(pertanyaan=pertanyaan, opsi_a=a, opsi_b=b, opsi_c=c, opsi_d=d, kunci=kunci)
                            db.session.add(soal_baru)
                            soal_masuk += 1
                            
                    db.session.commit()
                    pesan = f"✅ Berhasil import {soal_masuk} Soal dari Word!"
                except Exception as e:
                    pesan = f"❌ Gagal import soal. Pastikan format template Word benar. Error: {str(e)}"
            else:
                pesan = "❌ Format file tidak sesuai. Gunakan .xlsx untuk siswa dan .docx untuk soal."

    return render_template('import.html', pesan=pesan)

if __name__ == '__main__':
    # Gunakan port dari environment variable (Wajib untuk Railway)
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
