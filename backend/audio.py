import pyaudio
import wave
import time
import os
import threading
from config import config

class AudioRecorder:
    def __init__(self, format=pyaudio.paInt16, channels=1, rate=16000, chunk=1024, record_seconds_max=5):
        self.format = format
        self.channels = channels
        self.rate = rate
        self.chunk = chunk
        self.record_seconds_max = record_seconds_max
        self.audio = pyaudio.PyAudio()
        self.stream = self.audio.open(format=self.format, channels=self.channels, rate=self.rate,
                                      input=True, frames_per_buffer=self.chunk, start=False)
        self.frames = []
        self.start_record = False
        self.recording = False
        self.thread = None

    def start(self):
        if self.recording:
            print("Already recording!")
            return
        self.thread = threading.Thread(target=self._record)
        self.thread.start()

    def _record(self):
        print("Recording")
        self.start_record = True
        self.frames = []
        self.stream.start_stream()  # Start stream only when recording begins
        self.recording = True

        for _ in range(0, int(self.rate / self.chunk * self.record_seconds_max)):
            if not self.recording:
                print("Break recording!")
                break
            data = self.stream.read(self.chunk)
            self.frames.append(data)
        
        print("Recording completed!")
        self.stream.stop_stream()

    def stop(self):
        time.sleep(0.01)
        if self.start_record:
            self.recording = False
            self.start_record = False
            if self.thread:
                self.thread.join()
            if self.stream:
                self.stream.stop_stream()
            print("Recording stopped!")

            timestamp = int(time.time())  # Get current time in decimal format
            
            # Ensure unique filename
            counter = 1
            file_path = os.path.join(config.AUDIO_FILES, f"{timestamp}_{counter}.wav")
            while os.path.exists(file_path):
                counter += 1
                file_path = os.path.join(config.AUDIO_FILES, f"{timestamp}_{counter}.wav")

            with wave.open(file_path, 'wb') as wf:
                wf.setnchannels(self.channels)
                wf.setsampwidth(self.audio.get_sample_size(self.format))
                wf.setframerate(self.rate)
                wf.writeframes(b''.join(self.frames))
            
            print(f"Audio saved as: {file_path}")
    
    def save_audio(self, file):
        if file.filename == '':
            return "No selected file", 400
        
        if file and file.filename.endswith(".3gp"):
            file_name = os.path.basename(file.filename)
            file_path = os.path.join(config.RECORDINGS, file_name)
            file.save(file_path)

            timestamp = int(time.time())  # Get current time in decimal format

            # Ensure unique filename
            counter = 1
            wav_file_path = os.path.join(config.RECORDINGS, f"{timestamp}_{counter}.wav")
            while os.path.exists(wav_file_path):
                counter += 1
                wav_file_path = os.path.join(config.RECORDINGS, f"{timestamp}_{counter}.wav")

            os.system(f'ffmpeg -i {file_path} {wav_file_path}')
            
            return f"File {file_name} uploaded successfully", 200
        else:
            return "Invalid file type. Only .wav files are allowed.", 400

    def close(self):
        """Closes the stream and PyAudio instance."""
        if self.stream:
            self.stream.close()
        self.audio.terminate()
        print("Audio resources released!")

# Example usage
# if __name__ == "__main__":
#     recorder = AudioRecorder()
#     recorder.start()
#     time.sleep(7)
#     recorder.stop()
#     # # time.sleep(1)
#     recorder.start()
#     # # time.sleep(2)
#     recorder.stop()
#     # # recorder.close()
