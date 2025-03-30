from config import config
import json

class Progress:
    def __init__(self):
        with open(config.MATCH_SCORE_JSON, 'r', encoding='utf-8') as file:
            self.match_score = json.load(file)
        if config.DATE_TIME not in self.match_score:
            self.match_score[config.DATE_TIME] = "0 - 0"
        with open(config.MATCH_SCORE_JSON, 'w') as file:
            json.dump(self.match_score, file)
        score = self.match_score[config.DATE_TIME].split(" - ")
        self.team_score = int(score[0])
        self.opponent_score = int(score[1])
        self.PROGRESS_LEN = 50
        with open(config.ALL_PROGRESS_TXT, 'r', encoding='utf-8') as file:
            self.progress = file.read().splitlines()
        if len(self.progress) < self.PROGRESS_LEN:
            self.progress = ["" for i in range(self.PROGRESS_LEN)]
        self.progress_txt = ""

        with open(config.PROGRESS_TXT, "w", encoding="utf-8") as file:
            file.write("")

    def update_match_score(self):
        self.match_score[config.DATE_TIME] = str(self.team_score) + " - " + str(self.opponent_score)
        with open(config.MATCH_SCORE_JSON, 'w') as file:
            json.dump(self.match_score, file)
    
    def update_progress(self):
        self.progress_txt = self.match_score[config.DATE_TIME] + "|"
        for progress in self.progress[-3:]:
            self.progress_txt += f"{progress}|"
        with open(config.PROGRESS_TXT, 'w', encoding="utf-8") as file:
            file.write(self.progress_txt)
        
        with open(config.ALL_PROGRESS_TXT, 'w', encoding="utf-8") as file:
            for progress in self.progress:
                file.write(f"{progress}\n")

    def add(self, name, parameter):
        self.progress.pop(0)
        if parameter is not None:
            if name is not None:
                self.progress.append(f"{name}: {parameter}")
            else:
                self.progress.append(f"{parameter}")
        else:
            self.progress.append("?????")
    
    def remove(self):
        self.progress.pop()
        self.progress.insert(0, "")

    def latest_progress(self):
        return self.progress_txt

    def update(self, name, parameter):
        self.add(name, parameter)

        if parameter == "Bàn thắng":
            self.team_score += 1
            self.update_match_score()
        
        if parameter == "Bàn thua":
            self.opponent_score += 1
            self.update_match_score()
        
        self.update_progress()

        return self.match_score[config.DATE_TIME]

    def remove_latest(self):
        transcription = self.progress[-1]
        if ": " in transcription:
            parameter = transcription.split(": ")[1]
        else:
            parameter = transcription

        if parameter == "Bàn thắng":
            self.team_score -= 1
            self.update_match_score()
        
        if parameter == "Bàn thua":
            self.opponent_score -= 1
            self.update_match_score()

        self.remove()
        self.update_progress()

        return transcription, self.match_score[config.DATE_TIME]

# progress = Progress()
# progress.update(None,None)
# progress.remove_latest()
# progress.update("Đạt", "Bàn thắng")
# progress.update(None, "Bàn thua")
# progress.update("Vũ", "Sai lầm")
# progress.update("Nam", "Kiến tạo")
