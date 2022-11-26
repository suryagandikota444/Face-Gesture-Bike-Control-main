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

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

index = 0
last_val = 0
max_frames = 8
flagged = (False, 0)
curr_frames = []
total_frames = []
time = []
file = open("indicator.txt", "w")
file.write("None")
file.close()
while(True):
    index += 1
    #print(index)
    #ret, frame = vid.read()
    
    #print(frame)
    #frame = cv2.flip(frame,1)
    im = picam2.capture_array()
    print(im[0][0][:3])