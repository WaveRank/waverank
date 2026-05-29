const API_PREDICT_PATH = "/api/predict"
const API_LINK_PATH = "/api/youtube/download"
const API_PROCESS_PATH = "/api/youtube/process"


/**
 * Sends an audio file to the backend prediction endpoint.
 * Constructs a form-data request and POSTs it to the Flask API.
 * Returns JSON response.
 */
export async function uploadFile(file) {
    const formData = new FormData();
    formData.append("file", file);

    const response = await fetch(API_PREDICT_PATH, {
        method: "POST",
        body: formData,
    });

    let data;
    try {
        data = await response.json();
    } catch {
        console.error("Invalid server response");
        return;
    }
    
    if (!response.ok) {
        const error = data.error;
        console.error("Server error:", error);
        return(data);
    }

    console.log(data);    
    return(data)
}

/**
 * Phase 1: Sends a YouTube URL to the backend, which downloads the audio and
 * returns the title, audio URL, and subdir ID for phase 2.
 */
export async function downloadYoutubeAudio(link) {
    const response = await fetch(API_LINK_PATH, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ URL: link }),
    });

    let data;
    try {
        data = await response.json();
    } catch {
        console.error("Invalid server response");
        return;
    }

    if (!response.ok) {
        const error = data.error;
        console.error("Server error:", error);
        return (data);
    }

    console.log(data);
    return (data)
}

/**
 * Phase 2: Sends the subdir ID and filename to the backend to generate graphs
 * and run genre inference on the previously downloaded audio.
 */
export async function processYoutubeAudio(subdir, filename) {
    const response = await fetch(API_PROCESS_PATH, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ subdir: subdir, filename: filename }),
    });

    let data;
    try {
        data = await response.json();
    } catch {
        console.error("Invalid server response");
        return;
    }

    if (!response.ok) {
        const error = data.error;
        console.error("Server error:", error);
        return (data);
    }

    console.log(data);
    return (data)
}
