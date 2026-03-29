from app.vision.preprocess import preprocess_image
from app.utils.clean_text import clean_text
from app.ocr.extractor import extract_text
from app.input.pdf_handler import pdf_to_image
from app.input.video_handler import video_to_frames

def process_file(file):
    print("Processing file:", file.filename)
    
    file.stream.seek(0)
    filename = file.filename.lower()

    if filename.endswith(".pdf"):
        images = pdf_to_image(file)
        full_text = "\n".join(extract_text(img) for img in images)
        return clean_text(full_text)
    
    if filename.endswith((".mp4",".avi",".mov")):
        frames = video_to_frames(file)
        full_text = "\n".join(extract_text(frame) for frame in frames) if frames else "No frames extracted"
        return clean_text(full_text)
    
    image = preprocess_image(file)
    text = extract_text(image)
    return clean_text(text)