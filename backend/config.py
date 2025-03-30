import os
import json
from datetime import datetime

class Config:
    def __init__(self):
        self.debug = True

        # Change this to your base path
        self.BASE_PATH = r"C:\Users\lehuu\Documents\Personal_Project\Football"
        
        self.MODEL = "nguyenvulebinh/wav2vec2-base-vietnamese-250h"

        self.DATE_TIME = datetime.now().strftime("%d-%m-%Y")

        self.LOG = os.path.join(self.BASE_PATH, "log")
        self.MATCH_LOG = os.path.join(self.BASE_PATH, "match_log")
        self.AUDIO_FILES = os.path.join(self.BASE_PATH, "audio_files")
        self.RECORDINGS = os.path.join(self.BASE_PATH, "recordings")
        self.MEMBERS_TXT = os.path.join(self.BASE_PATH, "backend/data/members.txt")
        self.PARAMETERS_JSON = os.path.join(self.BASE_PATH, "backend/data/parameters.json")
        self.WORDS_JSON = os.path.join(self.BASE_PATH, "backend/data/words.json")
        self.MATCH_SCORE_JSON = os.path.join(self.MATCH_LOG, "match_score.json")
        self.PROGRESS_TXT = os.path.join(self.LOG, "progress.txt")
        self.ALL_PROGRESS_TXT = os.path.join(self.LOG, "all_progress.txt")

        # Follow https://www.youtube.com/watch?v=zCEJurLGFRk&t=637s 
        # to create your own credentials.json and sheet id
        # These information are used to update data to google sheet
        self.CREDENTIALS_JSON = os.path.join(self.BASE_PATH, "backend/data/credentials.json")
        self.SHEET_ID = "1pr_sd0uA2SsS1f2_GNW8Ys7g8N2NlfE5YHWdvH0EXiU"

        with open(self.MEMBERS_TXT, 'r', encoding='utf-8') as file:
            self.members = [line.strip() for line in file if line.strip()]

        with open(self.PARAMETERS_JSON, 'r', encoding="utf-8") as file:
            self.parameters = json.load(file)

        with open(self.WORDS_JSON, 'r', encoding='utf-8') as file:
            self.words = json.load(file)

    def print(self, output, data):
        if self.debug:
            with open(output, "a", encoding="utf-8") as file:
                file.write(data)

config = Config()
