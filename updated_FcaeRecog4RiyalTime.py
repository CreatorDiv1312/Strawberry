import cv2
import sqlite3
import datetime
from simple_facerec import SimpleFacerec

# Initialize Face Recognition
sfr = SimpleFacerec()
sfr.load_encoding_images("D:/coding/python/face_recognition/images/")

# Connect to SQLite Database
conn = sqlite3.connect("face_recognition.db")
cursor = conn.cursor()

# Create Users Table (Stores Registered Users)
cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL,
        registered_on DATETIME DEFAULT CURRENT_TIMESTAMP
    )
""")

# Create Face Recognition Logs Table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS face_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        detected_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
""")
conn.commit()

# Function to Register User (Only If Not Exists)
def register_user(name):
    cursor.execute("SELECT id FROM users WHERE name = ?", (name,))
    result = cursor.fetchone()
    if not result:
        cursor.execute("INSERT INTO users (name) VALUES (?)", (name,))
        conn.commit()
        print(f"✅ New User Registered: {name}")
    return cursor.execute("SELECT id FROM users WHERE name = ?", (name,)).fetchone()[0]

# Function to Log Face Detection
def log_face_detection(name):
    user_id = register_user(name)  # Ensure user is registered
    last_seen = cursor.execute(
        "SELECT detected_at FROM face_logs WHERE user_id = ? ORDER BY detected_at DESC LIMIT 1",
        (user_id,)
    ).fetchone()

    # Insert a log only if the last detection was more than 5 minutes ago
    if not last_seen or (datetime.datetime.now() - datetime.datetime.strptime(last_seen[0], "%Y-%m-%d %H:%M:%S")).total_seconds() > 300:
        cursor.execute("INSERT INTO face_logs (user_id) VALUES (?)", (user_id,))
        conn.commit()
        print(f"📌 Face Detected & Logged: {name} at {datetime.datetime.now()}")
    else:
        print(f"⏳ {name} was seen recently, skipping duplicate log.")

# Load Camera
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()

    # Detect Faces
    face_locations, face_names = sfr.detect_known_faces(frame)
    
    for face_loc, name in zip(face_locations, face_names):
        y1, x2, y2, x1 = face_loc[0], face_loc[1], face_loc[2], face_loc[3]

        # Display Name on Frame
        cv2.putText(frame, name, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 200), 2)
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 200, 400), 2)

        # Log Face Detection in SQLite
        if name != "Unknown":
            log_face_detection(name)

    cv2.imshow("Frame", frame)

    # Press ESC to Exit
    key = cv2.waitKey(1)
    if key == 27:
        break

# Cleanup
cap.release()
cv2.destroyAllWindows()
conn.close()