import cv2
import tempfile
from PIL import Image
import os

def video_to_frames(file, interval=120):
    temp = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
    
    # Flask is causing issues with temp files
    # file.save(temp.name)
    # temp.close()

    #Writing file manually
    temp.write(file.read())
    temp.close()
    
    cap = cv2.VideoCapture(temp.name)
    if not cap.isOpened():
        os.remove(temp.name)
        return []
    
    frames = []
    count = 0

    while True:
        ret,frame = cap.read()
        if not ret:
            break
        
        if count % interval == 0:
            frame_rgb = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
            image = Image.fromarray(frame_rgb)
            frames.append(image)
        
        count+=1
    cap.release()
    os.remove(temp.name)

    return frames