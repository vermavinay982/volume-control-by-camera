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

backlog
- color spaces - hsv
"""

import cv2
import imutils
import pyautogui as p

vc = cv2.VideoCapture(2)

def gray2hsv(img):
	img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
	img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

	return img


def find_circle(frame, low, high):
	h_d = 10
	s_d = 140
	v_d = 100

	# lower = (pixel_value[0]-h_d, pixel_value[1]-s_d, pixel_value[2]-v_d)
	# upper = (pixel_value[0]+h_d, pixel_value[1]+s_d, pixel_value[2]+v_d)


	# grab the current frame

	# resize the frame, blur it, and convert it to the HSV
	# color space
	frame = imutils.resize(frame, width=600)
	blurred = cv2.GaussianBlur(frame, (11, 11), 0)
	hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
	# construct a mask for the color "green", then perform
	# a series of dilations and erosions to remove any small
	# blobs left in the mask
	mask = cv2.inRange(hsv, low, high)
	mask = cv2.erode(mask, None, iterations=2)
	mask = cv2.dilate(mask, None, iterations=2)
	cv2.imshow('mask', mask)


	d_mask = gray2hsv(mask)

	mult = d_mask*frame
	cv2.imshow('mult', mult)
	
	# find contours in the mask and initialize the current
	# (x, y) center of the ball
	cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)
	cnts = imutils.grab_contours(cnts)
	center = None
	# only proceed if at least one contour was found
	if len(cnts) > 0:
		# find the largest contour in the mask, then use
		# it to compute the minimum enclosing circle and
		# centroid
		c = max(cnts, key=cv2.contourArea)
		((x, y), radius) = cv2.minEnclosingCircle(c)
		M = cv2.moments(c)
		center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
		# only proceed if the radius meets a minimum size
		if radius > 2:
			# draw the circle and centroid on the frame,
			# then update the list of tracked points
			cv2.circle(frame, (int(x), int(y)), int(radius),
				(0, 255, 255), 2)
			# cv2.circle(frame, center, 5, (0, 0, 255), -1)
	# update the points queue
	return center

count = 0
prev = 0
curr = 0
level = 0
mute = False

while True:
	ret, frame = vc.read()

	if not ret:
		break
	h,w,c = frame.shape

	lower_red = (164,79,100)
	upper_red = (227,255,255)


	# cv2.circle(frame, center, 5, (0, 0, 255), -1)

	center1 = find_circle(frame, lower_red, upper_red)
	# center2 = find_circle(frame, lower_black, upper_black)
	# center = find_circle(frame, lower_white, upper_white)
	if not center1 is None:
		cv2.circle(frame, center1, 5, (0, 0, 255), -1)
		# cv2.circle(frame, center2, 5, (0, 255,0), -1)
		y = center1[1]
		y_norm = y/h
		level = int(y_norm*10)

		if mute==True:
			p.press('volumemute')
			mute = False
		# print(level)
	else:
		# pause the music
		# p.press('volumedown', presses=5)
		
		if mute==False:
			print('paused')
			print('Mute Volume')
			p.press('volumemute')
			mute = True

		# if mute%2:
		# 	p.press('volumemute')
		# 	mute = 1
		# else:
		# 	pass

	curr = level
	if not prev == curr:
		diff = (prev-curr)*5
		print('Change the volume', diff)
		if diff<0:
			print('Reduce Volume')
			p.press('volumedown', presses=(diff*(-1)))
		else:
			print('Increase Volume')
			p.press('volumeup', presses=diff)

	prev = curr

	cv2.imshow('frame', frame)
	if ord('q')==cv2.waitKey(1):
		break

vc.release()
cv2.destroyAllWindows()