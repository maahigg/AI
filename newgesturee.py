import cv2
import numpy as np
import mediapipe as mp

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print('error, cannot open video cam')
    exit()

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands = 1, min_detection_confidence = 0.7)
mp_draw = mp.solutions.drawing_utils

while True:
    ret, frame = cap.read()
    if not ret:
        print('error: failed to capture image')
        break

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result=hands.process(rgb)

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_skin = np.array([0, 48, 80], dtype=np.uint8)
    upper_skin = np.array([20, 255, 255], dtype=np.uint8)
    mask = cv2.inRange(hsv, lower_skin, upper_skin)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11, 11))
    mask = cv2.erode(mask, kernel, iterations=2)
    mask = cv2.dilate(mask, kernel, iterations=2)
    mask = cv2.GaussianBlur(mask, (3, 3), 0)
    result_skin = cv2.bitwise_and(frame, frame, mask=mask)

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            landmarks = hand_landmarks.landmark
            fingers=[]

            fingers.append(landmarks[4].x < landmarks[3].x)

            for tip_id in [8, 12, 16, 20]:
                fingers.append(landmarks[tip_id].y < landmarks[tip_id -2].y)
            
            total_fingers = fingers.count(True)

            cv2.putText(frame, f"fingers up: {total_fingers}", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
            if total_fingers == 1:
                h, w, _ = frame.shape
                cv2.rectangle(frame, (w//2 - 50, h//2 - 50), (w//2+50, h//2+50), (0, 255, 0), 2)

    cv2.imshow('original frame', frame)
    cv2.imshow('skin filtered frame', result_skin)
           
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()