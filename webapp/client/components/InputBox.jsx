/**
 * Handles audio file selection, validation, and upload to backend.
 * 
 * Citations (4/29/2026):
 * https://www.geeksforgeeks.org/reactjs/file-uploading-in-react-js/
 * https://www.geeksforgeeks.org/javascript/file-type-validation-while-uploading-it-using-javascript/
 */
import React, { useState } from "react";
import AudioPlayer from "../components/AudioPlayer";


const API_PREDICT_PATH = "/api/predict"

// Client-side constraints for file uploads
const MAX_CONTENT_SIZE = 10 * 1024 * 1024  // 10MB
const ALLOWED_TYPES = ["audio/wav", "audio/mpeg", "audio/mp4"];
const ALLOWED_EXTENSIONS = [".wav", ".mp3", ".mp4"]


/**
 * Sends an audio file to the backend prediction endpoint.
 * Constructs a form-data request and POSTs it to the Flask API.
 * Returns JSON response.
 */
async function uploadFile(file) {
    const formData = new FormData();
    formData.append("file", file);

    const response = await fetch(API_PREDICT_PATH, {
        method: "POST",
        body: formData,
    });
    const data = await response.json();

    if (!response.ok) {
        const error = data.error;
        console.error("Server error:", error);
        return(data);
    }

    console.log(data);
    // TODO: Include graphs such as waveform, spectrogram, etc.
    return(data)
}

/** Converts a file size from bytes to a human-readable megabyte string. */
function bytesToMB(bytes) {
    return (bytes / (1024 * 1024)).toFixed(2) + ' MB';
}

/** Performs shallow client-side validation of MIME type and extension.
 * Can be bypassed, backend must also perform validation.
 */
function validFileType(file) {
    const ext = '.' + file.name.split('.').pop().toLowerCase();
    return ALLOWED_TYPES.includes(file.type) && ALLOWED_EXTENSIONS.includes(ext) 
}


export default function InputBox( {onUploadResult} ) {
    const [selectedFile, setSelectedFile] = useState(null);

    // Validation state used to gate upload button and prevent invalid requests
    const isValidType = selectedFile && validFileType(selectedFile);
    const isValidSize = selectedFile && selectedFile.size <= MAX_CONTENT_SIZE;
    const isValid = selectedFile && isValidSize && isValidType;

    const onFileChange = (event) => {
        setSelectedFile(event.target.files[0]);
    };

    // Triggers file upload to backend, forwards response via callback.
    // Redundant validation helps safeguard against UI bypass
    const onUploadFile = async () => {
        if (!isValid) return;
        const responseData = await uploadFile(selectedFile);
        if (responseData && onUploadResult) {
            onUploadResult(responseData);
        }
    };

    // TODO: start backend->inference pipeline from a URL rather than file upload
    const onPasteURL = () => {
        return;
    };

    // Shows metadata and audio preview of user's selected file.
    // Handles size validation feedback (can't be enforced by input element).
    // Falls back to demo audio when no file selected.
    // TODO: maybe redo how we present the demo song to be more obvious, or get rid of it
    const audioFileDetails = () => {
        if (!selectedFile) {
            return(
                <div className="inputAudio">
                    <h2>File Details:</h2>
                    <p>File Name: Your_File_Here</p>
                    <AudioPlayer audioFile={"/demo_song.mp3"}/>
                </div>
            );
        }
        if (!isValidSize) {
            const fileSizeMB = bytesToMB(selectedFile.size)
            const maxContentMB = bytesToMB(MAX_CONTENT_SIZE).slice(0, -6) + ' MB'
            return (
                <div className="inputAudio">
                    <h2>File Details:</h2>
                    <h3>Please select smaller file.</h3>
                    <h4>File size {fileSizeMB} exceeds maximum ({maxContentMB})</h4>
                    <p>File Name: {selectedFile.name}</p>
                </div>
            )
        } else {
            return (
                <div className="inputAudio">
                    <h2>File Details:</h2>
                    <p>File Name: {selectedFile.name}</p>
                    <AudioPlayer audioFile={selectedFile}/>
                </div>
            );
        };
    };

    
    return (
        <div className="inputBox">
            <h2>Input</h2>
            <p>Upload an audio clip to classify its top_N music genres using a CNN trained on spectrogram features.</p>
            <div className="inputButtons">
                <div>
                    <input type="file" accept={ALLOWED_EXTENSIONS.join(',')} onChange={onFileChange} />
                    <button onClick={onUploadFile} disabled={!isValid}>Upload!</button>
                </div>
                <button onClick={onPasteURL}>Paste URL</button>
            </div>
            {audioFileDetails()}
        </div>
    )
}

