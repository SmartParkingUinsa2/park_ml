from flask import Flask, request
from datetime import date, datetime
import locale
import sqlite3
import requests
import os

app = Flask(__name__)

# assign upload folder
UPLOAD_FOLDER = 'img2'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename)) # put file into folder
    
    # Connect to the database
    conn = sqlite3.connect('db_dummy_ml.db')
    cursor = conn.cursor()

    # Insert data into the "gambar" table
    img_path = f"{UPLOAD_FOLDER}\{file.filename}"
    img_size = file.content_length / 1048576
    cursor.execute("INSERT INTO gambar (path_gambar, size_gambar) VALUES (?, ?)", (img_path, img_size))

    # Insert data into the "deteksi" table
    locale.setlocale(locale.LC_TIME, 'id_ID')
    now = datetime.now()

    cursor.execute("SELECT MAX(id_gambar) FROM gambar")
    result = cursor.fetchone()
    current_id_gambar = result[0]

    data = {'img_id': current_id_gambar,
            'tahun': now.year,
            'bulan': now.month,
            'tanggal': now.day,
            'hari': date.today().strftime('%A'),
            'jam': now.hour,
            'area': "FST",
            'jeke': "mobil",
            'juke': 150,}
    
    img_id = data['img_id']
    tahun = data['tahun']
    bulan = data['bulan']
    tanggal = data['tanggal']
    hari = data['hari']
    jam = data['jam']
    area = data['area']
    jeke = data['jeke']
    juke = data['juke']
    cursor.execute("INSERT INTO deteksi (id_gambar, tahun, bulan, tanggal, hari, jam, area, jenis_kendaraan, jumlah_kendaraan) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                  (img_id, tahun, bulan, tanggal, hari, jam, area, jeke, juke))

    # Commit the changes to the database
    conn.commit()

    # Close the connection
    conn.close()

    # send data to db server
    url = 'https://xpqht97q-5001.asse.devtunnels.ms/store'
    requests.post(url, json=data)

    return "data_saved"

# run flask app
if __name__ == '__main__':
    app.run(port=5000)