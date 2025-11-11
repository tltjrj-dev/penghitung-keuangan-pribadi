from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# --- Konfigurasi Database ---
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(BASE_DIR, 'keuangan.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# --- Model Database ---
class Transaksi(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tipe = db.Column(db.String(20), nullable=False)
    jumlah = db.Column(db.Float, nullable=False)
    kategori = db.Column(db.String(50), nullable=False)
    catatan = db.Column(db.String(100))

# --- Inisialisasi Database ---
with app.app_context():
    db.create_all()

# --- Routes ---
@app.route('/')
def index():
    transaksi = Transaksi.query.all()
    total_pemasukan = sum(t.jumlah for t in transaksi if t.tipe == 'pemasukan')
    total_pengeluaran = sum(t.jumlah for t in transaksi if t.tipe == 'pengeluaran')
    saldo = total_pemasukan - total_pengeluaran
    return render_template('index.html', transaksi=transaksi, saldo=saldo)

@app.route('/tambah', methods=['GET', 'POST'])
def tambah():
    if request.method == 'POST':
        tipe = request.form['tipe']
        jumlah = float(request.form['jumlah'])
        kategori = request.form['kategori']
        catatan = request.form['catatan']

        transaksi_baru = Transaksi(
            tipe=tipe,
            jumlah=jumlah,
            kategori=kategori,
            catatan=catatan
        )
        db.session.add(transaksi_baru)
        db.session.commit()

        return redirect(url_for('index'))
    return render_template('tambah.html')

@app.route('/hapus/<int:id>')
def hapus(id):
    transaksi = Transaksi.query.get_or_404(id)
    db.session.delete(transaksi)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
