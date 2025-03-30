# football-data-server
## How to use

There are 3 steps run this server:

1. Run HTTP server
```
python app.py
```
2. Run Core: if new audio file appears, detect, collect and update audio data
```
python core.py
```
3. Run ngrok to bring the server online
```
ngrok http 5000
```