"""
goal: create a program that takes input into video
based on the video there is a dial
the dial can be used top control the volume or other stuff

- find the dial
- read the video
- find the contour
- find the red color range
- find red color only
- show the red only segmentation
"""

import cv2

vc = cv2.VideoCapture(2)

while True:
	ret, frame = vc.read()
	if not ret:
		break

	cv2.imshow('frame', frame)
	if ord('q')==cv2.waitKey(1):
		break

vc.release()
cv2.destroyAllWindows()