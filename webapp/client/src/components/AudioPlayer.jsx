import { useRef, useState, useEffect } from "react";

// Citation (4/29/26): https://stackoverflow.com/questions/3733227/javascript-seconds-to-minutes-and-seconds
export default function AudioPlayer({ audioFile, title }) {
    const audioRef = useRef(null);
    const [isPlaying, setIsPlaying] = useState(false);
    const [currentTime, setCurrentTime] = useState(0);
    const [src, setSrc] = useState(null);

    // Handle file vs string audioFile
    useEffect(() => {
        if (!audioFile) return;

        if (audioFile instanceof File) {
            const url = URL.createObjectURL(audioFile);
            setSrc(url);
            return () => URL.revokeObjectURL(url);
        } else {
            setSrc(audioFile); // assumes string URL
        }
    }, [audioFile]);


    // Handles play and pause
    const togglePlay = () => {
        const audio = audioRef.current;

        if (isPlaying) {
            audio.pause();
            setIsPlaying(false);
        } else {
            audio.play();
            setIsPlaying(true);
        }
    };

    // Tracks current playback position
    const onTimeUpdate = () => {
        setCurrentTime(audioRef.current.currentTime);
    };

    // Allows scrubbing of the playback bar
    const onSeek = (e) => {
        const time = Number(e.target.value);
        audioRef.current.currentTime = time;
        setCurrentTime(time);
    };

    // Formats time into MM:SS format
    const formatTime = (time) => {
        if (isNaN(time)) return "0:00";
        const m = Math.floor(time / 60);
        const s = Math.floor(time % 60);
        return `${m}:${s < 10 ? "0" : ""}${s}`;  // Citation for this bit here
    };

    return (
        <div className="audioPlayer">
            <audio ref={audioRef} src={src} onTimeUpdate={onTimeUpdate}/>

                <div className="audioRow">

                    <div className="audioTitle">{title}</div>

                    <div className="audioScrubber">
                        {/* Progress slider for song, scrubbable */}
                        <input
                            className="playbackBar"
                            type="range"
                            min="0"
                            max={audioRef.current?.duration || 0}
                            value={currentTime}
                            onChange={onSeek}
                        />
                        {/* Audio timestamps, shows current time and total length */}
                        <div className="audioTimes">
                            <span>{formatTime(currentTime)}</span>
                            <span>{formatTime(audioRef.current?.duration)}</span>
                        </div>

                    </div>

                {/* Play button to play/pause song */}
                <button className="playButton" onClick={togglePlay}>
                    {isPlaying ? "❚❚" : "▶"}
                </button>

            </div>
        </div>
    );
};
