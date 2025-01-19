import streamlit as st
import pyzbar

enable = st.checkbox("Enable camera")
picture = st.camera_input("Take a picture", disabled=not enable)

def readQRcodePicture():
    image = cv2.imread(picture)
    decoded = pyzbar.decode(image)
    st.text(decoded.data)

if picture:
    readQRcodePicture()

