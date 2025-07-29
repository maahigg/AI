import cv2
import numpy as np
from tensorflow.keras.models import load_model
from keras.preprocessing.image import img_to_array

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

emotion_model = load_model('emotion_model.h5')

emotion_labels = ['angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral']

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print('error, could not open camera')
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print('error, failed to capture image')
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors = 5, minSize = (30, 30))