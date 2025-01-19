import streamlit as st
from PIL import Image
import qreader

# Capture image using Streamlit's camera input
enable = st.checkbox("Enable camera")
image_file = st.camera_input("Take a picture")

if image_file is not None:
    image = Image.open(image_file)
    qr_data = qreader.QReader().detect_and_decode(image)
    st.write("QR Code Data:", qr_data)
