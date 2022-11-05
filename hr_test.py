# import the opencv library
import cv2
import dlib
import os
import imutils
import numpy as np
import faceBlendCommon as face
from scipy.signal import butter, lfilter
import matplotlib.pyplot as plt
from scipy import signal 

  
def butter_bandpass(lowcut, highcut, fs, order=5):
	nyq = 0.5 * fs
	low = lowcut / nyq
	high = highcut / nyq
	b, a = butter(order, [low, high], btype='band')
	return b, a


def butter_bandpass_filter(data, lowcut, highcut, fs, order=5):
	b, a = butter_bandpass(lowcut, highcut, fs, order=order)
	y = lfilter(b, a, data)
	return y
  
# define a video capture object
vid = cv2.VideoCapture(0)

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
color_blue = (239,207,137)
color_cyan = (255,200,0)
color_black = (0, 0, 0)
averages = [0]
fs = 30
lowcut = 0.5
highcut = 5
index = 0
while(True):
	index += 1
	# Capture the video frame
	# by frame
	ret, frame = vid.read()
	# im = frame
	# landmarks = face.getLandmarks(detector, predictor, im)
	# for i in range(17,27):
	# 	points = landmarks[i]
	# 	new_points = (points[0], points[1]-80)
	# 	landmarks[i] = new_points
	# # Create a mask for the lips
	# lipsPoints = landmarks[0:27]
	# mask = np.zeros((im.shape[0], im.shape[1], 3), dtype=np.float32)
	# cv2.fillConvexPoly(mask, np.int32(lipsPoints), (1.0, 1.0, 1.0))
	# mask = 255*np.uint8(mask)
	# # Apply close operation to improve mask
	# kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (40,40))
	# mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel, 1)
	# # Blur the mask to obtain natural result
	# mask = cv2.GaussianBlur(mask,(15,15),cv2.BORDER_DEFAULT)
	# # Calculate inverse mask
	# inverseMask = cv2.bitwise_not(mask)
	# # Convert masks to float to perform blending
	# mask = mask.astype(float)/255
	# inverseMask = inverseMask.astype(float)/255
	# # Apply color mapping for the lips
	# lips = cv2.applyColorMap(im, cv2.COLORMAP_INFERNO)
	# # Convert lips and face to 0-1 range
	# lips = lips.astype(float)/255
	# ladyFace = im.astype(float)/255
	# # Multiply lips and face by the masks
	# justLips = cv2.multiply(mask, lips)
	# justFace = cv2.multiply(mask, ladyFace)
	# # Add face and lips
	# result = justFace + justLips
	# # Show result
	# cv2.imshow("", justFace)

	# average = np.mean(justFace)
	# print(average)
	# if len(averages) > 10:
	# 	averages.pop(0)
	# 	averages.append(average)
	# 	y = butter_bandpass_filter(averages, lowcut, highcut, fs, order=6)
	# 	f, Pxx_den = signal.welch(y, fs)
	# 	max_index = 0
	# 	max_val = 0
	# 	for i in range(len(Pxx_den)):
	# 		if Pxx_den[i] > max_val:
	# 			max_val = Pxx_den[i]
	# 			max_index = i
	# 	print(y[i])

	# else:
	# 	averages.append(average)
		


	# # Display the resulting frame
	# cv2.imshow('frame', frame)

	gray = cv2.cvtColor(src=frame, code=cv2.COLOR_BGR2GRAY)
	faces = detector(gray)
	for face in faces:
		x1 = face.left() # left point
		y1 = face.top() # top point
		x2 = face.right() # right point
		y2 = face.bottom() # bottom point
		# Draw a rectangle
		# Look for the landmarks
		landmarks = predictor(gray, face)
		
		for i in range(30,31):
			x = landmarks.part(i).x
			y = landmarks.part(i).y

			# if i > 17 and i < 26:
			# 	y -= 80

			# Draw a circle
			# print("{} (x,y)->({},{})".format(index, x,y))
			cv2.circle(img=frame, center=(x, y), radius=5, color=(0, 255, 0), thickness=-1)

		cv2.rectangle(img=frame, pt1=(x1, y1), pt2=(x2, y2), color=(0, 255, 0), thickness=4)

	# show the image
	cv2.imshow(winname="Face", mat=frame)
		
	# the 'q' button is set as the
	# quitting button you may use any
	# desired button of your choice
	if cv2.waitKey(1) & 0xFF == ord('q'):
			break
  
# After the loop release the cap object
vid.release()
# Destroy all the windows
cv2.destroyAllWindows()