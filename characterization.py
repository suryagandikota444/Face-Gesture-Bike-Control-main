# import the opencv library
import cv2
import dlib
import numpy as np
import faceBlendCommon as face
import matplotlib.pyplot as plt
import statistics as stats
from time import sleep
from picamera2 import Picamera2, Preview
import serial
import time

picam2 = Picamera2()

picam2.configure(picam2.create_preview_configuration(main={"format": 'XRGB8888', "size": (640, 480)}))
picam2.start()

def increase_brightness(frame, value=50):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)

    limit = 255-value
    v[v > limit] = 255
    v[v <= limit] += value

    final = cv2.merge((h, s, v))
    return cv2.cvtColor(final, cv2.COLOR_HSV2BGR)

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

index = 0
last_val = 0
max_frames = 8
flagged = (False, 0)
curr_frames = []
total_frames = []
total_frames_y = []
time = []

while(True):
    index += 1

    im = picam2.capture_array()
    frame = cv2.resize(im, (200, 150), fx=0, fy=0, interpolation = cv2.INTER_CUBIC)
    frame = increase_brightness(frame)
    gray = cv2.cvtColor(frame, code=cv2.COLOR_BGR2GRAY)

    faces = detector(gray)
    for face in faces:
        x1 = face.left() # left point
        y1 = face.top() # top point
        x2 = face.right() # right point
        y2 = face.bottom() # bottom point

        landmarks = predictor(gray, face)
        for i in range(60):

            x = landmarks.part(i).x
            y = landmarks.part(i).y
        # total_frames.append(x)
        # total_frames_y.append(y)
        # time.append(index)

            cv2.circle(img=frame, center=(x, y), radius=5, color=(0, 255, 0), thickness=-1)
    # if index > 300:
    #     plt.plot(time, total_frames)
    #     plt.show()
    #     plt.plot(time, total_frames_y)
    #     plt.show()
    #     break
        cv2.rectangle(img=frame, pt1=(x1, y1), pt2=(x2, y2), color=(0, 255, 0), thickness=4)

    cv2.imshow(winname="Face", mat=frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break