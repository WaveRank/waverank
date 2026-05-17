"""
Citation (4/30):
https://flask.palletsprojects.com/en/stable/patterns/fileuploads/
Citation (5/15):
https://pytutorial.com/flask-send_from_directory-serve-files-securely-from-directories/
"""
from flask import Flask, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
import os
from flask_cors import CORS
import librosa

from webapp.server.config import PORT, MAX_CONTENT_LENGTH, ALLOWED_EXTENSIONS, UPLOAD_DIR, GRAPH_DIR
from webapp.server.services.file_io import create_unique_dir, delete_old_subdirs
from webapp.server.services.audio_validation import allowed_file, decodable_audio_file
from shared.audio_utils import load_audio
from visualizations.waveform.waveform import generate_waveform
from visualizations.spectrum.spectrum import generate_spectrum
from visualizations.spectrogram.spectrogram import generate_spectrogram

app = Flask(__name__)
CORS(app)

UPLOAD_DIR.mkdir(exist_ok=True)
GRAPH_DIR.mkdir(exist_ok=True)


# ----- ROUTES -----
@app.route('/')
def main():
    return "I work!"


@app.route("/api/graphs/<path:graph_path>")
def serve_graph(graph_path):
    return send_from_directory(GRAPH_DIR, graph_path)


@app.route("/api/predict", methods=["POST"])
def handle_uploaded_file():
    # Extract uploaded file
    if 'file' not in request.files:
        return jsonify({"error": "File to upload doesn't exist"}), 400

    file = request.files['file']
    filename = secure_filename(file.filename)

    if file == '':
        return jsonify({"error": "No file selected"}), 400
    
    # Reject obviously invalid files
    if not allowed_file(filename):
        print(f'received file {filename} rejected: file type not allowed')
        return jsonify({"error": "Invalid file type"}), 400

    # Save to disk in randomly generated folder to avoid filename collisions
    new_upload_subdir = create_unique_dir(UPLOAD_DIR)
    filepath = UPLOAD_DIR / new_upload_subdir / filename
    file.save(filepath)
     
    # Attempt to decode the file as audio - authoritative validation.
    if not decodable_audio_file(filepath):
        os.remove(filepath)
        print(f'received file {filename} rejected: failed to decode')
        return jsonify({"error": "Invalid audio file"}), 400

    print(f'received file: {filename}')

    # Generate graphs and save to disk. Client will GET query for them. 
    new_graph_subdir = create_unique_dir(GRAPH_DIR)
    waveform_filename = generate_waveform(filepath, GRAPH_DIR / new_graph_subdir)
    spectrum_filename = generate_spectrum(filepath, GRAPH_DIR / new_graph_subdir)
    spectrogram_filename = generate_spectrogram(filepath, GRAPH_DIR / new_graph_subdir)

    # Get genre prediction from inference pipeline
    # TODO maybe look into handling this asynchronously, graph generation too

    # Delete the uploaded file and graphs older than the age limit
    os.remove(filepath)
    delete_old_subdirs(GRAPH_DIR)
    
    base_url = request.host_url.rstrip("/")

    return jsonify({
        "message": "File uploaded",
        "filename": filename,
        "graphs": {
            "waveform": f"{base_url}/api/graphs/{new_graph_subdir}/{waveform_filename}",
            "spectrum": f"{base_url}/api/graphs/{new_graph_subdir}/{spectrum_filename}",
            "spectrogram": f"{base_url}/api/graphs/{new_graph_subdir}/{spectrogram_filename}"
        # "genres": {}
        }
    })


if __name__ == '__main__':
    delete_old_subdirs(GRAPH_DIR)
    app.run(port=PORT)
