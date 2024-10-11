import os
import pyaudio
import whisper
import recorder
from vosk import SetLogLevel, Model, KaldiRecognizer
import time

SetLogLevel(-1)
os.system('cls' if os.name == 'nt' else 'clear')

class VosperRecognizer:
    def __init__(self, vosk_model='small', whisper_model='small.en', waiting_time=4, filename='speaker', verbosity=True):
        self.verbosity = verbosity
        self.log('- loading models...')
        self.recorder = recorder.AudioRecorder(waiting_time, filename='speaker')
        self.whisper = whisper.load_model(whisper_model)
        self.vosk = self._load_vosk(vosk_model)
        self.recording_whisper = False
        self.filename = filename
        self.mic = self._stream()
        self.silence_start = None
        self.silence_threshold = 1.0  # segundos

        self.log(f'- waiting time:   {waiting_time} seconds\n- vosk model:     {vosk_model}\n- whisper model:  {whisper_model}\n- recording file: {filename}')

    def _load_vosk(self, model='small'):
        model_voice = Model(f'{os.getcwd()}/models/vosk/{model}')
        return KaldiRecognizer(model_voice, 16000)

    def _stream(self):
        mic = pyaudio.PyAudio()
        _stream = mic.open(
            channels=1,
            rate=16000,
            input=True,
            format=pyaudio.paInt16, 
            frames_per_buffer=4096
        )
        _stream.start_stream()
        os.system('cls' if os.name == 'nt' else 'clear')
        return _stream

    def log(self, msg):
        if self.verbosity:
            print(msg)

    def listen(self):
        data = self.mic.read(4096)

        if self.vosk.AcceptWaveform(data):
            self.recorder.stop()
            text = self.vosk.Result()[14:-3]
            if len(text) > 3:
                text = self.whisper.transcribe(f'{self.filename}.wav', language="es", task="transcribe")['text'].strip()
            self.recording_whisper = False
            self.silence_start = None
            return text
        else:
            partial_text = self.vosk.PartialResult()[17:-3]
            if partial_text:
                self.silence_start = None
                if not self.recording_whisper:
                    self.recorder.stop()
                    self.recording_whisper = True
                    self.recorder.record(5)
            elif self.silence_start is None:
                self.silence_start = time.time()
            elif time.time() - self.silence_start > self.silence_threshold:
                self.recording_whisper = False
                self.silence_start = None
                return ''
        
        return None
