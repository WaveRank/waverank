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
Non-simultaneous use version:
```
newman run tests/postman/WaveRank-sequential.postman_collection.json -e tests/postman/WaveRank-Local.postman_environment.json
```

## Building the model from source data
Set up virtual environment and dependencies.
```
python3 -m venv env
source env/bin/activate
# pip install -r requirements.txt
```
Acquire source audio files.
You can get the dataset we used from 
https://www.kaggle.com/datasets/andradaolteanu/gtzan-dataset-music-genre-classification
This dataset is already sorted into genres. Copy the 'genres_original' directory
into 'data/' so you have 'data/genres_original', with all the genre subdirectories
inside.

Alternatively, you could use any other sorted dataset by instead placing that one's
genres in 'data/genres_original'. This should work with any number or type of genres.
Combining multiple datasets is technically possible but you would ideally want to
control for duplicate songs, overlapping genres, etc.

### Preprocessing
Split the dataset into training, validation, and test directories, 
segment the original .wav files, and convert the segments to spectrograms.
```
python -m model.src.preprocessing.1_distribute_dataset
python -m model.src.preprocessing.2_segment_dataset
python -m model.src.preprocessing.3_wav_to_spectrogram
```
### Training
#### Enabling GPU usage
Note: Training the model can take a very long time. Utilizing a GPU, e.g. via 
tensorflow-with-cuda, can speed up this process. You will need to install
the appropriate package and export it to python's env path to enable it.
With an Nvida GPU, it might be something like:
```
export LD_LIBRARY_PATH=$(find $VIRTUAL_ENV/lib/python3.10/site-packages/nvidia -type d -name lib | tr "\n" ":"):$LD_LIBRARY_PATH
```
You can test that your GPU is working with Tensorflor with this command. 

```
python -c "import tensorflow as tf; print(tf.config.list_physical_devices('GPU'))"
```
If you see a GPU listed at the end, you know it is working, e.g.:
```
[PhysicalDevice(name='/physical_device:GPU:0', device_type='GPU')]
```

#### Building the trained CNN model
Use these commands to build the trained model from the spectrogram images. The
model will be saved as 'model/artifacts/final_model.keras'.
```
python -m model.src.model_training.main
python -m model.src.model_training.tune
```
Note: performing some other tasks with your pc while this is running may cause
Tensorflow to become unstable.
Note: training time can be decreased by lowering the number of training epochs
and fine tuning epochs in model/src/config.py.

### Inference testing
To test the inference pipeline and get genre predictions on any number of songs,
place them in data/test_songs and run the following command. Output will be saved
as tests/artifacts/inference_test_results.json.
```
python -m tests.test_inference
```
Alternatively, the web app uses the same inference pipeline.