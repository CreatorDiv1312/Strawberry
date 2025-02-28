import cv2
import numpy as np
from mtcnn import MTCNN
import time 
import math


# print("Starting the time")
# Initialize MTCNN detector
detector = MTCNN()

# Start the camera
cap = cv2.VideoCapture(0)

# previous faces ko store karna hooga 
previous_faces = {}

# frame rate calculations 
prev_time = time.time()


while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab")
        break

    # Convert frame to RGB (MTCNN works with RGB)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Detect faces
    faces = detector.detect_faces(rgb_frame)

    # fps calculation ke liye current time ka calculation 
    curr_time = time.time()
    time_diff = curr_time - prev_time #time difference between frames
    prev_time = curr_time #Update previous time

    current_faces = {}

    for face in faces:
        x, y, width, height = face['box']
        confidence = face['confidence']
        center_x, center_y = x + width // 2, y + height // 2 #capturing  the face center 


        # Store the new face location 
        face_id = f"{center_x}-{center_y}"
        current_faces[face_id] = (center_x, center_y)

        # If this face was detected in the previous frame, we will calculate speed
        if face_id in previous_faces:
            prev_x, prev_y = previous_faces[face_id]

            # Calculate Euclidiean distance 
            distance_pixels = math.sqrt((center_x - prev_x) ** 2 + (center_y - prev_y) ** 2)

            # Convert pixel speed to real speed (assumption is 30 fps == 1m/s )
            if time_diff > 0:
                speed = distance_pixels / time_diff #Pixelper seconds 
            else:
                speed = 0

        else:
            speed = 0 #Assuming a new rest object to be in rest

        #Draw speed text 
            cv2.putText(frame, f'Speed: {speed:.2f} px/sec', (x,y - 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
        # Draw bounding box if confidence > 0.7
        if confidence > 0.7:
            cv2.rectangle(frame, (x, y), (x+width, y+height), (0, 255, 0), 2)
            cv2.putText(frame, f"Face {confidence:.2f}", (x, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    # Updatingthe previous faces with current detected faces                        
    previous_faces = current_faces.copy()

    # Show the output
    cv2.imshow("MTCNN Face Detection", frame)

    # Press 'q' to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
