import os
import pandas as pd
from docx import Document
from flask import Flask, render_template, request, redirect, url_for, session, flash
from database import db, init_db, Siswa, Soal

app = Flask(__name__)
app.secret_key = "cbt_super_secret_key"

init_db(app)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    if 'siswa_id' in session:
        return redirect(url_for('ujian'))
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    user_input = request.form.get('nis', '').strip()
    pass_input = request.form.get('password', '').strip()
    
    if not user_input:
        flash('Silakan masukkan NIS atau Nama Siswa!')
        return redirect(url_for('index'))
    
    # Bisa login menggunakan NIS ATAU Nama Lengkap (bebas huruf besar/kecil)
    siswa = Siswa.query.filter(
        (db.func.lower(Siswa.nis) == user_input.lower()) | 
        (db.func.lower(Siswa.nama) == user_input.lower())
    ).first()
    
    if siswa:
        if not pass_input or pass_input.lower() == siswa.password.lower() or pass_input.lower() == siswa.nis.lower() or pass_input.lower() == siswa.nama.lower():
            session['siswa_id'] = siswa.id
            session['nama'] = siswa.nama
            session['kelas'] = siswa.kelas
            return redirect(url_for('ujian'))
            
    flash('NIS / Nama atau Password tidak ditemukan dalam sistem!')
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/ujian')
def ujian():
    if 'siswa_id' not in session:
        return redirect(url_for('index'))
    soal_list = Soal.query.all()
    return render_template('ujian.html', nama=session['nama'], kelas=session['kelas'], daftar_soal=soal_list)

@app.route('/submit', methods=['POST'])
def submit():
    if 'siswa_id' not in session:
        return redirect(url_for('index'))
    
    soal_list = Soal.query.all()
    nilai = 0
    total = len(soal_list)
    
    for soal in soal_list:
        jawaban_siswa = request.form.get(f'soal_{soal.id}')
        if jawaban_siswa and jawaban_siswa.strip().upper() == soal.kunci.strip().upper():
            nilai += 1
            
    skor = round((nilai / total) * 100, 2) if total > 0 else 0
    nama = session['nama']
    session.clear()
    return render_template('hasil.html', nama=nama, nilai=nilai, total=total, skor=skor)

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
                    df = pd.read_excel(file, dtype=str)
                    
                    col_map = {}
                    for col in df.columns:
                        c_upper = str(col).strip().upper()
                        if 'NIS' in c_upper:
                            col_map['nis'] = col
                        elif 'NAMA' in c_upper:
                            col_map['nama'] = col
                        elif 'KELAS' in c_upper:
                            col_map['kelas'] = col
                        elif 'PASS' in c_upper:
                            col_map['password'] = col

                    nis_col = col_map.get('nis')
                    nama_col = col_map.get('nama')
                    kelas_col = col_map.get('kelas')
                    pass_col = col_map.get('password')

                    if not nis_col or not nama_col:
                        pesan = "❌ Kolom NIS atau Nama tidak ditemukan di file Excel!"
                    else:
                        jumlah_berhasil = 0
                        for _, row in df.iterrows():
                            nis = str(row[nis_col]).split('.')[0].strip() if pd.notnull(row[nis_col]) else ''
                            nama = str(row[nama_col]).strip() if pd.notnull(row[nama_col]) else ''
                            kelas = str(row[kelas_col]).strip() if (kelas_col and pd.notnull(row[kelas_col])) else '-'
                            password = str(row[pass_col]).split('.')[0].strip() if (pass_col and pd.notnull(row[pass_col])) else nis
                            
                            if nis and nama and nis.lower() != 'nan' and nama.lower() != 'nan':
                                siswa_baru = Siswa(nis=nis, nama=nama, kelas=kelas, password=password)
                                db.session.add(siswa_baru)
                                try:
                                    db.session.commit()
                                    jumlah_berhasil += 1
                                except Exception:
                                    db.session.rollback()
                        
                        pesan = f"✅ Berhasil mengimpor {jumlah_berhasil} data siswa ke database!"
                except Exception as e:
                    pesan = f"❌ Gagal import siswa: {e}"

            elif tipe == 'soal' and file.filename.endswith('.docx'):
                try:
                    doc = Document(file)
                    soal_text = [p.text.strip() for p in doc.paragraphs if p.text.strip()]
                    
                    soal_masuk = 0
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
                            try:
                                db.session.commit()
                                soal_masuk += 1
                            except Exception:
                                db.session.rollback()
                            
                    pesan = f"✅ Berhasil import {soal_masuk} Soal dari Word!"
                except Exception as e:
                    pesan = f"❌ Gagal import soal: {str(e)}"
            else:
                pesan = "❌ Format file tidak sesuai."

    total_siswa = Siswa.query.count()
    total_soal = Soal.query.count()
    daftar_siswa = Siswa.query.limit(20).all()

    return render_template('import.html', pesan=pesan, total_siswa=total_siswa, total_soal=total_soal, daftar_siswa=daftar_siswa)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
