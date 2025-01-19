import streamlit as st
#Decode qr code
import cv2
import numpy as np
from PIL import Image
#Save data in google sheet
from streamlit_gsheets import GSheetsConnection
import pandas as pd

#Read google sheet
conn = st.connection("gsheets", type=GSheetsConnection)
existing_data = conn.read(worksheet="DatosForms")
df = pd.DataFrame(existing_data)

# Picture
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
        name_to_check = data
    else:
        st.write("No QR code found in the image.")

if st.button("Validate and Update"):
    st.dataframe(df)
