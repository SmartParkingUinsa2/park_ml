from flask import Flask, request
from PIL import Image, ImageDraw, ImageFont
from datetime import date, datetime
import locale
import tensorflow as tf
import numpy as np
import sqlite3
import requests
import os

app = Flask(__name__)

# Load model
model = tf.keras.models.load_model('keras_model.h5')

# assign upload folder
UPLOAD_FOLDER = 'hasildeteksi'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Inisialisasi nomor urut (counter) di luar fungsi
image_counter = 1

@app.route('/upload', methods=['POST'])
def upload_file():
    global image_counter  # Menjadikan image_counter sebagai variabel global

    # Menerima gambar dari permintaan POST
    file = request.files['file']
    img = Image.open(file)

    # Mengubah gambar menjadi array numpy
    img = img.resize((224, 224))  # Mengubah ukuran gambar menjadi (224 x 224)
    img_array = np.array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = img_array / 255.0  # Normalisasi

    # Memprediksi objek dalam gambar
    predictions = model.predict(img_array)
    predictionsmax = np.argmax(predictions)
    class_names = ['bicycle', 'car', 'motorcycle']
    predicted_class = class_names[predictionsmax]

    # Simpan gambar hasil prediksi dengan nama file "image_N.jpg"
    result_folder = 'hasildeteksi'
    os.makedirs(result_folder, exist_ok=True)
    result_image_path = os.path.join(result_folder, f'image_{image_counter}.jpg')

    draw = ImageDraw.Draw(img)
    text = f'Predicted: {predicted_class}'
    font = ImageFont.truetype("arial.ttf", 24)
    draw.text((10, 10), text, font=font, fill='red')

    img.save(result_image_path)

    # Mengincrement nomor urut
    image_counter += 1
    
    # Connect to the database
    conn = sqlite3.connect('db_ml.db')
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
            'jeke': predicted_class,
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