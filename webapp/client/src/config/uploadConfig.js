/**
 * Upload constraints for client-side validation.
 * Mirrors backend constraints; must be independently updated. 
 */

export const MAX_CONTENT_SIZE = 10 * 1024 * 1024;  // 10MB

const ALLOWED_AUDIO_FORMATS = [
    {
        extension: ".wav",
        mime: "audio/x-wav"
    },
    {
        extension: ".mp3",
        mime: "audio/mpeg"
    },
    {
        extension: ".mp4",
        mime: "video/mp4"
    }
];
export const ALLOWED_EXTENSIONS = ALLOWED_AUDIO_FORMATS.map(format => format.extension);
export const ALLOWED_TYPES =      ALLOWED_AUDIO_FORMATS.map(format => format.mime);
export const ALLOWED_LINKS = ["youtube.", "youtu.be/"]
