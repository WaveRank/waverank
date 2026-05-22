/**
 * Handles audio file selection, validation, and upload to backend.
 * 
 * Citations (4/29/2026):
 * https://www.geeksforgeeks.org/reactjs/file-uploading-in-react-js/
 * https://www.geeksforgeeks.org/javascript/file-type-validation-while-uploading-it-using-javascript/
 */
import React, { useState } from "react";
import AudioFileDetails from "./AudioFileDetails";
import { isValidFileType } from "../utils/fileType";
import { isValidFileSize } from "../utils/fileSize";
import { formatMB } from "../utils/fileSize";
import { uploadFile } from "../services/api";
import { MAX_CONTENT_SIZE, ALLOWED_EXTENSIONS } from "../config/uploadConfig";


export default function InputBox( {onUploadResult} ) {
    const [selectedFile, setSelectedFile] = useState(null); 
    const [showUploadPopup, setShowUploadPopup] = useState(false);
    const [showURLPopup, setShowURLPopup] = useState(false);

    // Validation flags used to gate upload button and prevent invalid requests
    const isValidType = !!selectedFile && isValidFileType(selectedFile);
    const isValidSize = !!selectedFile && isValidFileSize(selectedFile);
    const canUpload = !!selectedFile && isValidSize && isValidType;

    const onFileChange = (event) => {
        setSelectedFile(event.target.files[0]);
    };

    // Triggers file upload to backend, forwards response via callback.
    // Redundant validation helps safeguard against UI bypass
    const onUploadFile = async () => {
        if (!canUpload) return;
        const responseData = await uploadFile(selectedFile);
        if (responseData && onUploadResult) {
            onUploadResult(responseData);
        }
        setShowUploadPopup(false);
    };

    // TODO: start backend->inference pipeline from a URL rather than file upload
    const onPasteURL = () => {
        return;
    };

    return (
        <>
            {/* Buttons for uploading audio files and pasting URLs */}
            <div className="inputBox">
                <div className="inputButtons">
                    <button onClick={() => setShowUploadPopup(true)}>Upload Audio File</button>
                    <p>or</p>
                    <button onClick={() => setShowURLPopup(true)}>Paste URL</button>
                </div>
            </div>

            {/* Conditional: Popup for uploading audio file */}
            {showUploadPopup && (
                <div className="popupOverlay">
                    <div className="popupBox">
                        <h2>Upload Audio File</h2>
                        <button className="closeButton" onClick={() => setShowUploadPopup(false)}>X</button>            
                        <p>
                            Upload an audio clip to classify its top_N music genres using
                            a CNN trained on spectrogram features.
                            Max size {formatMB(MAX_CONTENT_SIZE, 0)}.
                        </p>   
                        <input className="fileInput" type="file" accept={ALLOWED_EXTENSIONS.join(',')} onChange={onFileChange}/>
                        <button className="uploadButton" onClick={onUploadFile} disabled={!canUpload}>Upload!</button>
                    </div>
                </div>
            )}

            {/* Conditional: Popup for pasting URL */}
            {showURLPopup && (
                <div className="popupOverlay">
                    <div className="popupBox">
                        <h2>Paste URL</h2>
                        <button className="closeButton" onClick={() => setShowURLPopup(false)}>X</button>
                        <p>TODO: URL-based audio classification.</p>
                    </div>
                </div>
            )} 
        </>
    )
}