import AudioPlayer from "./AudioPlayer"
import { formatMB } from "../utils/fileSize";


export default function AudioFileDetails( {selectedFile, isValidSize, maxContentSize, selectedFilename, selectedFilepath} ) {
   /**
    * Shows metadata and audio preview of user's selected file.
    * Displays validation feedback for oversized files.
    * Falls back to demo audio when no file selected.
    */
    let content;

    if (!selectedFile && !selectedFilename) {
        content = 
            <>
                <p>File Name: Your_File_Here</p>
                <AudioPlayer audioFile={"/demo_song.mp3"}/>
            </>
    }
    else if (selectedFile && !isValidSize) {
        const fileSizeMB = formatMB(selectedFile.size)
        const maxContentMB = formatMB(maxContentSize, 0)

        content = (
            <>
                <h3>Please select smaller file.</h3>
                <h4>File size {fileSizeMB} exceeds maximum ({maxContentMB})</h4>
                <p>File Name: {selectedFilename}</p>
            </>
        )
    }
    else if (selectedFile) {
        content =  (
            <>
                <p>File Name: {selectedFilename}</p>
                <AudioPlayer audioFile={selectedFile}/>
            </>
        );
    } else {
        content =  (
            <>
                <p>File Name: {selectedFilename}</p>
                <AudioPlayer audioFile={selectedFilepath}/>
            </>
        );
    };

    return (
        <div className="inputAudio">
            <h2>File Details:</h2>
            {content}
        </div>
    )
}