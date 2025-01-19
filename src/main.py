import streamlit as st
from pyzbar.pyzbar import decode
from PIL import Image

enable = st.checkbox("Enable camera")
picture = st.camera_input("Take a picture", disabled=not enable)

def readQRcodePicture():
    try:
    qr_code = decode(picture)[0]
    contenQr = qr_code.data.decode("utf-8")
    st.text(contenQr)
    except Exception as err:
    st.text(str(err))

if picture:
    readQRcodePicture()

