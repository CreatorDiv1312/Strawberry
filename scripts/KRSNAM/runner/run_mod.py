import sys
import os 
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),'..')))

import time
from voice.listener import listen
from voice.speaker import speak
from core.mind import think
from utils.logger import log_event
# from memory.memory_core import 
from voice.self_check import diagnose_microphone

speak("Gensis has successfully activated.Good morning Mummy, Genesis here, litening....")

log_event("Krsnam_activated")

diagonisis = diagnose_microphone()
print(f"GENESIS: {diagonisis}")

if "Mic is working fine" not in diagonisis:
    speak("Warning!! Mic test has been failed and your voice seems unclear.")
    speak("I will still proceed. But i may not hear you clearly.")
    
while True:
    query = listen()
    if query:
        log_event(f"Heard : {query}")
        response = think(query)
        speak(response)
        log_event(f"Responded: {response}")
        if "exit" in query.lower():
            log_event("Genesis shoutdown command has been initiated.")
            break
    time.sleep(1)


