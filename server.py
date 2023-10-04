import tensorflow as tf
from flask import Flask, request, jsonify
import numpy as np
import cv2
from PIL import Image
import io

# Load the TensorFlow Lite model
model_path = "ssd_mobilenet_v1_1_metadata_1.tflite"
model = tf.lite.Interpreter(model_path=model_path)
model.allocate_tensors()

# Load labels
with open("labels.txt", "r") as file:
    labels = [line.strip() for line in file.readlines()]

# Define an image processing function
def preprocess_image(image_data):
    try:
        # Decode the image data and open it with Pillow
        image = Image.open(io.BytesIO(image_data))
        image = image.convert("RGB")

        # Resize and normalize the image
        image = image.resize((300, 300))
        image = np.array(image) / 255.0
        image = np.expand_dims(image, axis=0).astype(np.float32)
        
        return image
    except Exception as e:
        return None

# Define a function for object detection
def detect_objects(image_data):
    image = preprocess_image(image_data)

    if image is None:
        return [], [], []

    # Perform inference
    input_details = model.get_input_details()
    output_details = model.get_output_details()

    model.set_tensor(input_details[0]['index'], image)
    model.invoke()

    # Get the detection results
    locations = model.get_tensor(output_details[0]['index'])
    classes = model.get_tensor(output_details[1]['index'])
    scores = model.get_tensor(output_details[2]['index'])

    return locations, classes, scores

# Create a Flask app
app = Flask(__name__)

@app.route("/deteksi", methods=["POST"])
def index():
    if request.method == "POST":
        # Receive the image data from the Android app
        image_data = request.data

        # Detect objects in the received image data
        locations, classes, scores = detect_objects(image_data)

        # Check if there are any detection results
        if not scores or len(scores) == 0 or len(scores[0]) == 0:
            return jsonify({"results": [], "message": "No objects detected."})

        # Prepare and send the detection results along with a message as JSON response
        results = []
        for i in range(len(scores[0])):
            if scores[0][i] > 0.1:
                label = labels[int(classes[0][i])]
                confidence = scores[0][i]
                results.append({"label": label, "confidence": float(confidence)})

        # Include a message in the response
        message = "Object detection completed."

        # Create a dictionary containing both the results and the message
        response_data = {"results": results, "message": message}

        return jsonify(response_data)

    
if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0', port=5000)
