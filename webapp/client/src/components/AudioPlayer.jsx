import { useRef, useState, useEffect } from "react";

// Citation (4/29/26): https://stackoverflow.com/questions/3733227/javascript-seconds-to-minutes-and-seconds
// Citation (5/28/26): https://www.w3schools.com/jsref/met_win_settimeout.asp
export default function AudioPlayer({ audioFile, title }) {
    const audioRef = useRef(null);
    const titleContainerRef = useRef(null);
    const titleTextRef = useRef(null);
    const [isPlaying, setIsPlaying] = useState(false);
    const [isLongTitle, setIsLongTitle] = useState(false);
    const [currentTime, setCurrentTime] = useState(0);
    const [duration, setDuration] = useState(0);
    const [src, setSrc] = useState(null);

    // Handle file vs string audioFile
    useEffect(() => {
        if (!audioFile) return;

        setCurrentTime(0);
        setDuration(0);
        setIsPlaying(false);

        if (audioFile instanceof File) {
            const url = URL.createObjectURL(audioFile);
            setSrc(url);
            return () => URL.revokeObjectURL(url);
        } else {
            setSrc(audioFile); // assumes string URL
        }
    }, [audioFile]);

    // Checks whether the title is longer than container
    useEffect(() => {
    setIsLongTitle(false);
    // Ensure title measure is done after re-render
    const timer = setTimeout(() => {
        if (titleContainerRef.current && titleTextRef.current) {
            setIsLongTitle(
                titleTextRef.current.scrollWidth > titleContainerRef.current.clientWidth
            );
        }}, 80); return () => clearTimeout(timer);
    }, [title]);

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

    const onLoadedMetadata = () => {
        setDuration(audioRef.current.duration);
    };

    const onEnded = () => {
        setIsPlaying(false);
        setCurrentTime(0);
        audioRef.current.currentTime = 0;
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
            <audio 
                ref={audioRef} 
                src={src} 
                onTimeUpdate={onTimeUpdate}
                onLoadedMetadata={onLoadedMetadata}
                onEnded={onEnded}
            />

                <div className="audioRow">
                    {/* Adds scrolling animation if the title is long */}
                    <div className="audioTitleContainer" ref={titleContainerRef}> 
                        <span
                            className={`audioTitleText ${isLongTitle ? "scrolling" : ""}`}
                            ref={titleTextRef}
                        >
                            {title}
                            {isLongTitle && <span className="titleSpacer">{title}</span>}
                        </span>
                    </div>

                    <div className="audioScrubber">
                        {/* Progress slider for song, scrubbable */}
                        <input
                            className="playbackBar"
                            type="range"
                            min="0"
                            max={duration}
                            value={currentTime}
                            onChange={onSeek}
                        />
                        {/* Audio timestamps, shows current time and total length */}
                        <div className="audioTimes">
                            <span>{formatTime(currentTime)}</span>
                            <span>{formatTime(duration)}</span>
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
