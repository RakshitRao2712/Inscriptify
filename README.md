# Inscriptify
Extract. Understand. Structure.

A tool to extract text from images, videos and PDFs.

## Features
- Raw text extraction
- File input (image, video, and PDFs)

## Tech Stack
- React (Frontend)
- Flask (Backend)

## Project Structure
- `backend/` Flask API for OCR, text processing, and translation
- `frontend/` React + Vite client for uploads and result visualization

## Run Locally
### Backend
```bash
cd backend
pip install -r requirements.txt
python main.py
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

The frontend expects the Flask API at `http://127.0.0.1:5000` by default. You can override it with `VITE_API_BASE_URL`.
