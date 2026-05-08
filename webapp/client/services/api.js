const API_PREDICT_PATH = "/api/predict"


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