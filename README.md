# WaveRank

## How to run web app
Installation lines (commented out) should be run once

### linux

#### frontend
```
cd webapp/client
# npm install
npm run dev
```

#### backend
```
python3 -m venv env
source env/bin/activate
# pip install -r webapp/server/requirements.txt
python -m scripts.run_server
```

## Server testing
Automated testing of server API surface. 
Three scripts run in parallel to simulate simultaneous requests (and finish faster).
Needs to be run from project root, with server running.
```
newman run tests/postman/WaveRank-1.postman_collection.json -e tests/postman/WaveRank-Local.postman_environment.json &
newman run tests/postman/WaveRank-2.postman_collection.json -e tests/postman/WaveRank-Local.postman_environment.json &
newman run tests/postman/WaveRank-3.postman_collection.json -e tests/postman/WaveRank-Local.postman_environment.json &
wait

```
Single-threaded version:
```
newman run tests/postman/WaveRank-single-threaded.postman_collection.json -e tests/postman/WaveRank-Local.postman_environment.json
```

## Building the model from source data
Sort source .wav audio files into directories named after each genre, and 
place them within data/genres_original.
### Preprocessing
Split the dataset into training, validation, and test directories, 
segment the original .wav files, and convert the segments to spectrograms.
```
python -m model.src.preprocessing.1_distribute_dataset
python -m model.src.preprocessing.2_segment_dataset
python -m model.src.preprocessing.3_wav_to_spectrogram
```
### Training
Note: Training the model can take a very long time. Utilizing a GPU, e.g. via 
tensorflow-with-cuda, can speed up this process. You will need to install
the appropriate package and export it to python's env path to enable it.
With an Nvida GPU, it might be something like:
```
export LD_LIBRARY_PATH=$(find $VIRTUAL_ENV/lib/python3.10/site-packages/nvidia -type d -name lib | tr "\n" ":"):$LD_LIBRARY_PATH
```

Build a trained CNN model using the spectrogram dataset. 
Note: performing some other tasks with your pc while this is running may cause
Tensorflow to become unstable.
```
python -m model.src.model_training.main
python -m model.src.model_training.tune
```
### Inference testing
To run songs through the model and get genre predictions, put the test songs
in data/test_songs and run the following command. Output will be saved
as tests/artifacts/inference_test_results.json
```
python -m tests.test_inference
```