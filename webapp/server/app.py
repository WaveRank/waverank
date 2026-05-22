"""
Citation (4/30):
https://flask.palletsprojects.com/en/stable/patterns/fileuploads/
Citation (5/15):
https://pytutorial.com/flask-send_from_directory-serve-files-securely-from-directories/
"""
from flask import Flask, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
from werkzeug.exceptions import RequestEntityTooLarge
from flask_cors import CORS
from pathlib import Path

from webapp.server.config import PORT, UPLOAD_DIR, GRAPH_DIR, MAX_CONTENT_LENGTH
from webapp.server.services.file_io import create_unique_dir, delete_old_subdirs
from webapp.server.services.audio_validation import allowed_file
from webapp.server.services.audio_processing import process_audio_file
from webapp.server.services.youtube import download_youtube_audio
from shared.audio_utils import load_audio
from visualizations.waveform.waveform import generate_waveform
from visualizations.spectrum.spectrum import generate_spectrum
from visualizations.spectrogram.spectrogram import generate_spectrogram

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH

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


@app.errorhandler(RequestEntityTooLarge)
def handle_large_file(error):
    # Replace default error behavior of flask.request for overly large files
    print(f'rejected file: file exceeds maximum size')
    return jsonify({"error": "File exceeds maximum size"}), 413

@app.route("/api/audio/<path:audio_path>")
def serve_audio(audio_path):
    return send_from_directory(UPLOAD_DIR, audio_path)

@app.route("/api/sentLink", methods=["POST"])
def handle_youtube_link():
    # Extract URL from request
    data = request.get_json()
    if data == None or 'URL' not in data:
        return jsonify({"error": "YouTube link missing"}), 400

    # Extract audio from youtube, which saves to disk
    try:
        filepath, filename = download_youtube_audio(data['URL'])
    except Exception as e:
        print("YouTube download failed:", repr(e))
        return jsonify({"error": "Invalid audio file"}), 400
    
    # Process the file
    response_data, status = process_audio_file(filepath, filename)
    if status != 200:
        return jsonify(response_data), status
    
    # Complete and return response data
    response_data["audio"] = (
        f"{request.host_url.rstrip('/')}/api/audio/{filepath.parent.name}/audio.mp3"
    )

    return jsonify(response_data)


@app.route("/api/predict", methods=["POST"])
def handle_uploaded_file():
    # Extract uploaded file
    if 'file' not in request.files:
        return jsonify({"error": "File to upload doesn't exist"}), 400

    file = request.files['file']
    raw_filename = file.filename.strip()

    # Reject files with no base name
    if raw_filename == '' or raw_filename.startswith('.'):
        print(f'rejected file "{raw_filename}": no base filename')
        return jsonify({"error": "Invalid filename"}), 400

    # Reject obviously invalid file types
    if not allowed_file(raw_filename):
        print(f'rejected file "{raw_filename}": file type not allowed')
        return jsonify({"error": "Invalid file type"}), 400

    # Sanitize filename
    filename = secure_filename(raw_filename)

    # Save to disk in randomly generated folder to avoid filename collisions
    new_upload_subdir = create_unique_dir(UPLOAD_DIR)
    filepath = UPLOAD_DIR / new_upload_subdir / filename
    file.save(filepath)

    
    # Process the file
    response_data, status = process_audio_file(filepath, filename)
    if status != 200:
        return jsonify(response_data), status
    
    # Complete and return response data
    response_data["audio"] = (
        f"{request.host_url.rstrip('/')}/api/audio/{filepath.parent.name}/{filename}"
    )

    return jsonify(response_data)

if __name__ == '__main__':
    delete_old_subdirs(GRAPH_DIR)
    app.run(port=PORT)
