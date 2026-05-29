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
import { downloadYoutubeAudio, processYoutubeAudio, uploadFile } from "../services/api";
import { MAX_CONTENT_SIZE, ALLOWED_EXTENSIONS } from "../config/uploadConfig";


export default function InputBox( {onUploadResult, onStatusChange}) {
    const [selectedFile, setSelectedFile] = useState(null); 
    const [uploadedFile, setUploadedFile] = useState(null);
    const [filename, setFilename] = useState(null);
    const [filepath, setFilepath] = useState(null);
    const [sentLink, setSentLink] = useState(null);
    const [showUploadPopup, setShowUploadPopup] = useState(false);
    const [showURLPopup, setShowURLPopup] = useState(false);
    const [requestActive, setRequestActive] = useState(false)
    const [uploadComplete, setUploadComplete] = useState(false)

    // Validation flags used to gate upload button and prevent invalid requests
    const isValidType = !!selectedFile && isValidFileType(selectedFile);
    const isValidSize = !!selectedFile && isValidFileSize(selectedFile);
    const canUpload = !!selectedFile && isValidSize && isValidType && !uploadComplete;
    const isValidLink = isValidYoutubeLink(sentLink);

    const onFileChange = (event) => {
        setSelectedFile(event.target.files[0]);
        setUploadComplete(false);
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
        onStatusChange("Processing Audio from File Upload")
        const responseData = await uploadFile(selectedFile);
        if (responseData?.error) {
            onStatusChange(responseData.error);
            setRequestActive(false);
            return;
        }
        if (responseData && onUploadResult) {
            onUploadResult(responseData);
            setFilename(responseData.filename);
            setFilepath(null)
            setUploadedFile(selectedFile)
        }
        setRequestActive(false);
        setUploadComplete(true);
    };

    // Start backend->inference pipeline from a URL rather than file upload
    const onPasteLink = async () => {
        // Close pop up and disable buttons
        setShowURLPopup(false)
        setRequestActive(true)
        
        // Phase 1: end link to download flask route
        onStatusChange("Downloading audio from YouTube")
        const downloadData = await downloadYoutubeAudio(sentLink);
        if (downloadData?.error) {
            onStatusChange(downloadData.error);
            setRequestActive(false);
            return;
        }
        // handle download response
        if (downloadData) {
            setFilename(downloadData.filename);
            setFilepath(downloadData.audio);
            setSelectedFile(null);
            setUploadedFile(null);

            // Phase 2: process audio file from download
            onStatusChange("Processing audio from YouTube")
            const processData = await processYoutubeAudio(downloadData.subdir, downloadData.filename)
            if (processData && onUploadResult) {
                onUploadResult(processData);
            }
        } else {
            onUploadResult(downloadData)
        }
        setRequestActive(false);
        setSentLink(null);
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
                <div className="popupOverlay" onClick={() => setShowUploadPopup(false)}>
                    <div className="popupBox" onClick={(e) => e.stopPropagation()}>
                        <h2>Upload Audio File</h2>
                        <button className="closeButton" onClick={() => {
                            setShowUploadPopup(false); 
                            setSelectedFile(null);
                        }}>X</button>
                        <p>
                            Upload an audio clip to classify its top_N music genres using
                            a CNN trained on spectrogram features.
                            Max size {formatMB(MAX_CONTENT_SIZE, 0)}.
                        </p>
                        <input className="fileInput" type="file" accept={ALLOWED_EXTENSIONS.join(',')} onChange={onFileChange} />
                        {selectedFile && !isValidType && (
                            <p className="popupError">
                                File type not supported. Allowed types are: {ALLOWED_EXTENSIONS.join(',')}
                            </p>
                        )}
                        {selectedFile && !isValidSize && isValidType && (
                            <p className="popupError">
                                File size {formatMB(selectedFile.size)} exceeds maximum {formatMB(MAX_CONTENT_SIZE, 0)} limit.
                            </p>
                        )}
                        <button className="uploadButton" onClick={onUploadFile} disabled={!canUpload}>Upload!</button>
                    </div>
                </div>
            )}

            {/* Conditional: Popup for pasting URL */}
            {showURLPopup && (
                <div className="popupOverlay" onClick={() => setShowUploadPopup(false)}>
                    <div className="popupBox" onClick={(e) => e.stopPropagation()}>
                        <h2>Paste URL</h2>
                        <button className="closeButton" onClick={() => {
                            setShowURLPopup(false);
                            setSentLink(null);
                        }}>X</button>
                        <p>Paste a URL from YouTube. Does not allow livestreams, age-restricted content, private videos, or videos over 10 minutes.</p>
                        <input className="fileInput" type="url" id="youtube-url-input" name="youtube-url-input" placeholder="Paste URL here" onChange={onLinkChange}></input>
                        {sentLink && !isValidLink && (
                            <p className="popupError">Invalid YouTube link!</p>
                        )}
                        <button className="uploadButton" onClick={onPasteLink} disabled={!isValidLink}>Paste URL</button>
                    </div>
                </div>
            )}
            <AudioFileDetails
                selectedFile={uploadedFile}
                selectedFilename={filename}
                selectedFilepath={filepath}
            />
        </>
    )
}
