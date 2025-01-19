import streamlit as st
import cv2
import numpy as 
from PIL import Image

# File uploader
uploaded_file = st.camera_input("Take a picture")

if uploaded_file is not None:
    # Convert the uploaded image to a format suitable for OpenCV
    image = Image.open(uploaded_file)
    image_np = np.array(image)

    # Convert to grayscale
    gray_image = cv2.cvtColor(image_np, cv2.COLOR_BGR2GRAY)

    # Create a QRCodeDetector
    detector = cv2.QRCodeDetector()

    # Detect and decode the QR code
    data, points, _ = detector.detectAndDecode(gray_image)

    # Display the result
    if data:
        st.write("QR Code Data:", data)
    else:
        st.write("No QR code found in the image.")