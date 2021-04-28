# For more info: http://docs.opencv.org/3.0-beta/doc/py_tutorials/py_gui/py_video_display/py_video_display.html
import cv2 as cv2
import cv2 as cv
import numpy as np
import os
import time
import subprocess

import imagezmq

sender = imagezmq.ImageSender(connect_to='tcp://localhost:5555')

index_maximum = 512
index = 0

flag_is_record=False

ROOT_DIR='/opt/records'

FILE_OUTPUT_FORMAT = os.path.join(ROOT_DIR, 'output_%s.mp4')
# Checks and deletes the output file
# You cant have a existing file or it will through an error
print(FILE_OUTPUT_FORMAT % str(index).zfill(3) )
for i in range(index_maximum):
	if os.path.isfile( FILE_OUTPUT_FORMAT % str(i).zfill(3) ):
		os.remove(FILE_OUTPUT_FORMAT % str(i).zfill(3))
    

# Playing video from file:
# cap = cv2.VideoCapture('vtest.avi')
# Capturing video from webcam:
cap = cv2.VideoCapture(0)

currentFrame = 0


width_default=640
height_default=480
width = cap.set(cv2.CAP_PROP_FRAME_WIDTH, width_default)
height  = cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height_default)

if not isinstance(type(width), int):
    width = width_default
if not isinstance(type(height), int):
    height = height_default
print(width, height)
#width = cap.get(cv2.CAP_PROP_FRAME_WIDTH) # float
#height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT) # float


# Get current width of frame
# width = cap.get(cv2.CV_CAP_PROP_FRAME_WIDTH)   # float
# Get current height of frame
# height = cap.get(cv2.CV_CAP_PROP_FRAME_HEIGHT) # float

# Define the codec and create VideoWriter object
# fourcc = cv2.CV_FOURCC(*'X264')

#fourcc = cv2.VideoWriter_fourcc(*'XVID')
fourcc = cv2.VideoWriter_fourcc(*'MP4V')

size_maximum='60G'
t_interval_video=60
t_video=t_start=t_curr=time.time()

fname = FILE_OUTPUT_FORMAT % str(index).zfill(3)

if flag_is_record:
	out = cv2.VideoWriter(fname, fourcc, 20.0, (int(width),int(height)))
# while(True):
while(cap.isOpened()):
	# Capture frame-by-frame
	ret, frame = cap.read()

	if ret == True:
		# Handles the mirroring of the current frame
		#frame = cv2.flip(frame,1)
		"""
		if t_curr-t_video>10:
			with subprocess.Popen(["du", "-sh"], stdout=subprocess.PIPE, bufsize=1, universal_newlines=True) as p:
				for line in p.stdout:
					print(line, end='')

			t_video=time.time()
		"""
		if t_curr-t_video>=t_interval_video and flag_is_record:
			out.release()			
			print(f'save "{fname}"')
			t_video = t_curr
			index= (index+1)%index_maximum
			fname = FILE_OUTPUT_FORMAT % str(index).zfill(3)
			out = cv2.VideoWriter(fname,fourcc, 20.0, (int(width),int(height)))
			print(f'start "{fname}"')			

		# Saves for video
		if flag_is_record:
			out.write(frame)


		sender.send_image("c525", frame)

		# Display the resulting frame
		cv2.imshow('frame',frame)



	else:
		break

	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

	# To stop duplicate images
	currentFrame += 1

	t_curr=time.time()

# When everything done, release the capture
cap.release()
if flag_is_record:
	out.release()
cv2.destroyAllWindows()