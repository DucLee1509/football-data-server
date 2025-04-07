# football-data-server
## How to use

**Note**: Modify base path in **core.py** and **backend/config.py**

There are 2 steps run this server:

1. Run HTTP server
    ```
    python server.py
    ```
2. Bring the server online
    
    There are many ways to bring the server online

    **2.1. ngrok**
    ```
    $ ngrok http 5000
    ```
    Now you will see a http server. (Eg: https://3fae-116-110-42-54.ngrok-free.app).
    
    Use it in your client to communicate with the server.
    
    Note: ngrok has limit requests for free version.
    
    **2.2. localtunnel**
    
    Follow https://theboroer.github.io/localtunnel-www/
    ```
    $ npm install -g localtunnel
    $ lt --port 5000
    ```

**Sample python client app**: check `sample_client.py`
