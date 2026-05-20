import InputBox from "../components/InputBox";
import "../App.css";
import React, { useState } from "react";


export default function HomePage() {
    const [status, setStatus] = useState('Awaiting file')
    const [data, setData] = useState(null)

    // Set status depending on response from Flask backend
    // TODO: set graphs and prediction result too
    const handleUploadResult = (data) => {
        if (data.error) {
            setStatus(data.error);
        }
        else if (data.message) {
            setStatus(data.message);
            setData(data);
        }
    };

    const graphs = data?.graphs;

    return (
        <div>
            <div className="body">

                <div className="bodyLeft">
                    <InputBox onUploadResult={handleUploadResult}/>
                    <div className="analysisBox">
                        <h2>Analysis</h2>
                        <p>Status: {status}</p>
                        <p>Bar chart here</p>
                    </div>
                </div>

                <div className="bodyRight">
                    <div className="dataBox">
                        <h2>Data</h2>
                        <p>Graphs here</p>
                        <>
                            {graphs?.waveform && <img src={graphs.waveform} />}
                            {graphs?.spectrum && <img src={graphs.spectrum} />}
                            {graphs?.spectrogram && <img src={graphs.spectrogram} />}
                        </>
                    </div>
                </div>

            </div>
        </div>
    );
};