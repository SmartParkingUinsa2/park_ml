import io
import numpy as np
import tensorflow as tf
from PIL import Image
from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app)

model = tf.lite.Interpreter(model_path='ssd_mobilenet_v1_1_metadata_1.tflite')

with open('labels.txt', 'r') as file:
    labels = file.read().splitlines()

def preprocess_image(image):
    image = image.convert("RGB")
    image = image.resize((300, 300))
    image_array = np.asarray(image)
    processed_image = tf.keras.applications.mobilenet_v2.preprocess_input(image_array)
    processed_image = np.expand_dims(processed_image, axis=0)
    return processed_image

def run_object_detection(image):
    image = preprocess_image(image)

    input_details = model.get_input_details()
    output_details = model.get_output_details()

    model.set_tensor(input_details[0]['index'], image)
    model.invoke()
    locations = model.get_tensor(output_details[0]['index'])
    classes = model.get_tensor(output_details[1]['index'])
    scores = model.get_tensor(output_details[2]['index'])
    numberOfDetections = model.get_tensor(output_details[3]['index'])

    return locations, classes, scores, numberOfDetections

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}

@app.route('/upload', methods=['POST'])
def upload_image():
    try:
        if 'image' not in request.files:
            return jsonify({"error": "No image part"})

        file = request.files['image']

        if file.filename == '':
            return jsonify({"error": "No selected file"})

        if file and allowed_file(file.filename):
            image_data = file.read()
            image = Image.open(io.BytesIO(image_data))

            locations, classes, scores, numberOfDetections = run_object_detection(image)
            detection_results = process_detection_results(locations, classes, scores, numberOfDetections)

            return jsonify("sukses")
        else:
            return jsonify({"error": "Invalid file type. Allowed file types are: png, jpg, jpeg, gif"})
    except FileNotFoundError:
        return jsonify({"error": "Model or label file not found"})
    except Exception as e:
        return jsonify({"error": str(e)})

def process_detection_results(locations, classes, scores, numberOfDetections):
    detection_results = []
    for i in range(int(numberOfDetections[0])):
        if scores[0, i] > 0.5:
            class_id = int(classes[0, i])
            class_label = labels[class_id]
            score = float(scores[0, i])
            bounding_box = locations[0, i].tolist()
            detection_results.append({
                "class": class_label,
                "score": score,
                "bounding_box": bounding_box
            })

    return detection_results

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
