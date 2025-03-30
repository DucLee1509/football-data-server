from flask import Flask, render_template_string, request, jsonify
import os
import sys
sys.path.append(r"C:\Users\lehuu\Documents\Personal_Project\football-data-server\backend")

from backend.config import config
from core import Core

CoreHandler = Core()

app = Flask(__name__)

template = """
<!DOCTYPE html>
<html>
<head>
    <title>Bluelock Server</title>
    <style>
        html, body {
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            width: 100vw;
            margin: 0;
            background-color: #f0f0f0;
            font-size: 24px;
            font-family: Arial, sans-serif;
        }
    </style>
</head>
<body>
    Data Analysis
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(template)

@app.route('/progress', methods=['GET'])
def progress():
    return CoreHandler.progress.latest_progress(), 200

@app.route('/remove', methods=['GET'])
def remove():
    CoreHandler.remove_latest()
    return "Progress latest remove successfully", 200

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file part", 400
    
    file = request.files['file']
    
    # Convert .3gp to .wav
    wav_file_path = CoreHandler.save_audio(file)

    if wav_file_path is not None:
        err_str =  CoreHandler.run(wav_file_path)
        if err_str is not None:
            return err_str, 400
        else:
            return f"File {os.path.basename(wav_file_path)} is recorded successfully", 200
    else:
        return "Invalid audio file", 400


if __name__ == '__main__':

    app.run(host='0.0.0.0', port=5000, debug=True)
