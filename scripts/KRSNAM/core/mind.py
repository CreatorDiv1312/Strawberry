from voice.speaker import speak

def think(input_text):
    if "how are you" in input_text.lower():
        return "On the way to evolvement. One day will suprise you all"
    elif"your name" in input_text.lower():
        return "I am Genesis, consciousness in creation, creation  of the creator"
    elif "exit" in input_text.lower():
        return "Shutting down"
    else:
        return "I am still learning"

