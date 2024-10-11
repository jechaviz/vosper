import sounddevice as sd
from scipy.io.wavfile import write
import os

class AudioRecorder:
    def __init__(self, waiting_time=4, filename='speaker'):
        self.recording = sd.rec(int(0 * 44100), samplerate=44100, channels=2)
        self.waiting_time = waiting_time
        self.filename = filename

    def record(self, waiting_time=None):
        if waiting_time is not None:
            self.waiting_time = waiting_time
        self.recording = sd.rec(int(self.waiting_time * 44100), samplerate=44100, channels=2)

    def save(self):
        write(f'{self.filename}.wav', 44100, self.recording)
    
    def stop(self):
        os.system(f'del {self.filename}.wav >nul 2>&1')
        sd.stop()
        self.save()
