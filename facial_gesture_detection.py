# import the opencv library
import cv2
import dlib
import numpy as np
import faceBlendCommon as face
import matplotlib.pyplot as plt

from picamera2 import Picamera2, Preview

def checkGesture(frames):
    if frames[-1] - frames[0] > 40:
        print('left')
    elif frames[-1] - frames[0] < -40:
        print("right")
     
     

picam2 = Picamera2()
picam2.configure(picam2.create_preview_configuration(main={"format": 'XRGB8888', "size": (640, 480)}))
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
    frame = cv2.resize(im, (200, 200), fx=0, fy=0, interpolation = cv2.INTER_CUBIC)
    gray = cv2.cvtColor(frame, code=cv2.COLOR_BGR2GRAY)
    
    faces = detector(gray)
    for face in faces:
        landmarks = predictor(gray, face)
        x = landmarks.part(30).x
        y = landmarks.part(30).y

        if len(curr_frames) > max_frames:
            curr_frames.pop(0)
            curr_frames.append(x)
            #checkGesture(curr_frames)
            
        else:
            curr_frames.append(x)
        
        total_frames.append(x)
        time.append(index)

        cv2.circle(img=frame, center=(x, y), radius=5, color=(0, 255, 0), thickness=-1)
    # show the image
    cv2.imshow(winname="Face", mat=frame)
    if index == 150:
        break

plt.plot(time, total_frames, 'o')
plt.show()
 
vid.release()

cv2.destroyAllWindows()