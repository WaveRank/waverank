"""
Citation (4/30):
https://flask.palletsprojects.com/en/stable/patterns/fileuploads/
"""
from flask import Flask, request, jsonify
import os
from werkzeug.utils import secure_filename
from flask_cors import CORS
import librosa


PORT = 5137
UPLOAD_FOLDER = "../uploads"
ALLOWED_EXTENSIONS = {'wav', 'mp3', 'mp4'}
MAX_CONTENT_LENGTH = 10 * 1024 * 1024  # 10MB 


app = Flask(__name__)
CORS(app)

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Performs a fast, non-secure extension check.
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# ----- ROUTES -----
@app.route('/')
def main():
    return "I work!"

@app.route("/api/predict", methods=["POST"])
def upload_file():
    # Extract uploaded file
    if 'file' not in request.files:
        return jsonify({"error": "File to upload doesn't exist"}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400
    
    # Fast extension check (early rejection of obvious invalid inputs)
    if not allowed_file(file.filename):
        return jsonify({"error": "Invalid file type"}), 400

    # Sanitize filename to prevent path traversal or unsafe characters
    filename = secure_filename(file.filename)

    # Save file to disk for downstream processing
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    # Attempt to decode the file as audio - authoritative validation.
    # Only a short duration is loaded to reduce processing cost.
    try:
        librosa.load(filepath, duration=5)
    except Exception:
        os.remove(filepath)  # Avoid storing unusable or malicious data
        return jsonify({"error": "Invalid audio file"}), 400

    # TODO
    # Convert to .wav
    # Send to inference pipeline
    # Receive stuff from inference pipeline
    return jsonify({
        "message": "File uploaded",
        "filename": file.filename
        # more stuff from inference pipeline goes here
    })


if __name__ == '__main__':
    app.run(port=PORT)
