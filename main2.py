import os
import traceback
import csv
import json 
import smtplib
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from  watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import subprocess


SCRIPTS_FOLDER = "scriptfol"
LOG_TEXT_FILE = "logtxt"
LOG_JSON_FILE = "logjs"
LOG_EXCEL_FILE = "logexec"
ENABLE_STATIC_ANALYSIS = True
SEND_EMAIL_ALERTS = False
EMAIL_TO = "" #emailid of mine
EMAIL_FROM = "" #email of server
# EMAIL_SERVER = "" #EMAIL OF SERVER
SMTP_SERVER = "" #SMTP 
SMTP_PORT = 587

SMTP_USER = ""
SMTP_PASS = ""


error_log_data = []

def analyze_script(file_path):
    log_entry = {
        "filename":os.path.basename(file_path),
        "timestamp":datetime.now().isoformat(),
        "errors":[],
        "pylint_score":None
    }

    try:
        with open(file_path, 'r') as f:
            code = f.read()
        compile(code, file_path, 'exec')
        exec(code, {})
    except Exception as e:
        tb = traceback.format_exc()
        log_entry["errors"].append(tb)
    
    if ENABLE_STATIC_ANALYSIS:
        try:
            result = subprocess.run(["pylint",file_path, "--score" , "y"] , capture_output= True , text= True )
            score_line = [line for line in result.stdout.splitlines() if "your code has been rated at " in line ]
            if score_line:
                score = score_line[0].split("at")[-1].strip()
                log_entry["errors"] = score
        except Exception as e:
            log_entry["pylint_score"] = "analysis failed"  

    if log_entry["errors"]:
        error_log_data.append(log_entry)
        log_to_text()
        log_to_json()
        log_to_excel() 
        if SEND_EMAIL_ALERTS:
            send_email_alerts()
            #argument dalna hai
def log_to_text(log_entry):
    with open(LOG_TEXT_FILE , "a") as f:
        f.write(f"\n timestamp:{log_entry["timestamp"]}\nfile_name:{log_entry["filename"]}")
        if log_entry["errors"]:
            for error in log_entry["errors"]:
                f.write(f"errors:{error}")
        if log_entry["pylint_score"]:
            f.write(f"\nscore:{log_entry["pylint_score"]}")        
             
def log_to_json():
    with open(LOG_JSON_FILE, 'w') as f:
        json.dump(error_log_data , f , indent = 2)       

def log_to_excel():
    with open(LOG_EXCEL_FILE , 'w', newline = " ") as f:
        writer = csv.writer(f)
        writer.writerow(["timestamp" , "filename" , "error" , "pylint_score"])
        for entry in error_log_data:
            errorstr = "\n".join(entry["error"])
            writer.writerow(entry["timestamp"] , entry["filename"] , errorstr , entry["pylint_score"])

def send_email_alerts(log_entry):
    msg = MIMEMultipart()
    msg['From'] = EMAIL_FROM
    msg['To'] = EMAIL_TO
    msg['Subject'] = f"error in {log_entry['filename']}"
    body = f"time:{log_entry['timestamp'] , log_entry['filename']}"     
    for error in log_entry["errors"]:
        body += f"{error}"
    if log_entry["pylint_score"]:
        body += f"{log_entry["pylint_score"]}"
    msg.attach(MIMEText(body , 'plain'))
    with smtplib.SMTP(SMTP_SERVER , SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_USER , SMTP_PASS)
        server.send_message(msg)    

class ScryptChangeHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path.endswith(".py"):
            analyze_script(event.src_path)

    def on_created(self, event):
        if event.src_path.endswith(".py"):
            analyze_script(event.src_path)


if __name__ == "__main__":
    if not os.path.exists(SCRIPTS_FOLDER):
        os.makedirs(SCRIPTS_FOLDER)
    for file in os.listdir(SCRIPTS_FOLDER):
        if file.endswith(".py"):
            analyze_script(os.path.join(SCRIPTS_FOLDER , file)) 

    observer = Observer()
    eventhandler = ScryptChangeHandler
    observer.schedule(eventhandler , SCRIPTS_FOLDER , recursive = False)
    observer.start()
    print("observing start")
    print("[autoerrorscan]for monitoring script changes.. press ctrl + c to exit  ")

    try:
        while True:
            pass           
    except KeyboardInterrupt:
        observer.stop()

    observer.join()            

