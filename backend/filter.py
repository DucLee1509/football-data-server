import os
from config import config
from fuzzywuzzy import fuzz

class Filter:
    def __init__(self):
        self.output = os.path.join(config.LOG, "filter.txt")
        with open(self.output, "w", encoding="utf-8") as file:
            file.write("")
    
    def correct_transcript(self, transcription):
        correct_transcription = ""
        words = transcription.lower().split(" ")
        first_word = config.words["first word"]
        other_words = config.words["other words"]

        for i, word in enumerate(words):
            if i == 0:
                word_list = first_word
            else:
                word_list = other_words
            fuzzy_max_score = 0
            best_fuzzy_match = ""
            match = False
            for correct_word in word_list:
                for similar_word in word_list[correct_word]:
                    fuzzy_score = fuzz.ratio(word, similar_word)
                    if fuzzy_score == 100:
                        best_fuzzy_match = correct_word
                        match = True
                        break
                    elif fuzzy_score > fuzzy_max_score:
                        fuzzy_max_score = fuzzy_score
                        best_fuzzy_match = correct_word
                if match:
                    break
            correct_transcription += best_fuzzy_match + " "

        correct_transcription = correct_transcription.strip()
        return correct_transcription
    
    def get_name(self, transcription):
        for member_id, member in enumerate(config.members, 1):
            if f"{member.lower()} " in transcription.lower():
                name = member
                name_id = member_id
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
        config.print(self.output, correct_transcription + ' -> ')

        name, name_id = self.get_name(correct_transcription)
        parameter, parameter_id = self.get_parameter(correct_transcription)

        if name is None:
            if parameter is None:
                config.print(self.output, '?????' + '\n')
            else:
                config.print(self.output, parameter + '\n')
        else:
            if parameter is None:
                config.print(self.output, name + ': ?????' + '\n')
            else:
                config.print(self.output, name + ': ' + parameter + '\n')

        return name, name_id, parameter, parameter_id

filter = Filter()
name, name_id, parameter, parameter_id = filter.run("đạt chyền tốt")
