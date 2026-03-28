from flask import Flask, request, jsonify
from flask_cors import CORS
from app.input.file_handler import process_file

app = Flask(__name__)
CORS(app)

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    text = process_file(file)
    return jsonify({"text": text})

if __name__ == '__main__':
    app.run(debug=True)