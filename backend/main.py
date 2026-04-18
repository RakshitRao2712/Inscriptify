from flask import Flask, request, jsonify
from flask_cors import CORS

from app.input.file_handler import process_file
from app.processing.processor import Processor

app = Flask(__name__)
CORS(app)

processor = Processor()

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']

    raw_text = process_file(file)
    processed = processor.process(raw_text)

    return jsonify({
        "raw_text": raw_text,
        "processed": processed
    })

if __name__ == '__main__':
    app.run(debug=True)