import tkinter as tk
from tkinter import Label
from PIL import Image, ImageTk
import cv2
import numpy as np
import tensorflow as tf
from tflite_support import metadata as _metadata

# Load the TensorFlow Lite model
model_path = "ssd_mobilenet_v1_1_metadata_1.tflite"

# Load labels
labels_path = "labels.txt"
with open(labels_path, "r") as file:
    labels = [line.strip() for line in file.readlines()]

# Load metadata
model_buffer = open(model_path, "rb").read()
model_meta = _metadata.MetadataPopulator.with_model_file(model_path)
model_meta.load_metadata_buffer(model_buffer)

# Define an image processing function
def preprocess_image(image_path):
    # Load and preprocess the image
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = cv2.resize(image, (300, 300))
    image = np.expand_dims(image, axis=0)
    image = (image / 255.0).astype(np.uint8)  # Konversi ke UINT8
    return image

# Define a function for object detection
def detect_objects(image_path):
    image = preprocess_image(image_path)

    # Perform inference
    interpreter = tf.lite.Interpreter(model_path=model_path)
    interpreter.allocate_tensors()

    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()

    interpreter.set_tensor(input_details[0]['index'], image)
    interpreter.invoke()

    # Get the detection results
    locations = interpreter.get_tensor(output_details[0]['index'])
    classes = interpreter.get_tensor(output_details[1]['index'])
    scores = interpreter.get_tensor(output_details[2]['index'])

    return locations, classes, scores

# Main function
def main():
    image_path = "gambar\coba5.jpg"
    locations, classes, scores = detect_objects(image_path)

    image_cv2 = cv2.imread(image_path)
    image = cv2.cvtColor(image_cv2, cv2.COLOR_BGR2RGB)

    root = tk.Tk()
    root.title("Detected Objects")

    # Convert the OpenCV image to a format that can be displayed in Tkinter
    image_pil = Image.fromarray(image)
    image_tk = ImageTk.PhotoImage(image=image_pil)

    # Create a label to display the image
    label_image = Label(root, image=image_tk)
    label_image.pack()

    for i in range(len(scores[0])):
        if scores[0][i] > 0.1:
            class_idx = int(classes[0][i])
            if class_idx < len(labels):
                label = labels[class_idx]
            else:
                label = 'Unknown'
            confidence = scores[0][i]
            y1, x1, y2, x2 = locations[0][i]
            y1, x1, y2, x2 = int(y1 * image_cv2.shape[0]), int(x1 * image_cv2.shape[1]), int(y2 * image_cv2.shape[0]), int(x2 * image_cv2.shape[1])

            # Create a label to display the detection label and confidence
            label_text = f"{label}: {confidence:.2f}"
            label_detection = Label(root, text=label_text)
            label_detection.pack()

            print(f"Label: {label}, Confidence: {confidence:.2f}")

    root.mainloop()

if __name__ == "__main__":
    main()
