import { useState } from "react";
import "../styles/about.css";
import "../styles/popup.css";

export default function AboutPage() {
    const [expanded, setExpanded] = useState(false);

    return (
        <>
            <div className="header">
                    <div className="headerTitle">
                        <h1>WaveRank</h1>
                        <h1>Audio Classifier</h1>
                    </div>
                    <p>AI-powered audio analysis and music genre classification from sound clips</p>
            </div>
            <div>
                <div className="aboutBody">
                    <div className="aboutOutput">

                        <div className="aboutLeft">
                            <div className="aboutContainer">
                                <h2 className="aboutHeader">INSTRUCTIONS</h2>
                                <div className="aboutContent">
                                    <p className="aboutLabel">Follow these steps to classify your audio files:</p>
                                    <div className="aboutDivider"/>
                                    <p><strong>1. Upload or Link:</strong> Use the "Upload" button to select a file or paste a YouTube URL.</p>
                                    <p><strong>2. Process:</strong> The system validates your file and normalizes the audio for analysis.</p>
                                    <p><strong>3. Analyze:</strong> Run the audio through our trained CNN model for classification.</p>
                                    <p><strong>4. Visualize:</strong> Review the genre probability distribution and generated audio graphs.</p></div>
                            </div>

                            <div className="aboutContainer">
                                <h2 className="aboutHeader">GRAPH TYPES</h2>
                                <div className="aboutContent">
                                    <p className="aboutLabel">Descriptions of the visual representations generated:</p>
                                    <div className="aboutDivider"/>
                                    <p><strong>Waveform:</strong> Displays raw amplitude over time to identify rhythm and silence.</p>
                                    <p><strong>Frequency Spectrum:</strong> Shows the intensity of specific frequencies in the signal.</p>
                                    <p><strong>Mel Spectrogram:</strong> A psychoacoustic representation highlighting the patterns our model uses for classification.</p> </div>
                            </div>

                            <div className="aboutContainer">
                                <h2 className="aboutHeader">PIPELINE & ARCHITECTURE</h2>
                                <div className="aboutContent">
                                    <p  className="aboutLabel">Our classification engine follows a robust pipeline:</p>
                                    <div className="aboutDivider"/>
                                    <p><strong>1. Acquisition:</strong> Captures audio from your provided source.</p>
                                    <p><strong>2. Preprocessing:</strong> Audio is normalized and converted to standard format.</p>
                                    <p><strong>3. Feature Extraction:</strong> Audio is transformed into visual "fingerprints" (Mel Spectrograms).</p>
                                    <p><strong>4. Classification:</strong> The CNN analyzes spectrograms for textures, rhythms, and timbres.</p>
                                    <p><strong>5. Prediction:</strong> Returns the most likely genre for the track.</p>
                                </div>
                            </div>

                            <div className="aboutContainer">
                                <h2 className="aboutHeader">PERFORMANCE & LIMITATIONS</h2>
                                <div className="aboutContent">
                                    <p className="aboutLabel">Current performance metrics:</p>
                                    <div className="aboutDivider"/>
                                    <p><strong>Accuracy:</strong> [Insert Accuracy %] on [validation/test] set.</p>
                                    <p><strong>Genres:</strong> Supports 10 genres: Blues, Classical, Country, Disco, Hiphop, Jazz, Metal, Pop, Reggae, and Rock.</p>
                                    <p><strong>Limitations:</strong> Best suited for standard track lengths; high background noise may reduce confidence scores.</p>
                                </div>
                            </div>
                        </div>

                        <div className="aboutContainer modelBox">
                            <h2 className="aboutHeader">SYSTEM ARCHITECTURE</h2>
                            <div className="aboutContent">
                                <img src="/diagram.png" alt="Model Diagram" className="modelDiagram" onClick={() => setExpanded(true)}/>
                            </div>
                        </div>

                        {expanded && (
                            <div className="popupOverlay" onClick={() => setExpanded(false)}>
                                <div className="diagramPopupBox" onClick={(e) => e.stopPropagation()}>
                                    <button className="closeButton" onClick={() => setExpanded(false)}>X</button>
                                    <h2>System Architecture</h2>
                                    <img src="/diagram.png" alt="Model Diagram" className="expandedDiagram"/>
                                </div>
                            </div>
                        )}

                    </div>
                </div>
            </div>
        </>
    );
};