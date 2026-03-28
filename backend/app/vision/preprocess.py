import cv2
import numpy as np
from PIL import Image

def preprocess_image(file):
    file_bytes = np.frombuffer(file.read(),np.uint8)
    img = cv2.imdecode(file_bytes,cv2.IMREAD_COLOR)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray,150,255,cv2.THRESH_BINARY)[1]

    return Image.fromarray(thresh)