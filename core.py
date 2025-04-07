import time
import os
import glob
import traceback

import sys
sys.path.append(r"C:\Users\lehuu\Documents\Personal_Project\football-data-server\backend")

from backend.config import Config
from backend.model import Wav2Vec
from backend.filter import Filter
from backend.sheet import Sheet
from backend.progress import Progress

class Core:
    def __init__(self):
        self.model = Wav2Vec()
        self.filter = Filter()
        self.sheet = Sheet()
        self.progress = Progress()
        self.config = Config()

        self.output = os.path.join(self.config.LOG, "core.txt")
        with open(self.output, "w", encoding="utf-8") as file:
            file.write("")
    
    def save_audio(self, file):
        if file.filename == '':
            return None
        
        if file and file.filename.endswith(".3gp"):
            file_name = os.path.basename(file.filename)
            file_path = os.path.join(self.config.RECORDINGS, file_name)
            file.save(file_path)

            timestamp = int(time.time())  # Get current time in decimal format

            # Ensure unique filename
            counter = 1
            wav_file_path = os.path.join(self.config.RECORDINGS, f"{timestamp}_{counter}.wav")
            while os.path.exists(wav_file_path):
                counter += 1
                wav_file_path = os.path.join(self.config.RECORDINGS, f"{timestamp}_{counter}.wav")

            os.system(f'ffmpeg -i {file_path} {wav_file_path}')
            
            return wav_file_path
        else:
            return None

    def audio(self, audio_file):
        err_str = None
        try:
            self.config.print(self.output, f"Audio file: {audio_file}\n")
            start_time = time.time()
            
            # Audio to text
            transcription = self.model.detect(audio_file)

            # Extract name, parameter
            name, name_id, parameter, parameter_id = self.filter.run(transcription)

            # Update progress
            match_score = self.progress.update(name, parameter)

            # Update data
            self.sheet.update(name, name_id, parameter, parameter_id, match_score)

            execution_time = time.time() - start_time
            self.config.print(self.output, f"Execution time: {execution_time:.2f} seconds\n\n")
        
        except FileNotFoundError as e:
            err_str = f"Error: File not found: {e}"
        except ValueError as e:
            err_str = f"Error: Value error: {e}"
        except Exception as e:
            # Catch unexpected exceptions and log them
            err_str = f"Error: An unexpected error occurred: {e}"
            traceback.print_exc()  # Print the full traceback for debugging
        except:
            err_str = "Error: Unknown"

        if err_str is not None:
            self.config.print(self.output, err_str)

        # Remove file_path
        # if os.path.exists(audio_file):
        #     os.remove(audio_file)
        
        return err_str

    def text(self, text):
        err_str = None
        try:
            self.config.print(self.output, f"Text: {text}\n")
            start_time = time.time()

            # Extract name, parameter
            name, name_id, parameter, parameter_id = self.filter.run(text)

            # Update progress
            match_score = self.progress.update(name, parameter)

            # Update data
            self.sheet.update(name, name_id, parameter, parameter_id, match_score)

            execution_time = time.time() - start_time
            self.config.print(self.output, f"Execution time: {execution_time:.2f} seconds\n\n")
        
        except FileNotFoundError as e:
            err_str = f"Error: File not found: {e}"
        except ValueError as e:
            err_str = f"Error: Value error: {e}"
        except Exception as e:
            # Catch unexpected exceptions and log them
            err_str = f"Error: An unexpected error occurred: {e}"
            traceback.print_exc()  # Print the full traceback for debugging
        except:
            err_str = "Error: Unknown"
        
        if err_str is not None:
            self.config.print(self.output + '\n', err_str)

        # Remove file_path
        # if os.path.exists(audio_file):
        #     os.remove(audio_file)
        
        return err_str
    
    def remove_latest(self):
        transcription, match_score = self.progress.remove_latest()
        self.config.print(self.output, f"Removing: {transcription}\n")
        transcription = transcription.replace(":", "")
        name, name_id = self.filter.get_name(transcription)
        parameter, parameter_id = self.filter.get_parameter(transcription)
        self.config.print(self.output, f"name, name_id: {name}, {name_id}\n")
        self.config.print(self.output, f"parameter, parameter_id: {parameter}, {parameter_id}\n")
        self.sheet.remove_latest(name, name_id, parameter, parameter_id, match_score)
