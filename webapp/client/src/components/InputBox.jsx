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
        if (!canUpload) return;
        onStatusChange("Processing Audio from File Upload")
        const responseData = await uploadFile(selectedFile);
        if (responseData && onUploadResult) {
            onUploadResult(responseData);
            setFilename(responseData.filename);
            setFilepath(null)
        }
    };

    // Start backend->inference pipeline from a URL rather than file upload
    const onPasteLink = async () => {
        // Validate link is a real YouTube
        if (!isValidLink) {
            onStatusChange("Invalid YouTube link!")
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
    };

    
    return (
        <div className="inputBox">
            <h2>Input</h2>
            <p>
                Upload an audio clip to classify its top_N music genres using 
                a CNN trained on spectrogram features. 
                Max size {formatMB(MAX_CONTENT_SIZE, 0)}.
            </p>
            <div className="inputButtons">
                <div>
                    <input type="file" accept={ALLOWED_EXTENSIONS.join(',')} onChange={onFileChange} />
                    <button onClick={onUploadFile} disabled={!canUpload}>Upload!</button>
                </div>
                <div>
                    <input type="url" id="homepage" name="homepage" onChange={onLinkChange}></input>
                    <button onClick={onPasteLink}>Paste URL</button>
                </div>
                
            </div>
            <AudioFileDetails 
                selectedFile={selectedFile} 
                isValidSize={isValidSize} 
                maxContentSize = {MAX_CONTENT_SIZE}
                selectedFilename = {filename}
                selectedFilepath = {filepath}
            />
        </div>
    )
}