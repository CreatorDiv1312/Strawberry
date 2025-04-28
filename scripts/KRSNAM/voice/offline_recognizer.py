import sounddevice as sd
import queue
import json
from vosk import Model, KaldiRecognizer

model_path = "models/vosk-model-small-en-us-0.15"

q = queue.Queue()

def callback(indata, frames, time, status):
    if status:
        print(status)
    q.put(bytes(indata))

def recognize_offline():
    model = Model(model_path)
    recognize = KaldiRecognizer(model, 44100)

    with sd.RawInputStream(samplerate=44100, blocksize=8000, dtype='int16', channels=1, callback=callback):
        print("[GENESIS](OFFLINE): Listening....")
        while True:
            data = q.get()
            if recognize.AcceptWaveform(data):
                result = json.loads(recognize.Result())
                return result.get("text", "")
            
# recognize_offline()

# 16000 earphone ise handle nhi kar payega ye baaki ke case ke liye sahi hai