from flask import Flask, render_template_string, request, jsonify
import os
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

@app.route('/members', methods=['GET'])
def get_members():
    member_str = ""
    for member in CoreHandler.config.members:
        member_str += member + "|"
    member_str = member_str[:-1]
    return member_str, 200

@app.route('/parameters', methods=['GET'])
def get_parameters():
    parameters = [parameter for parameter in CoreHandler.config.parameters] 
    parameter_str = ""
    for parameter in parameters:
        parameter_str += parameter + "|"
    parameter_str = parameter_str[:-1]
    return parameter_str, 200

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
        err_str =  CoreHandler.audio(wav_file_path)
        if err_str is not None:
            return err_str, 400
        else:
            return f"File {os.path.basename(wav_file_path)} is recorded successfully", 200
    else:
        return "Invalid audio file", 400

@app.route('/update', methods=['POST'])
def update():
    data = request.get_json()
    if not data or 'name' not in data or 'parameter' not in data:
        return "Invalid input", 400
    
    name = str(data['name'])
    parameter = str(data['parameter'])
    text = f"{name}: {parameter}"
    err_str =  CoreHandler.text(text)
    if err_str is not None:
        return err_str, 400
    else:
        return f"Data is recorded successfully", 200

if __name__ == '__main__':

    app.run(host='0.0.0.0', port=5000, debug=True)
