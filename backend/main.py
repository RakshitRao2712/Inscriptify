from __future__ import annotations

from flask import Flask, jsonify, request
from flask_cors import CORS

from app.input.file_handler import process_file
from app.processing.processor import Processor
from app.translation.translator import Translator

app = Flask(__name__)
CORS(app)

processor = Processor()
translator = Translator()


def _serialize_result(file, target_lang: str | None = None) -> dict:
    extracted_text = process_file(file)
    processed = processor.process(
        extracted_text,
        metadata={
            "filename": file.filename,
            "content_type": file.mimetype,
        },
    )

    result = {
        "text": extracted_text,
        "processed": processed,
    }

    if target_lang:
        result["translation"] = translator.translate(processed, target_lang=target_lang)

    return result


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})


@app.route("/upload", methods=["POST"])
def upload():
    file = request.files.get("file")
    if file is None or not file.filename:
        return jsonify({"error": "A file upload is required."}), 400

    try:
        return jsonify(_serialize_result(file))
    except Exception as exc:  # pragma: no cover - defensive API boundary
        return jsonify({"error": str(exc)}), 500


@app.route("/process", methods=["POST"])
def process():
    file = request.files.get("file")
    if file is None or not file.filename:
        return jsonify({"error": "A file upload is required."}), 400

    target_lang = (request.form.get("target_lang") or "").strip() or None

    try:
        return jsonify(_serialize_result(file, target_lang=target_lang))
    except Exception as exc:  # pragma: no cover - defensive API boundary
        return jsonify({"error": str(exc)}), 500


if __name__ == "__main__":
    app.run(debug=True)
