"""
Citation (4/30):
https://flask.palletsprojects.com/en/stable/patterns/fileuploads/
Citation (5/15):
https://pytutorial.com/flask-send_from_directory-serve-files-securely-from-directories/
"""
from flask import Flask, request, jsonify, send_from_directory
import os
from flask_cors import CORS
import librosa

from webapp.server.config import PORT, MAX_CONTENT_LENGTH, ALLOWED_EXTENSIONS, UPLOAD_DIR, GRAPH_DIR
from webapp.server.services.file_io import save_file, delete_old_files
from webapp.server.services.audio_validation import allowed_file, decodable_audio_file
from shared.audio_utils import load_audio
from visualizations.waveform.waveform import generate_waveform
from visualizations.spectrum.spectrum import generate_spectrum
from visualizations.spectrogram.spectrogram import generate_spectrogram

app = Flask(__name__)
CORS(app)

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(GRAPH_DIR, exist_ok=True)


# ----- ROUTES -----
@app.route('/')
def main():
    return "I work!"


@app.route("/api/graphs/<path:filename>")
def serve_graph(filename):
    return send_from_directory(GRAPH_DIR, filename)


@app.route("/api/predict", methods=["POST"])
def handle_uploaded_file():
    # Extract uploaded file
    if 'file' not in request.files:
        return jsonify({"error": "File to upload doesn't exist"}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400
    
    # Reject obviously invalid files
    if not allowed_file(file.filename):
        print(f'received file {filename} rejected: file type not allowed')
        return jsonify({"error": "Invalid file type"}), 400

    filename, filepath = save_file(file)
     
    # Attempt to decode the file as audio - authoritative validation.
    if not decodable_audio_file(filepath):
        os.remove(filepath)
        print(f'received file {filename} rejected: failed to decode')
        return jsonify({"error": "Invalid audio file"}), 400

    print(f'received file: {filename}')

    # Generate graphs and save to disk. Client will GET query for them. 
    waveform_filename = generate_waveform(filepath)
    spectrum_filename = generate_spectrum(filepath)
    spectrogram_filename = generate_spectrogram(filepath)

    # Get genre prediction from inference pipeline
    # TODO maybe look into handling this asynchronously, graph generation too

    # Delete the uploaded file and graphs older than the age limit
    os.remove(filepath)
    delete_old_files(GRAPH_DIR)
    
    base_url = request.host_url.rstrip("/")

    return jsonify({
        "message": "File uploaded",
        "filename": filename,
        "graphs": {
            "waveform": f"{base_url}/api/graphs/{waveform_filename}",
            "spectrum": f"{base_url}/api/graphs/{spectrum_filename}",
            "spectrogram": f"{base_url}/api/graphs/{spectrogram_filename}"
        # "genres": {}
        }
    })


if __name__ == '__main__':
    list_of_files = os.listdir(GRAPH_DIR)
    print("list of files: ", list_of_files)
    delete_old_files(GRAPH_DIR)
    app.run(port=PORT)
