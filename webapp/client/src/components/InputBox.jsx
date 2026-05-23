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
import { isValidYoutubeLink } from "../utils/validLink";
import { formatMB } from "../utils/fileSize";
import { uploadFile, uploadLink } from "../services/api";
import { MAX_CONTENT_SIZE, ALLOWED_EXTENSIONS } from "../config/uploadConfig";


export default function InputBox( {onUploadResult, onStatusChange}) {
    const [selectedFile, setSelectedFile] = useState(null); 
    const [sentLink, setSentLink] = useState(null);
    const [filename, setFilename] = useState(null);
    const [filepath, setFilepath] = useState(null);
    const [showUploadPopup, setShowUploadPopup] = useState(false);
    const [showURLPopup, setShowURLPopup] = useState(false);
    const [requestActive, setRequestActive] = useState(false)

    // Validation flags used to gate upload button and prevent invalid requests
    const isValidType = !!selectedFile && isValidFileType(selectedFile);
    const isValidSize = !!selectedFile && isValidFileSize(selectedFile);
    const canUpload = !!selectedFile && isValidSize && isValidType;
    const isValidLink = isValidYoutubeLink(sentLink);

    const onFileChange = (event) => {
        setSelectedFile(event.target.files[0]);
    };

    const onLinkChange = (event) => {
        setSentLink(event.target.value);
    }

    // Triggers file upload to backend, forwards response via callback.
    // Redundant validation helps safeguard against UI bypass
    const onUploadFile = async () => {
        // Close popup and disable buttons
        setShowUploadPopup(false);
        setRequestActive(true)
        // Validate upload
        if (!canUpload) {
            setRequestActive(false)
            return;
        }
        onStatusChange("Processing Audio from File Upload")
        const responseData = await uploadFile(selectedFile);
        if (responseData && onUploadResult) {
            onUploadResult(responseData);
            setFilename(responseData.filename);
            setFilepath(null)
        }
        setRequestActive(false);
    };

    // Start backend->inference pipeline from a URL rather than file upload
    const onPasteLink = async () => {
        // Close pop up and disable buttons
        setShowURLPopup(false)
        setRequestActive(true)
        // Validate link is a real YouTube
        if (!isValidLink) {
            onStatusChange("Invalid YouTube link!")
            setRequestActive(false)
            return;
        }
        // send it to new flask route
        onStatusChange("Processing Audio from Youtube")
        const responseData = await uploadLink(sentLink);
        // handle response
        if (responseData && onUploadResult) {
            onUploadResult(responseData);
            setFilename(responseData.filename);
            setFilepath(responseData.audio);
            setSelectedFile(null)
        }
        setRequestActive(false)
    };

    return (
        <>
            {/* Buttons for uploading audio files and pasting URLs */}
            <div className="inputBox">
                <div className="inputButtons">
                    <button onClick={() => setShowUploadPopup(true)} disabled={requestActive}>Upload Audio File</button>
                    <p>or</p>
                    <button onClick={() => setShowURLPopup(true)} disabled={requestActive}>Paste URL</button>
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
                        <input className="fileInput" type="file" accept={ALLOWED_EXTENSIONS.join(',')} onChange={onFileChange} />
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
                        <input type="url" id="youtube-url-input" name="youtube-url-input" onChange={onLinkChange}></input>
                        <button onClick={onPasteLink}>Paste URL</button>
                    </div>
                </div>
            )}
            <AudioFileDetails
                selectedFile={selectedFile}
                isValidSize={isValidSize}
                maxContentSize={MAX_CONTENT_SIZE}
                selectedFilename={filename}
                selectedFilepath={filepath}
            />
        </>


    )
}