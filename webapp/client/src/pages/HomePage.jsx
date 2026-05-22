import InputBox from "../components/InputBox";
import AudioPlayer from "../components/AudioPlayer";
import { AnalysisSummary, WaveformSpectrumData, MelSpectrogramData } from '../components/AnalysisData';
import "../styles/inputBox.css";
import "../styles/audioPlayer.css";
import "../styles/popup.css";
import "../styles/analysisBoxes.css";
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
        <>
            <div className="header">
                <div className="headerTitle">
                    <h1>WaveRank</h1>
                    <h1>Audio Classifier</h1>
                </div>
                <p>AI-powered audio analysis and music genre classification from sound clips.</p>
            </div>
            <div>
                <div className="body">

                    <InputBox onUploadResult={handleUploadResult} onStatusChange = {setStatus}/>

                    <div className="bodyOutput">
                        <AnalysisSummary status={status}></AnalysisSummary>
                        <WaveformSpectrumData waveform={graphs?.waveform} spectrum={graphs?.spectrum} />
                        <MelSpectrogramData spectrogram={graphs?.spectrogram}></MelSpectrogramData>
                    </div>

                </div>
            </div>
        </>
    );
};