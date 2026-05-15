"""
Citation (4/30):
https://flask.palletsprojects.com/en/stable/patterns/fileuploads/
"""
from flask import Flask, request, jsonify
import os
from flask_cors import CORS
import librosa

from webapp.server.config import PORT, MAX_CONTENT_LENGTH, ALLOWED_EXTENSIONS, UPLOAD_DIR, GRAPH_DIR
from webapp.server.services.file_io import save_file
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

@app.route("/api/predict", methods=["POST"])
def upload_file():
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
    print(filepath)
    # Attempt to decode the file as audio - authoritative validation.
    if not decodable_audio_file(filepath):
        os.remove(filepath)
        print(f'received file {filename} rejected: failed to decode')
        return jsonify({"error": "Invalid audio file"}), 400

    print(f'received file: {filename}')

    # Generate graphs
    waveform_graph_path = generate_waveform(filepath)
    spectrum_graph_path = generate_spectrum(filepath)
    spectrograpm_graph_path = generate_spectrogram(filepath)

    # Get genre prediction from inference pipeline

    # Clean up
    os.remove(filepath)
    # TODO remove graphs after return
    
    return jsonify({
        "message": "File uploaded",
        "filename": file.filename,
        # more stuff from inference pipeline goes here
    })


if __name__ == '__main__':
    app.run(port=PORT)
