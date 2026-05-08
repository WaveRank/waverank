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
    };

    // TODO: start backend->inference pipeline from a URL rather than file upload
    const onPasteURL = () => {
        return;
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
                <button onClick={onPasteURL}>Paste URL</button>
            </div>
            <AudioFileDetails 
                selectedFile={selectedFile} 
                isValidSize={isValidSize} 
                maxContentSize = {MAX_CONTENT_SIZE}
            />
        </div>
    )
}