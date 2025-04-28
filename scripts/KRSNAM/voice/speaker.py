import pyttsx3

engine = pyttsx3.init()
engine.setProperty('rate', 160)
engine.setProperty('volume', 0.9)

# Speak function 
def speak(text):
    print(f"[Genesis]:{text}")
    engine.say(text)
    engine.runAndWait()

