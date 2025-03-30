import os
from config import config

class Filter:
    def __init__(self):
        self.output = os.path.join(config.LOG, "filter.txt")
        with open(self.output, "w", encoding="utf-8") as file:
            file.write("")
    
    def correct_transcript(self, transcription):
        correct_transcription = ""
        words = transcription.split(" ")
        for word in words:
            match = False
            for correct_word in config.words:
                if word.lower() in config.words[correct_word]:
                    correct_transcription += correct_word + " "
                    match = True
                    break
            if not match:
                correct_transcription += word + " "
        correct_transcription = correct_transcription.strip()
        return correct_transcription
    
    def get_name(self, transcription):
        count = 0
        for member_id, member in enumerate(config.members, 1):
            if member.lower() in transcription.lower():
                name = member
                name_id = member_id
                count += 1
        if count == 1:
            return name, name_id
        return None, None
    
    def get_parameter(self, transcription):
        for data_id, data in enumerate(config.parameters, 1):
            for parameter in config.parameters[data]["acronym"]:
                if parameter in transcription.lower():
                    return data, data_id
        return None, None

    def run(self, transcription):
        correct_transcription = self.correct_transcript(transcription)

        name, name_id = self.get_name(correct_transcription)
        parameter, parameter_id = self.get_parameter(correct_transcription)

        if name is None:
            if parameter is None:
                config.print(self.output, '?????' + '\n')
            else:
                config.print(self.output, parameter + '\n')
        else:
            config.print(self.output, name + ': ' + parameter + '\n')

        return name, name_id, parameter, parameter_id

# filter = Filter()
# name, parameter = filter.run("đạt gi bàn")
# self.output = "filter.txt"
# with open(self.output, "a", encoding="utf-8") as file:
#     file.write(name + ': ' + parameter + '\n')
