from app.vision.preprocess import preprocess_image
from app.ocr.extractor import extract_text
from app.input.pdf_handler import pdf_to_image
from app.input.video_handler import video_to_frames

def process_file(file):
    file.stream.seek(0)
    filename = file.filename.lower()

    if filename.endswith(".pdf"):
        images = pdf_to_image(file)
        return "\n".join(extract_text(img) for img in images)
    
    if filename.endswith((".mp4",".avi",".mov")):
        frames = video_to_frames(file)
        return "\n".join(extract_text(frame) for frame in frames) if frames else "No frames extracted"
    
    image = preprocess_image(file)
    return extract_text(image)