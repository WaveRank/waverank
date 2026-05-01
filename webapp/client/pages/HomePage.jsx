import AudioPlayer from "../components/AudioPlayer";
import "../src/App.css";

const onUploadFile = () => {
    return;
};

const onPasteURL = () => {
    return;
};

export default function HomePage() {
    return (
        <div>
            <div className="body">

                <div className="bodyLeft">

                    <div className="inputBox">
                        <h2>Input</h2>
                        <p>Upload an audio clip to classify its top_N music genres using a CNN trained on spectrogram features.</p>
                        <div className="inputButtons">
                            <button onClick={onUploadFile}>Upload audio file</button>
                            <button onClick={onPasteURL}>Paste URL</button>
                        </div>
                        <div className="inputAudio">
                            <p>File/song name here</p>
                            <AudioPlayer audioFile={"/demo_song.mp3"}/>
                        </div>
                    </div>

                    <div className="analysisBox">
                        <h2>Analysis</h2>
                        <p>Status: ???</p>
                        <p>Bar chart here</p>
                    </div>

                </div>

                <div className="bodyRight">
                    <div className="dataBox">
                        <h2>Data</h2>
                        <p>Graphs here</p>
                    </div>
                </div>

            </div>
        </div>
    );
};