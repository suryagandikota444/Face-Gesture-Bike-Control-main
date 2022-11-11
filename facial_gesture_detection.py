# import the opencv library
import cv2
import dlib
import numpy as np
import faceBlendCommon as face
import matplotlib.pyplot as plt
import statistics as stats

from picamera2 import Picamera2, Preview

def checkGesture(frames):
    print(stats.mean(frames))
     
     

picam2 = Picamera2()
picam2.configure(picam2.create_preview_configuration(main={"format": 'XRGB8888', "size": (1280, 720)}))
picam2.start()

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

index = 0
max_frames = 20
curr_frames = []
total_frames = []
time = []
while(True):
    index += 1
    print(index)
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
        
        if index % 20 == 0:
            checkGesture(total_frames[-20:]) 

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