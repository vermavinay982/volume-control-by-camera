import cv2
import imutils

# lower = (165, 126, 211)
# upper = (185, 146, 291)

# 152 181 151

# grab the current frame
frame = cv2.imread('dial.jpg')
# handle the frame from VideoCapture or VideoStream

frame_lab = cv2.cvtColor(frame,cv2.COLOR_BGR2LAB)
frame_hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)

# ROIs = cv2.selectROIs('Select ROIs',frame, False)
# frame = frame[ROIs[0][1]:ROIs[0][1]+ROIs[0][3], ROIs[0][0]:ROIs[0][0]+ROIs[0][2]]

# resize the frame, blur it, and convert it to the HSV
# color space
# print(ROI_1)
# cv2.imshow('frae',frame)
# cv2.imshow('roi',ROI_1)


import numpy as np

# color = (10,181,151)

# hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

lower_lab = (10,181,151)
upper_lab = (152,181,151)
# print(frame.mean())

lower_bgr = cv2.cvtColor( np.uint8([[lower_lab]] ), cv2.COLOR_LAB2BGR)[0][0]
lower_hsv = cv2.cvtColor( np.uint8([[lower_bgr]] ), cv2.COLOR_BGR2HSV)[0][0]

upper_bgr = cv2.cvtColor( np.uint8([[upper_lab]] ), cv2.COLOR_LAB2BGR)[0][0]
upper_hsv = cv2.cvtColor( np.uint8([[upper_bgr]] ), cv2.COLOR_BGR2HSV)[0][0]

print(lower_hsv, upper_hsv)
# img = np.full((100,100,3),color, dtype=np.uint8)
# img = cv2.cvtColor(img, cv2.COLOR_LAB2BGR)
# print(img)
# cv2.imshow('np',img)

mask = cv2.inRange(frame_hsv, lower_hsv, upper_hsv)
mask = cv2.erode(mask, None, iterations=2)
mask = cv2.dilate(mask, None, iterations=2)
cv2.imshow('mask', mask)
cv2.imshow('hsv', frame_hsv)



# 152 181 151

cv2.waitKey(0)