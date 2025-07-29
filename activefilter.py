<<<<<<< HEAD
import cv2
import numpy as np

cap = cv2.VideoCapture(0)

color_ranges = {
    'r': [([0, 120, 70], [10, 255, 255]), ([170, 120, 70], [180, 255, 255])], 
    'g': ([36, 100, 100], [86, 255, 255]),
    'b': ([94, 80, 2], [126, 255, 255])
}

active_filter=None

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    if active_filter:
        masks=[]
        for lower, upper in color_ranges[active_filter]:
            mask = cv2.inRange(hsv, np.array(lower), np.array(upper))
            masks.append(mask)
        
        combined_mask = cv2.bitwise_or(*masks)
        combined_mask = cv2.GaussianBlur(combined_mask, (7, 7), 0)
        filtered = cv2.bitwise_and(frame, frame, mask=combined_mask)
    else:
        filtered=frame

    cv2.imshow("filtered + edges", filtered)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('r'):
        active_filter = 'r'
    elif key == ord('g'):
        active_filter = 'g'
    elif key == ord('b'):
        active_filter = 'b'
    elif key == ord('c'):
        active_filter = None
    elif key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
=======
import cv2
import numpy as np

cap = cv2.VideoCapture(0)

color_ranges = {
    'r': [([0, 120, 70], [10, 255, 255]), ([170, 120, 70], [180, 255, 255])], 
    'g': ([36, 100, 100], [86, 255, 255]),
    'b': ([94, 80, 2], [126, 255, 255])
}

active_filter=None

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    if active_filter:
        masks=[]
        for lower, upper in color_ranges[active_filter]:
            mask = cv2.inRange(hsv, np.array(lower), np.array(upper))
            masks.append(mask)
        
        combined_mask = cv2.bitwise_or(*masks)
        combined_mask = cv2.GaussianBlur(combined_mask, (7, 7), 0)
        filtered = cv2.bitwise_and(frame, frame, mask=combined_mask)
    else:
        filtered=frame

    cv2.imshow("filtered + edges", filtered)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('r'):
        active_filter = 'r'
    elif key == ord('g'):
        active_filter = 'g'
    elif key == ord('b'):
        active_filter = 'b'
    elif key == ord('c'):
        active_filter = None
    elif key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
>>>>>>> eca3271d26c0c52e2d9da550f5d337e75522f509
