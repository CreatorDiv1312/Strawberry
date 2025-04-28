import speech_recognition as sr
from voice.speaker import speak
from voice.offline_recognizer import recognize_offline



def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("[Genesis] Listening......")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source, phrase_time_limit=5)

        try:
            text = recognizer.recognize_google(audio)
            print("[GENESIS] heared (Gogle):", text)
            return text.lower()
        except sr.UnknownValueError:
            speak("I didn't catch that, Shifting to the other mode of listening.....")
            query = recognize_offline()
            print("[GENESIS] heared about this in offline mode....", query) 
            return query.lower()
        except sr.RequestError:
            speak("No internet, Switching to offline mode.")
            queryof = recognize_offline()
            print("[GENESIS] HEARD IT OFFLINE.....", queryof)
            return queryof.lower()
            # return "[ERROR : Speech Service unavialable]"

# listen()