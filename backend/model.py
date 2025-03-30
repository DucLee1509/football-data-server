import os
import librosa
import torch
from transformers import Wav2Vec2Processor, Wav2Vec2ForCTC
from config import config

class Wav2Vec:
    def __init__(self):
        # Load model and processor
        self.processor = Wav2Vec2Processor.from_pretrained(config.MODEL)
        self.model = Wav2Vec2ForCTC.from_pretrained(config.MODEL)

        self.output = os.path.join(config.LOG, "model.txt")
        with open(self.output, "w", encoding="utf-8") as file:
            file.write("")

    def detect(self, audio_file):
        # Load audio and resample to 16 kHz
        speech, sample_rate = librosa.load(audio_file, sr=16000)  

        # Skip files that are too short
        if len(speech) < 10:
            print(f"Skipping {audio_file}, too short!")
            return

        # Tokenize
        input_values = self.processor(speech, sampling_rate=sample_rate, return_tensors="pt", padding="longest").input_values  

        # Predict
        logits = self.model(input_values).logits
        predicted_ids = torch.argmax(logits, dim=-1)
        transcription = self.processor.batch_decode(predicted_ids, skip_special_tokens=True)[0]

        # Write to file
        config.print(self.output, transcription + '\n')

        return transcription
