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
arduino = serial.Serial(port='/dev/ttyUSB0', baudrate=115200, timeout=.1)

picam2 = Picamera2()
picam2.configure(picam2.create_preview_configuration(main={"format": 'XRGB8888', "size": (1280, 720)}))
picam2.start()

def write_read(x):
    arduino.write(bytes(str(x), 'utf-8'))
    data = arduino.readline()
    return data

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

index = 0
last_val = 0
max_frames = 8
flagged = (False, 0)
curr_frames = []
total_frames = []
time = []
while(True):
    index += 1
    #print(index)
    #ret, frame = vid.read()
    
    #print(frame)
    #frame = cv2.flip(frame,1)
    im = picam2.capture_array()
    frame = cv2.resize(im, (200, 150), fx=0, fy=0, interpolation = cv2.INTER_CUBIC)
    gray = cv2.cvtColor(frame, code=cv2.COLOR_BGR2GRAY)
    
    faces = detector(gray)
    for face in faces:
        landmarks = predictor(gray, face)
        x = landmarks.part(30).x
        y = landmarks.part(30).y
        if index % max_frames == 0:
            if index == max_frames:
                last_val = stats.mean(total_frames[-1*max_frames:])
            else:
                frames = total_frames[-1*max_frames:]
                #print(stats.mean(frames))
                if (stats.mean(frames)) < last_val-7 and not flagged[0]:
                    print("right")
                    flagged = (True, index)
                    write_read(0)
                    # sleep(2)
                elif stats.mean(frames) > last_val+7 and not flagged[0]:
                    print("left") 
                    flagged = (True, index)
                    write_read(1)
                    # sleep(2)
                last_val = stats.mean(frames)
                if index > flagged[1] + max_frames*2:
                    flagged = (False, 0)
            total_frames = total_frames[-1*max_frames:]

        total_frames.append(x)
        time.append(index)

        cv2.circle(img=frame, center=(x, y), radius=5, color=(0, 255, 0), thickness=-1)
    # show the image
    cv2.imshow(winname="Face", mat=frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

plt.plot(time, total_frames, 'o')
plt.show()
 

cv2.destroyAllWindows()