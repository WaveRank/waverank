"""
Audio processing service for the backend audio-processing pipeline used by
upload and YouTube endpoints, including:
- audio decoding and validation
- waveform/spectrum/spectrogram generation
- file cleanup
- response metadata generation
"""
from pathlib import Path
from flask import request

from shared.paths import GRAPH_DIR, UPLOAD_DIR
from webapp.server.services.file_io import create_unique_dir, delete_old_subdirs
from webapp.server.services.inference import predict_genre
from model.src.audio.audio_utils import load_audio
from visualizations.waveform.waveform import generate_waveform
from visualizations.spectrum.spectrum import generate_spectrum
from visualizations.spectrogram.spectrogram import generate_spectrogram

def process_audio_file(filepath, filename):
    """
    Validates audio, generates graphs, and returns response data.

    Returns:
        tuple(response_data, status_code)
    """

    # Attempt to decode the file as audio - authoritative validation
    y, sr = load_audio(filepath)

    if y is None:
        filepath.unlink()
        print(f'rejected file "{filename}": failed to decode')
        return {"error": "Invalid audio file"}, 400

    print(f'received file: "{filename}"')

    # Generate graphs and save to disk
    new_graph_subdir = create_unique_dir(GRAPH_DIR)
    output_dir = GRAPH_DIR / new_graph_subdir

    file_basename = Path(filename).stem
    waveform_filename = file_basename + "_waveform.png"
    spectrum_filename = file_basename + "_spectrum.png"
    spectrogram_filename = file_basename + "_spectrogram.png"

    try:
        generate_waveform(y, sr, output_dir / waveform_filename)
        generate_spectrum(y, sr, output_dir / spectrum_filename)
        generate_spectrogram(y, sr, output_dir / spectrogram_filename)

    except Exception as e:
        filepath.unlink()
        print("Graph generation failed:", repr(e))
        return {"error": "Error generating graphs"}, 500

    # TODO Get genre prediction from inference pipeline
    # TODO maybe look into handling this asynchronously
    # genre_prediction = predict_genre(filepath)


    # Cleanup the uploads and graphs older than the age limit
    try:
        delete_old_subdirs(GRAPH_DIR)
        delete_old_subdirs(UPLOAD_DIR)
    except Exception as e:
        print("Cleanup failed:", repr(e))

    # Build partial response
    server_url = request.host_url.rstrip("/")

    response_data = {
        "message": "File uploaded",
        "filename": filename,
        "graphs": {
            "waveform": f"{server_url}/api/graphs/{new_graph_subdir}/{waveform_filename}",
            "spectrum": f"{server_url}/api/graphs/{new_graph_subdir}/{spectrum_filename}",
            "spectrogram": f"{server_url}/api/graphs/{new_graph_subdir}/{spectrogram_filename}",
        },
        # "genre_prediction": genre_prediction
    }

    return response_data, 200