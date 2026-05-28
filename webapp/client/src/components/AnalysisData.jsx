import { useEffect, useState } from 'react';
import { prepareGenreData, getMagmaColor, formatPercentage } from '../utils/analysisHelpers';
// Temporary static data from the demo song
const waveform = '/demo_waveform.png';
const frequency = '/demo_frequency_spectrum.png';
const spectrogram = '/demo_spectrogram.png';

// Helper for genre analysis bar graph
function GenreBar({ genre, value }) {
    const percentage = formatPercentage(value);

    return (
        <div className="genreRow">
            {/* Genre label */}
            <span className="genreLabel">{genre.toUpperCase()}</span>

            {/* Actual bar (with Magma palette colored fill) */}
            <div className="barContainer">
                <div className="barTrack">
                    <div 
                        className="barFill" 
                        style={{ 
                            width: `${percentage}%`, backgroundColor: getMagmaColor(value) }}
                    />
                </div>

                {/* Percentage score */}
                <span className="percentageColumn">{percentage}%</span>
            </div>
        </div>
    );
}

// Analysis Summary Box: Contains input song's percentage results for genres
export function AnalysisSummary({ status, genrePrediction }) {
    const [demoData, setDemoData] = useState(null);

    // Genre bar chart uses demo data on initial load
    useEffect(() => {
        fetch('/demo_test_results.json')
            .then((response) => response.json())
            .then((data) => setDemoData(data));
    }, []);
    if (!demoData) {
        return <div className="boxContainer">Loading...</div>;
    }

    // Prepare bar chart data
    const genreData = genrePrediction || demoData.genre_prediction;
    const sortedGenres = prepareGenreData(genreData);

    return (
        <div className="boxContainer">
            {/* Section header */}
            <h2 className="boxHeader">ANALYSIS SUMMARY</h2>

            {/* Section content */}
            <div className="boxContent">
                <h3>{status.toUpperCase()}</h3>

                <div className="boxDivider"/>

                {/* Bar chart of genre probabilities */}
                <p>{genrePrediction ? "Genres:" : "Genres: (example)"}</p>
                <div className="chartContainer">
                    {sortedGenres.map(([genre, value]) => (
                        <GenreBar key={genre} genre={genre} value={value} />
                    ))}
                </div>
            </div>

        </div>
    );
}

export function WaveformSpectrumData({ waveform, spectrum }) {
    return (
        <div className="boxContainer">
            {/* Section header */}
            <h2 className="boxHeader">WAVEFORM & FREQUENCY SPECTRUM DATA</h2>

            {/* Section content */}
            <div className="boxContent">

                {/* Waveform data */}
                <div className="boxSection">
                    <p className="boxLabel">WAVEFORM</p>
                    <div className="boxGraph">
                        <img className="boxImage" src={waveform || '/demo_waveform.png'}></img>
                    </div>
                </div>

                <div className="boxDivider"/>

                {/* Frequency spectrum data */}
                <div className="boxSection">
                    <p className="boxLabel">FREQUENCY SPECTRUM</p>
                    <div className="boxGraph">
                        <img className="boxImage" src={spectrum || '/demo_frequency_spectrum.png'}></img>
                    </div>
                </div>

            </div>
        </div>
    );
}

export function MelSpectrogramData({ spectrogram }) {
    return (
        <div className="boxContainer">
            {/* Section header */}
            <h2 className="boxHeader">MEL SPECTROGRAM & ???</h2>

            {/* Section content */}
            <div className="boxContent">

                {/*Mel spectrogram data */}
                <div className="boxSection">
                    <p className="boxLabel">MEL SPECTROGRAM</p>
                    <div className="boxGraph">
                        <img className="boxImage" src={spectrogram || 'demo_spectrogram.png'}></img>
                    </div>
                </div>
            </div>
        </div>
    );
}