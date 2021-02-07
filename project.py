import cv2 
import numpy

img = cv2.imread('CHECKPOINT1.png')

height, width, channel = img.shape
print(height, width, channel)

img = cv2.resize(img , (0,0), fx=0.5 , fy=0.5)
imgc = img
imgc = cv2.cvtColor(imgc , cv2.COLOR_BGR2GRAY)
retVal ,imgc = cv2.threshold(imgc ,127,255, cv2.THRESH_BINARY_INV)

contours, hierarchy = cv2.findContours(imgc, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE) 
cv2.drawContours(img, contours, -1, (255,0,0), 3)
cv2.imshow("cp1",img)
cv2.waitKey(0)