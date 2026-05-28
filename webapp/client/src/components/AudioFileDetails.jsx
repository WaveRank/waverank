import AudioPlayer from "./AudioPlayer"
import { formatMB } from "../utils/fileSize";


export default function AudioFileDetails( {selectedFile, selectedFilename, selectedFilepath} ) {
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
                <AudioPlayer audioFile={null} title={null}/>
            </>
    }
    else if (selectedFile) {
        content =  (
            <>
                <p>File Name: {selectedFilename}</p>
                <AudioPlayer audioFile={selectedFile} title={selectedFilename}/>
            </>
        );
    } else {
        content =  (
            <>
                <p>File Name: {selectedFilename}</p>
                <AudioPlayer audioFile={selectedFilepath} title={selectedFilename}/>
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