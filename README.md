# football-data-server
## How to use

**Note**: Modify base path in **core.py** and **backend/config.py**

There are 2 steps run this server:

1. Run HTTP server
```
python server.py
```
2. Run ngrok to bring the server online
```
ngrok http 5000
```
Now you will see a http server. (Eg: https://3fae-116-110-42-54.ngrok-free.app)
Use it in your client to communicate with the server.

For example check `sample_client.py`
