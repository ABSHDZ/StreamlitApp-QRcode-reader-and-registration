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
registrer = conn.read(worksheet="Sabado")
registrer2 = conn.read(worksheet="Sabado2")
df = pd.DataFrame(existing_data)
# Picture
enable = st.checkbox("Enable camera")
uploaded_file = st.camera_input("Take a picture", disabled=not enable)
Nombre = "Hola"

def get_payment_for_name(df, name_to_check):
    st.cache_data.clear()
    conn = st.connection("gsheets", type=GSheetsConnection)
    existing_data = conn.read(worksheet="DatosForms")
    df = pd.DataFrame(existing_data)
    # Check if the name exists in the NameList column
    if name_to_check in df['NombreCompleto'].values:
        # Find the index of the row where the name matches
        idx = df[df['NombreCompleto'] == name_to_check].index[0]
        return df.at[idx, 'Pago']  # Return the value in the Asistencia column
    else:
        return None  # Name not found

def registerABS():
    st.cache_data.clear()
    conn = st.connection("gsheets", type=GSheetsConnection)
    registrer = conn.read(worksheet="Sabado")
    if Nombre in registrer["NombreCompleto"].values:
        st.warning("AlreadyExist")
        st.stop()
    else:
        new_to_add = pd.DataFrame([{"NombreCompleto": Nombre}])
        update_row = pd.concat([registrer, new_to_add], ignore_index=False)
        conn.update(worksheet="Sabado", data=update_row)
        st.success("Data updated successfully")

def registerABS2():
    st.cache_data.clear()
    conn = st.connection("gsheets", type=GSheetsConnection)
    registrer2 = conn.read(worksheet="Sabado2")
    if Nombre in registrer2["NombreCompleto"].values:
        st.warning("AlreadyExist")
        st.stop()
    else:
        new_to_add = pd.DataFrame([{"NombreCompleto": Nombre}])
        update_row = pd.concat([registrer2, new_to_add], ignore_index=False)
        conn.update(worksheet="Sabado2", data=update_row)
        st.success("Data updated successfully")

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
        Nombre = data
        st.write("QR Code Data:", data)
        checkingPay = get_payment_for_name(df, data)
        if checkingPay is not None:
            st.success(f"Payment for {data}: {checkingPay}")
            registerABS()
        else:
            st.warning(f"{data} not found in the NameList.")
            registerABS2()
    else:
        st.write("No QR code found in the image.")
