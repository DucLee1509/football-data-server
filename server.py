from flask import Flask, render_template_string, request, jsonify
import sys
sys.path.append(r"C:\Users\lehuu\Documents\Personal_Project\Football\backend")

from backend.audio import AudioRecorder
from backend.progress import Progress
from backend.update import Sheet
from backend.config import config

Recorder = AudioRecorder()
MatchProgress = Progress()
sheet = Sheet()

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
    with open(config.PROGRESS_TXT, 'r', encoding='utf-8') as file:
        first_line = file.readline()
    return first_line, 200

@app.route('/remove', methods=['GET'])
def remove():
    MatchProgress.remove_latest()
    sheet.match_score = MatchProgress.match_score[config.DATE_TIME]
    sheet.update_match_core()
    return "Progress latest remove successfully", 200

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file part", 400
    
    file = request.files['file']
    
    return Recorder.save_audio(file)

if __name__ == '__main__':

    app.run(host='0.0.0.0', port=5000, debug=True)
