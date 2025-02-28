import cv2
import time 
import numpy as np
# from mtcnn import MTCNN

# ab pre trained model ka abhi ke liye use karta hu for human detection 
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

# initializing the MTCNN detector 
# detector = MTCNN()

# camera start kar raha 
cap = cv2.VideoCapture(0) # 0 isliye rakha hai kyunki mujhe pre recorded jana nhi hai live record karna hai


# ab set bananan start kar raha jisme previous positions ko store karunga isse mai speed calculation kar paunga
previous_positions = {}
fps = cap.get(cv2.CAP_PROP_FPS) # get camera FPS

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    start_time = time.time() #time to start frame processing.

    # frame ko resize karna start kar diya jaye 
    frame = cv2.resize(frame, (640,480))
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect humans 
    print("human Detetction started")
    boxes, _ = hog.detectMultiScale(gray, winStride=(8,8), padding=(8,8), scale=1.05)
    print("human Detection is starting")
    # ab yaha new positions jo human ke flow ko hogi wo dikhayenge 
    new_positions = {}
    print(f"{new_positions}")

    for i, (x,y,w,h) in enumerate(boxes):
        print("Inside for loop")
        center_x = x+w // 2
        center_y = y+h // 2

        # ab analyse karega to ek bounding box banana padega 
        cv2.rectangle(frame, (x,y), (x+w, y+h), (0, 255, 0), 2)

        # ab is ek box ki speed ko calculate karwaunga 
        if i in previous_positions:
            prev_x, prev_y = previous_positions[i]
            distance = np.sqrt((center_x - prev_x)**2 + (center_y - prev_y) ** 2)
            # Roughly speed ki value nikal leta hu 
            speed = distance * fps
            cv2.putText(frame, f"Speed: {speed: .2f} px/sec", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX,0.5, (0,0,255),2)
            print(f"{speed} km/sec")

        # storing new positions now 
        new_positions[i] = (center_x, center_y)
        
    previous_positions = new_positions.copy() #updating the previous position
    end_time = time.time()
    processing_time = end_time - start_time

    cv2.putText(frame, f"Processing Time: {processing_time:.2f} sec", (10,30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)


    # TESTING PURPOSE KE LIYE FRAME show karwata hu and i get 
    cv2.imshow("Human Detection &motion Tracking", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()