import time
import os
import glob
import traceback

import sys
sys.path.append(r"C:\Users\lehuu\Documents\Personal_Project\Football\backend")

from backend.config import config
from backend.model import Wav2Vec
from backend.filter import Filter
from backend.update import Sheet
from backend.progress import Progress

class Core:
    def __init__(self):
        self.model = Wav2Vec()
        self.filter = Filter()
        self.sheet = Sheet()
        self.progress = Progress()

        self.output = os.path.join(config.LOG, "core.txt")
        with open(self.output, "w", encoding="utf-8") as file:
            file.write("")

    def run(self):
        while(True):
            time.sleep(0.2)
            audio_files = glob.glob(rf'{config.RECORDINGS}\*.wav')
            if len(audio_files) > 0:
                config.print(self.output, f"Files: {audio_files}\n")

            for audio_file in audio_files:
                try:
                    config.print(self.output, f"File: {audio_file}\n")
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
                    config.print(self.output, f"Execution time: {execution_time:.2f} seconds\n\n")
                
                except FileNotFoundError as e:
                    print(f"File not found: {e}")
                except ValueError as e:
                    print(f"Value error: {e}")
                except Exception as e:
                    # Catch unexpected exceptions and log them
                    print(f"An unexpected error occurred: {e}")
                    traceback.print_exc()  # Print the full traceback for debugging
                except:
                    print("UNKNOWN ERROR")
                
                # Remove file_path
                if os.path.exists(audio_file):
                    os.remove(audio_file)

core = Core()
core.run()
