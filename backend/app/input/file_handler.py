from app.vision.preprocess import preprocess_image
from app.ocr.extractor import extract_text

def process_file(file):
    file.stream.seek(0)
    image = preprocess_image(file)
    text = extract_text(image)
    return text