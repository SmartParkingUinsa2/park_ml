from flask import Flask, request
from PIL import Image, ImageDraw, ImageFont
from datetime import date, datetime
import locale
import sqlite3
import requests
import os
import cv2
import numpy as np

app = Flask(__name__)

# Load YOLO
net = cv2.dnn.readNet("yolov4.weights", "yolov4.cfg")
classes = []
with open("coco.names", "r") as f:
    classes = [line.strip() for line in f.readlines()]
layer_names = net.getUnconnectedOutLayersNames()

# assign upload folder
UPLOAD_FOLDER = 'hasildeteksi'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Inisialisasi nomor urut (counter) di luar fungsi
image_counter = 1

# Define the classes to detect: car, motorbike, and bicycle
classes_to_detect = ["car", "motorbike", "bicycle"]

@app.route('/upload', methods=['POST'])
def upload_file():
    global image_counter  # Menjadikan image_counter sebagai variabel global

    # Menerima gambar dari permintaan POST
    file = request.files['file']
    img = Image.open(file)

    # Simpan gambar hasil prediksi dengan nama file "image_N.jpg"
    result_folder = 'hasildeteksi'
    os.makedirs(result_folder, exist_ok=True)
    result_image_path = os.path.join(result_folder, f'image_{image_counter}.jpg')

    # Convert PIL image to OpenCV format
    opencv_image = np.array(img)
    opencv_image = cv2.cvtColor(opencv_image, cv2.COLOR_RGB2BGR)

    # Preprocess image for YOLO
    height, width, _ = opencv_image.shape
    blob = cv2.dnn.blobFromImage(opencv_image, 1/255.0, (416, 416), swapRB=True, crop=False)
    net.setInput(blob)

    # Forward pass
    outs = net.forward(layer_names)

    # Post-process detection results
    conf_threshold = 0.5
    nms_threshold = 0.4

    boxes = []
    confidences = []
    class_ids = []

    # Initialize class-specific counts
    class_counts = {class_name: 0 for class_name in classes_to_detect}

    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]

            if confidence > conf_threshold and classes[class_id] in classes_to_detect:
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)

                x = int(center_x - w / 2)
                y = int(center_y - h / 2)

                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)

                # Increment the class-specific count
                class_name = classes[class_id]
                class_counts[class_name] += 1

    # Apply non-maximum suppression
    indices = cv2.dnn.NMSBoxes(boxes, confidences, conf_threshold, nms_threshold)

    # Draw bounding boxes on the image and add text annotations
    for i in indices:
        i = i[0] if isinstance(i, list) else i
        box = boxes[i]
        x, y, w, h = box
        label = str(classes[class_ids[i]])
        confidence = confidences[i]
        color = (0, 255, 0)  # Green color for the bounding box
        cv2.rectangle(opencv_image, (x, y), (x + w, y + h), color, 2)
        cv2.putText(opencv_image, f"{label} {confidence:.2f}", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

    # Add text annotations for vehicle counts
    for class_name, count in class_counts.items():
        cv2.putText(opencv_image, f"{class_name} Count: {count}", (10, 30 + 20 * classes_to_detect.index(class_name)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        if count != 0:
            real_class_name = class_name
            real_count = count

    # Save vehicle counts to a text file
    with open("jumlah_kendaraan.txt", "w") as file:
        file.write("\n".join([f"{class_name} Count: {count}" for class_name, count in class_counts.items()]))

    # Convert OpenCV image back to PIL format
    pil_image = Image.fromarray(cv2.cvtColor(opencv_image, cv2.COLOR_BGR2RGB))

    # Save the result image
    pil_image.save(result_image_path)

    # Mengincrement nomor urut
    image_counter += 1
    
    # Connect to the database
    conn = sqlite3.connect('db_ml.db')
    cursor = conn.cursor()

    # Insert data into the "gambar" table
    img_path = os.path.join(UPLOAD_FOLDER, file.name)
    img_size = 1048576
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
            'jeke': real_class_name,  # Replace with any default value
            'juke': real_count}

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