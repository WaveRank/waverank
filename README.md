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
source webapp/server/env/bin/activate
# pip install -r webapp/server/requirements.txt
python run_server.py
```

## Server testing
Automated testing of server API surface. 
Three scrips run in parallel to simulate simultaneous accesses (and finish faster).
Needs to be run from project root.
```
newman run tests/postman/WaveRank-1.postman_collection.json -e tests/postman/WaveRank-Local.postman_environment.json &
newman run tests/postman/WaveRank-2.postman_collection.json -e tests/postman/WaveRank-Local.postman_environment.json &
newman run tests/postman/WaveRank-3.postman_collection.json -e tests/postman/WaveRank-Local.postman_environment.json &
wait

```