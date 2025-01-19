import streamlit as st
import qrtools


def readQRcodePicture():
    qr = qrtools.QR()
    qr.decode("bookmark.png")
    st.text(qr.data)

enable = st.checkbox("Enable camera")
picture = st.camera_input("Take a picture", disabled=not enable)

if picture:
    readQRcodePicture()

