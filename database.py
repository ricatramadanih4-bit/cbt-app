from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()

def init_db(app):
    # Mengambil DATABASE_URL dari Railway (PostgreSQL). Jika tidak ada, pakai SQLite.
    db_url = os.getenv('DATABASE_URL', 'sqlite:///cbt_local.db')
    
    # Menyesuaikan string koneksi postgresql untuk SQLAlchemy terbaru
    if db_url.startswith("postgres://"):
        db_url = db_url.replace("postgres://", "postgresql://", 1)
        
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

class Siswa(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nis = db.Column(db.String(50), unique=True, nullable=False)
    nama = db.Column(db.String(100), nullable=False)
    kelas = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(100), nullable=False)

class Soal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pertanyaan = db.Column(db.Text, nullable=False)
    opsi_a = db.Column(db.String(255), nullable=False)
    opsi_b = db.Column(db.String(255), nullable=False)
    opsi_c = db.Column(db.String(255), nullable=False)
    opsi_d = db.Column(db.String(255), nullable=False)
    kunci = db.Column(db.String(10), nullable=False)
