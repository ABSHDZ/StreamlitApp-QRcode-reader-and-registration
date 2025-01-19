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
name_to_check = "Hola"

# Picture
uploaded_file = st.camera_input("Take a picture")

def validate_and_update_name(df, name_to_check):
    # Check if the name exists in the NombreCompleto column
    if name_to_check in df['NombreCompleto'].values:
        # Find the index of the row where the name matches
        idx = df[df['NombreCompleto'] == name_to_check].index[0]

        # Check if the Payment column is empty
        if df.at[idx, 'Payment'] == "":
            df.at[idx, 'Payment'] = "Paid"  # Update the value
            return True  # Indicate that an update was made
    return False  # No update needed

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
    updated = validate_and_update_name(df, name_to_check)
    if updated:
        # Write the updated DataFrame back to the Google Sheet
        conn.write(df, worksheet="DatosForms")
        st.success(f"Payment status updated for {name_to_check}.")
    else:
        st.warning(f"No update needed for {name_to_check} (name not found or already paid).")

