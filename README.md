# WaveRank
WaveRank is a web app that classifies the top music genres of an audio file using a CNN trained on mel-scaled spectrogram features. Upload an audio file or paste a YouTube URL to get genre predictions along with waveform, frequency spectrum, and mel spectrogram visualizations.

<!-- SCREENSHOT: Homepage with example results -->

## Using the Hosted Website
WaveRank is hosted at **[HOSTED URL HERE]**. No login required.
 
1. Click **Upload Audio File** to upload a `.wav`, `.mp3`, or `.mp4` file (max 10MB), or click **Paste URL** to enter a YouTube link.
2. Wait for the audio to process, this may take a few seconds.
3. View your genre predictions and audio visualizations while you listen to your song on the built-in audio player.
> Note: YouTube URL uploads do not support livestreams, age-restricted content, private videos, or videos over 10 minutes.
 
<!-- SCREENSHOT: Upload popups -->
<!-- SCREENSHOT: Results with genre bars and graphs -->
 
---

## Local Development Setup
 
### Prerequisites
- Python 3.10.12 
- Node.js v20.20.2
- ffmpeg (see below)

#### Installing ffmpeg
ffmpeg is required for YouTube audio downloads.
 
**Linux (Ubuntu/Debian):**
```
sudo apt update
sudo apt install ffmpeg
```
 
**Mac:**
```
brew install ffmpeg
```
 
**Windows:**
1. Download ffmpeg from https://ffmpeg.org/download.html
2. Extract the zip and copy `ffmpeg.exe` from the `bin` folder
3. Add the folder containing `ffmpeg.exe` to your system PATH

**Verify installation:**
```
ffmpeg -version
```
 
---
 
### Frontend
```
cd webapp/client
# npm install  (run once)
npm run dev
```
 
### Backend
 
**Linux/Mac:**
```
python3 -m venv env
source env/bin/activate
# pip install -r requirements.txt  (run once)
python -m scripts.run_server
```
 
**Windows:**
```
python -m venv env
env\Scripts\activate
# pip install -r requirements.txt  (run once)
python -m scripts.run_server
```

---

## Server Testing
Automated testing of the server API. Three collections run in parallel to simulate simultaneous requests.
Requires Newman (`npm install -g newman`). Run from the project root with the server already running.

**Parallel (faster):**
```
newman run tests/postman/WaveRank-1.postman_collection.json -e tests/postman/WaveRank-Local.postman_environment.json &
newman run tests/postman/WaveRank-2.postman_collection.json -e tests/postman/WaveRank-Local.postman_environment.json &
newman run tests/postman/WaveRank-3.postman_collection.json -e tests/postman/WaveRank-Local.postman_environment.json &
wait

```

**Single-threaded:**
```
newman run tests/postman/WaveRank-single-threaded.postman_collection.json -e tests/postman/WaveRank-Local.postman_environment.json
```

## Building the model from source data
> **Note:** A pre-trained model is already included in the repository. This section is only necessary if you want to retrain the model from scratch, which is *NOT* needed to run the web app!

### Prepare raw data
Sort source `.wav` audio files into directories named after each genre, and 
place them within `data/genres_original`.

### Preprocessing
Split the dataset into training, validation, and test directories, 
segment the original `.wav` files, and convert the segments to spectrograms. Wait for each command to finish before running the next.
```
python -m model.src.preprocessing.1_distribute_dataset
python -m model.src.preprocessing.2_segment_dataset
python -m model.src.preprocessing.3_wav_to_spectrogram
```
### Training
Training the model can take a very long time! Utilizing a GPU, e.g. via 
`tensorflow-with-cuda`, can greatly speed up this process. You will need to install
the appropriate package and export it to python's env path to enable it.
With an Nvidia GPU, it might be something like:
```
export LD_LIBRARY_PATH=$(find $VIRTUAL_ENV/lib/python3.10/site-packages/nvidia -type d -name lib | tr "\n" ":"):$LD_LIBRARY_PATH
```
> For GPU setup instructions specific to your system, see the [TensorFlow GPU guide](https://www.tensorflow.org/install/pip#gpu).

> **Note:** Do not run other intensive tasks while training — this may cause TensorFlow to become unstable.

Train the CNN model using the spectrogram dataset:
```
python -m model.src.model_training.main
```

Optionally, run hyperparameter tuning via Optuna:
<!-- TODO: Get more information from Angie about what tune.py does and recommended order of operations -->
```
python -m model.src.model_training.tune
```
> Note: performing some other tasks with your pc while this is running may cause
Tensorflow to become unstable.

### Inference Testing
Place test songs in `data/test_songs` and run:
```
python -m tests.test_inference
```
Output will be saved to `tests/artifacts/inference_test_results.json`.

---
 
## Contributors
 
| Name | GitHub | Role |
|------|--------|------|
| Emily Huntley | <!-- @github --> | <!-- Role --> |
| Kevin Klein | <!-- @github --> | <!-- Role --> |
| Madeline Rachow | <!-- @github --> | <!-- Role --> |
| Angela Shin | <!-- @github --> | <!-- Role --> |
 
---
 
## Known Issues
 
<!-- TODO: Add known issues before final submission -->
 
---


## Acknowledgements

WaveRank was built with the help of the following tools, libraries, and resources. See the website for even more details.

<table>
  <thead>
    <tr>
      <th>Category</th>
      <th>Resource</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Dataset</td>
      <td><a href="https://www.tensorflow.org/datasets/catalog/gtzan">GTZAN Genre Collection</a></td>
    </tr>
    <tr>
      <td rowspan="3">Deep Learning & AI</td>
      <td><a href="https://www.tensorflow.org/api_docs">TensorFlow & Keras</a></td>
    </tr>
    <tr>
      <td><a href="https://www.tensorflow.org/guide/keras/transfer_learning">ResNet50 & Transfer Learning</a></td>
    </tr>
    <tr>
      <td><a href="https://keras.io/keras_tuner/api/tuners/bayesian/">Keras Tuner (Bayesian Optimization)</a></td>
    </tr>
    <tr>
      <td rowspan="3">Audio Processing</td>
      <td><a href="https://librosa.org/doc/main/generated/librosa.feature.melspectrogram.html">Librosa</a></td>
    </tr>
    <tr>
      <td><a href="https://medium.com/analytics-vidhya/understanding-the-mel-spectrogram-fca2afa2ce53">Understanding Mel Spectrograms</a></td>
    </tr>
    <tr>
      <td><a href="https://github.com/yt-dlp/yt-dlp">yt-dlp</a></td>
    </tr>
    <tr>
      <td rowspan="2">Metrics & Visualization</td>
      <td><a href="https://scikit-learn.org/stable/modules/generated/sklearn.metrics.roc_curve.html">Scikit-Learn</a></td>
    </tr>
    <tr>
      <td><a href="https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.legend.html">Matplotlib</a></td>
    </tr>
    <tr>
      <td rowspan="2">Frontend & Web</td>
      <td><a href="https://react.dev/">React</a></td>
    </tr>
    <tr>
      <td><a href="https://flask.palletsprojects.com/">Flask</a></td>
    </tr>
  </tbody>
</table>