from datetime import datetime

def log_event(event):
    with open("krsnam_log.txt",'a') as f:
        f.write(f"[{datetime.now()}] {event}\n")

        