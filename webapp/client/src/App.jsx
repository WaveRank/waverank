/**
 * Citations (4/29/2026):
 * https://www.geeksforgeeks.org/reactjs/file-uploading-in-react-js/
 * https://www.geeksforgeeks.org/javascript/file-type-validation-while-uploading-it-using-javascript/
 */

import { Routes, Route, Link } from "react-router-dom";
import HomePage from "../pages/HomePage";
import AboutPage from "../pages/AboutPage";
import ContributorsPage from "../pages/ContributorsPage";
import CreditsPage from "../pages/CreditsPage";
import "./App.css";
import React, { useState } from "react";

const HOST = "http://localhost"
const PORT = 5137
const PATH = "/api/predict"
const MAX_CONTENT_SIZE = 10 * 1024 * 1024  // 10MB
const ALLOWED_TYPES = ["audio/wav", "audio/mpeg", "audio/mp4"];
const ALLOWED_EXTENSIONS = [".wav", ".mp3", ".mp4"]


/**
 * Sends an audio file to the backend prediction endpoint.
 *
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
}

// Converts a file size from bytes to a human-readable megabyte string.
function bytesToMB(bytes) {
  return (bytes / (1024 * 1024)).toFixed(2) + ' MB';
}

// Validates that file conforms to allowed types by checking MIME type and extension
function validFileType(file) {
  const ext = '.' + file.name.split('.').pop().toLowerCase();
  return ALLOWED_TYPES.includes(file.type) && ALLOWED_EXTENSIONS.includes(ext) 
}


export default function App() {
  const [selectedFile, setSelectedFile] = useState(null);

  const isValidType = selectedFile && validFileType(selectedFile);
  const isValidSize = selectedFile && selectedFile.size <= MAX_CONTENT_SIZE;
  const isValid = selectedFile && isValidSize && isValidType;

	const onFileChange = (event) => {
		setSelectedFile(event.target.files[0]);
	};

  const onFileUpload = () => {
    if (!isValidType) return;
    uploadFile(selectedFile);
    console.log(`uploaded file ${selectedFile.name}`)
  };

	const userUploadSection = () => {
		if (!selectedFile) return;
    if (!isValidSize) {
      const fileSizeMB = bytesToMB(selectedFile.size)
      const maxContentMB = bytesToMB(MAX_CONTENT_SIZE).slice(0, -6) + ' MB'
      return (
        <div>
          <h2>Please select smaller file.</h2>
          <h3>File size {fileSizeMB} exceeds maximum ({maxContentMB})</h3>
          <p>File Name: {selectedFile.name}</p>
          <p>File Type: {selectedFile.type}</p>
        </div>
      )
    }
    else {
      return (
        <div>
          <h2>File Details:</h2>
          <p>File Name: {selectedFile.name}</p>
          <p>File Type: {selectedFile.type}</p>
        </div>
      );
    }
  }

      return (
        <div>
            <div className="navBar">
                <h1>WaveRank</h1>

                <div className="navButtons">
                    <Link to="/about"><button>About</button></Link>
                    <Link to="/contributors"><button>Contributors</button></Link>
                    <Link to="/credits"><button>Credits</button></Link>
                    <Link to="/"><button className="homeButton">Home</button></Link>
                </div>
            </div>

            <div className="header">
                <h1>WaveRank</h1>
                <p>AI-powered music genre classification from audio clips</p>
            </div>

            <div>
              <h3>Choose a file to upload</h3>
              <div>
                <input type="file" accept={ALLOWED_EXTENSIONS.join(',')} onChange={onFileChange} />
                <button onClick={onFileUpload} disabled={!isValid}>Upload!</button>
              </div>
              {userUploadSection()}
            </div>

            <Routes>
                <Route path="/" element={<HomePage/>}/>
                <Route path="/about" element={<AboutPage/>}/>
                <Route path="/contributors" element={<ContributorsPage/>}/>
                <Route path="/credits" element={<CreditsPage/>}/>
            </Routes>
        </div>
    );
}