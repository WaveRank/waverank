import "../styles/credits.css";

export default function CreditsPage() {
    const credits = [
        {
            category: "Deep Learning & AI",
            items: [
                { name: "TensorFlow & Keras API", url: "https://www.tensorflow.org/api_docs" },
                { name: "ResNet50 & Transfer Learning", url: "https://www.tensorflow.org/guide/keras/transfer_learning" },
                { name: "Keras Functional API", url: "https://www.tensorflow.org/guide/keras/functional_api" },
                { name: "Data Performance Guide", url: "https://www.tensorflow.org/guide/data_performance" },
                { name: "Keras Tuner (Bayesian Optimization)", url: "https://keras.io/keras_tuner/api/tuners/bayesian/" },
                { name: "Model Saving & Loading", url: "https://www.geeksforgeeks.org/machine-learning/save-and-load-models-in-tensorflow/" }
            ]
        },
        {
            category: "Audio Processing",
            items: [
                { name: "Librosa Documentation", url: "https://librosa.org/doc/main/generated/librosa.feature.melspectrogram.html" },
                { name: "Understanding Mel Spectrograms", url: "https://medium.com/analytics-vidhya/understanding-the-mel-spectrogram-fca2afa2ce53" },
                { name: "Spectrogram Augmentation", url: "https://medium.com/data-science/audio-deep-learning-made-simple-part-3-data-preparation-and-augmentation-24c6e1f6b52" },
                { name: "YT-DLP (Audio Extraction)", url: "https://github.com/yt-dlp/yt-dlp" }
            ]
        },
        {
            category: "Metrics & Visualization",
            items: [
                { name: "Scikit-Learn Metrics (ROC, AUC)", url: "https://scikit-learn.org/stable/modules/generated/sklearn.metrics.roc_curve.html" },
                { name: "Top-K Accuracy", url: "https://scikit-learn.org/stable/modules/generated/sklearn.metrics.top_k_accuracy_score.html" },
                { name: "t-SNE Dimensionality Reduction", url: "https://scikit-learn.org/stable/modules/generated/sklearn.manifold.TSNE.html" },
                { name: "Matplotlib Documentation", url: "https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.legend.html" }
            ]
        },
        {
            category: "Frontend & Web",
            items: [
                { name: "React File Uploads", url: "https://www.geeksforgeeks.org/reactjs/file-uploading-in-react-js/" },
                { name: "JS File Validation", url: "https://www.geeksforgeeks.org/javascript/file-type-validation-while-uploading-it-using-javascript/" },
                { name: "CSS Animations & Keyframes", url: "https://www.w3schools.com/CSSref/atrule_keyframes.php" },
                { name: "Regular Expressions", url: "https://regexr.com/" }
            ]
        },
        {
            category: "Backend & Infrastructure",
            items: [
                { name: "Flask File Uploads", url: "https://flask.palletsprojects.com/en/stable/patterns/fileuploads/" },
                { name: "Secure File Serving", url: "https://pytutorial.com/flask-send_from_directory-serve-files-securely-from-directories/" },
                { name: "Automated File Cleanup", url: "https://www.geeksforgeeks.org/python/delete-files-older-than-n-days-in-python/" },
                { name: "Git Large File Storage (LFS)", url: "https://docs.github.com/en/repositories/working-with-files/managing-large-files" }
            ]
        }
    ];

    return (
        <>
            <div className="header">
                    <div className="headerTitle">
                        <h1>WaveRank</h1>
                        <h1>Credits</h1>
                    </div>
                    <p>Acknowleding the tools, libraries, and resources that made WaveRank possible.</p>
            </div>
            <div className="creditsBoody">
                {credits.map((section, index) => (
                <section key={index} className="creditsOutput">
                    <h3>{section.category}</h3>
                    <ul>
                    {section.items.map((item, idx) => (
                        <li key={idx}><a href={item.url} target="_blank" rel="noopener noreferrer">{item.name}</a></li>
                    ))}
                    </ul>
                </section>
                ))}
            </div>
        </>
    );
};