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
try:
    arduino = serial.Serial(port='/dev/ttyUSB0', baudrate=115200, timeout=.1)
except:
    arduino = False

picam2 = Picamera2()

picam2.configure(picam2.create_preview_configuration(main={"format": 'XRGB8888', "size": (640, 480)}))
picam2.start()

def write_read(x):
    arduino.write(bytes(str(x), 'utf-8'))
    data = arduino.readline()
    return data

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
total_frames = []
running_avg = []
z_score_threshold = 5
window = 5
flagged = {"flagged": False, "index": 0}
file = open("indicator.txt", "w")
file.write("None")
file.close()

while(True):
    index += 1

    im = picam2.capture_array()
    frame = cv2.resize(im, (200, 150), fx=0, fy=0, interpolation = cv2.INTER_CUBIC)
    frame = increase_brightness(frame)
    gray = cv2.cvtColor(frame, code=cv2.COLOR_BGR2GRAY)

    faces = detector(gray)

    for face in faces:
        landmarks = predictor(gray, face)
        x = landmarks.part(30).x
        y = landmarks.part(30).y
        
        if len(total_frames) < 200:
            total_frames.append(x)
        else:
            total_frames.pop(0)
            total_frames.append(x)

        if index % window == 0:
            avg = stats.mean(total_frames[-1*window:])
            if len(running_avg) < 10:
                running_avg.append(avg)
                print("initializing")
            else:
                total_mean = stats.mean(running_avg[-1*window*5:])
                total_stdev = stats.stdev(running_avg[-1*window*5:])
                z_score = (x-total_mean)/total_stdev
                # print(z_score)
                if z_score > z_score_threshold and not flagged["flagged"]:
                    print("Left")
                    flagged["flagged"] = True
                    flagged["index"] = index
                    file = open("indicator.txt", "w")
                    file.write("Left")
                    file.close()
                    if arduino != False:
                        write_read(1)
                elif z_score < -1*z_score_threshold and not flagged["flagged"]:
                    print("Right")
                    flagged["flagged"] = True
                    flagged["index"] = index
                    file = open("indicator.txt", "w")
                    file.write("Right")
                    file.close()
                    if arduino != False:
                        write_read(0)
                running_avg.append(avg)

                if index > flagged["index"] + 10 and flagged["index"]:
                    print("reset")
                    flagged["flagged"] = False
                    flagged["index"] = index
                    file = open("indicator.txt", "w")
                    file.write("None")
                    file.close()

        cv2.circle(img=frame, center=(x, y), radius=5, color=(0, 255, 0), thickness=-1)

    cv2.imshow(winname="Face", mat=frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break