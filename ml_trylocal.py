import tensorflow as tf
import cv2
import numpy as np
import tkinter as tk
from tkinter import Label
from PIL import Image, ImageTk

# # Load the TensorFlow Lite model
model = tf.lite.Interpreter(model_path="ssd_mobilenet_v1_1_metadata_1.tflite")
model.allocate_tensors()

# Load labels
with open("labels.txt", "r") as file:
    labels = [line.strip() for line in file.readlines()]

# FUN image processing
def preprocess_image(image_path):
    # Load and preprocess the image
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = cv2.resize(image, (300, 300))
    image = np.expand_dims(image, axis=0)
    image = (image / 255.0).astype(np.uint8)  # Konversi ke UINT8
    return image

# FUN object detection
def detect_objects(image_path):
    image = preprocess_image(image_path)

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

# FUN main
def main():
    image_path = "img\coba4.jpg"
    locations, classes, scores = detect_objects(image_path)

    image_cv2 = cv2.imread(image_path)
    image = cv2.cvtColor(image_cv2, cv2.COLOR_BGR2RGB)

    root = tk.Tk()
    root.title("Detected Objects")
    root.geometry("300x300")

    # Convert the OpenCV image to a format that can be displayed in Tkinter
    image_pil = Image.fromarray(image)
    image_tk = ImageTk.PhotoImage(image=image_pil)

    # Create a label to display the image
    label_image = Label(root, image=image_tk)
    label_image.pack()

    for i in range(len(scores[0])):
        if scores[0][i] > 0.1:
            label = labels[int(classes[0][i])]
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