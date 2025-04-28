import speech_recognition as sr
import numpy as np
import io
import wave
import os
from datetime import datetime 

MIC_FAILURE_LOG = "logs/mic_failure.log"

def log_failure(reason):
    os.makedirs("logs", exist_ok=True)
    with open(MIC_FAILURE_LOG, 'a') as f:
        f.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | {reason}\n")

def diagnose_microphone():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("GENESIS: Running  mic diagnonistics....")

        recognizer.adjust_for_ambient_noise(source, duration=1)
        print("[GENESIS]: Please Say Something.....")
        audio = recognizer.listen(source, phrase_time_limit=3)

        # Coverting audio to waveform
        raw_data = audio.get_wav_data()
        wav_file = wave.open(io.BytesIO(raw_data))
        frames = wav_file.readframes(wav_file.getnframes())
        samples = np.frombuffer(frames,dtype=np.int16)

        # AnalyzeVolumes
        volume = np.abs(samples).mean()
        noise = np.abs(samples[:1000]).mean()
        clarity = volume-noise
        # first part = ambient noise
        
        print(f'[DEBUG] Avg Volume:{volume:2f}, Background noise:{noise:2f}')

        # Diaognisis Think like a  doctor 

        # Adapting the threshold logic like a pro!!

        if volume < 300:
            recognizer.energy_threshold = 250
            reason = "Mic input too low. Try speaker louder or use a better mic"
            log_failure(reason)
            return reason
        elif noise > 500:
            reason = "Too much background Noise. Try moving  to a quieter place"
            return reason
            # return "Too much background Noise. Try moving  to a quieter place"
        elif clarity < 200:
            reason = "Voice is not clear over the background. Try speaking closer the  mic."
            return reason
            # return "Voice is not clear over the background. Try speaking closer the  mic."
        else:
            return "Mic is working fine. GENESIS READY TO WORK SIR."
        
    