from flask import Flask, request, jsonify
from flask_cors import CORS
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
from PIL import Image
import cv2
import numpy as np

app = Flask(__name__)
CORS(app)

def preprocess_image(file):
    file_bytes = np.frombuffer(file.read(),np.uint8)
    img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    
    gray = cv2.cvtColor(img, cv2.IMREAD_COLOR)
    thresh = cv2.threshold(gray,150,255,cv2.THRESH_BINARY)[1]

    return Image.fromarray(thresh)

@app.route('/upload',methods=['POST'])
def upload():
    file = request.files['file']
    file.stream.seek(0)
    image = preprocess_image(file)
    text = pytesseract.image_to_string(image)

    return jsonify({"text":text})

if __name__ == '__main__':
    app.run(debug=True)