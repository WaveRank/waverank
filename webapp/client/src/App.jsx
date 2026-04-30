/**
 * Citations:
 * https://www.geeksforgeeks.org/reactjs/file-uploading-in-react-js/
 */
import axios from "axios";
import React, { useState } from "react";
import cors from "cors"

const MAX_CONTENT_SIZE = 10 * 1024 * 1024  // 10MB 

async function uploadFile(file) {
  const formData = new FormData();
  formData.append("file", file);

  const response = await fetch("http://localhost:5137/api/predict", {
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


function bytes_to_MB(bytes) {
  return (bytes / (1024 * 1024)).toFixed(2);
}


const App = () => {
	const [selectedFile, setSelectedFile] = useState(null);

	const onFileChange = (event) => {
		setSelectedFile(event.target.files[0]);
	};

  const onFileUpload = () => {
    if (!selectedFile) return;
    if (selectedFile.size > MAX_CONTENT_SIZE) {
      alert("File too large");
      console.log(formatSize(file.size));
      return;
    }
    uploadFile(selectedFile);
  };

	const fileData = () => {
		if (!selectedFile) return;
    uploadFile(selectedFile)
    if (selectedFile.size > MAX_CONTENT_SIZE) {
      return (
        <div>
          <h2>File size {bytes_to_MB(selectedFile.size)}MB exceeds maximum (10MB)</h2>
          <h3>Please select smaller file.</h3>
          <p>File Name: {selectedFile.name}</p>
          <p>File Type: {selectedFile.type}</p>
        </div>
      )
    }
    return (
      <div>
        <h2>File Details:</h2>
        <p>File Name: {selectedFile.name}</p>
        <p>File Type: {selectedFile.type}</p>
      </div>
    );
  }

	return (
		<div>
			<h1>WaveRank</h1>
			<h3>Choose a file to upload</h3>
			<div>
				<input type="file" onChange={onFileChange} />
				<button onClick={onFileUpload}>Upload!</button>
			</div>
			{fileData()}
		</div>
	);
};

export default App;