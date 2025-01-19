import streamlit as st
from qreader import QReader
import cv2

def readQRcodePicture():
    qreader = QReader()
    image = cv2.cvtColor(cv2.imread(picture), cv2.COLOR_BGR2RGB)
    decoded_text = qreader.detect_and_decode(image=image)
    qtext = decoded_text[0]

enable = st.checkbox("Enable camera")
picture = st.camera_input("Take a picture", disabled=not enable)

if picture:
    st.text(readQRcodePicture())

