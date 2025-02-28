import cv2
import numpy as np
from mtcnn import MTCNN

# print("Starting the time")
# Initialize MTCNN detector
detector = MTCNN()

# Start the camera
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Convert frame to RGB (MTCNN works with RGB)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Detect faces
    faces = detector.detect_faces(rgb_frame)

    for face in faces:
        x, y, width, height = face['box']
        confidence = face['confidence']

        # Draw bounding box if confidence > 0.7
        if confidence > 0.7:
            cv2.rectangle(frame, (x, y), (x+width, y+height), (0, 255, 0), 2)
            cv2.putText(frame, f"Face {confidence:.2f}", (x, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Show the output
    cv2.imshow("MTCNN Face Detection", frame)

    # Press 'q' to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
