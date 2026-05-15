import librosa
from webapp.server.config import MAX_CONTENT_LENGTH, ALLOWED_EXTENSIONS


# Performs a fast, non-secure extension check.
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Performs authoritative validity check by attempting to decode as audio
def decodable_audio_file(path):
    try:
        librosa.load(path)
        return True
    except Exception as e:
        print("Decode error:", repr(e))
        return False
