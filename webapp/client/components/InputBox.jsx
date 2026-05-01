/**
 * Citations (4/29/2026):
 * https://www.geeksforgeeks.org/reactjs/file-uploading-in-react-js/
 * https://www.geeksforgeeks.org/javascript/file-type-validation-while-uploading-it-using-javascript/
 */
import React, { useState } from "react";
import AudioPlayer from "../components/AudioPlayer";

const HOST = "http://localhost"
const PORT = 5137
const PATH = "/api/predict"

const MAX_CONTENT_SIZE = 10 * 1024 * 1024  // 10MB
const ALLOWED_TYPES = ["audio/wav", "audio/mpeg", "audio/mp4"];
const ALLOWED_EXTENSIONS = [".wav", ".mp3", ".mp4"]


/**
 * Sends an audio file to the backend prediction endpoint.
 * Constructs a form-data request and POSTs it to the Flask API.
 * Expects a JSON response. Logs server errors if the response is not OK.
 * 
 * @param {File} file - The audio file selected by the user
 */
async function uploadFile(file) {
    const formData = new FormData();
    formData.append("file", file);

    const response = await fetch(`${HOST}:${PORT}${PATH}`, {
        method: "POST",
        body: formData,
    });

    if (!response.ok) {
        const text = await response.text();
        console.error("Server error:", text);
        return;
    }

    const data = await response.json();
    console.log(data);
    return(data)
}

/** Converts a file size from bytes to a human-readable megabyte string. */
function bytesToMB(bytes) {
    return (bytes / (1024 * 1024)).toFixed(2) + ' MB';
}

/** Validates that file conforms to allowed types by checking MIME type and extension */
function validFileType(file) {
    const ext = '.' + file.name.split('.').pop().toLowerCase();
    return ALLOWED_TYPES.includes(file.type) && ALLOWED_EXTENSIONS.includes(ext) 
}


export default function InputBox() {
    const [selectedFile, setSelectedFile] = useState(null);
    const [uploadStatus, setUploadStatus] = useState(null);

    const isValidType = selectedFile && validFileType(selectedFile);
    const isValidSize = selectedFile && selectedFile.size <= MAX_CONTENT_SIZE;
    const isValid = selectedFile && isValidSize && isValidType;

    const onFileChange = (event) => {
        setSelectedFile(event.target.files[0]);
    };

    const onUploadFile = async () => {
        if (!isValid) return;
        const responseData = await uploadFile(selectedFile);
        if (responseData) {
            setUploadStatus(responseData.message)
        }
    };

    // TODO
    const onPasteURL = () => {
        return;
    };

    // Show info about the user's selected file and a player to play it.
    // File type already validated, file size validated here
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

