import cv2 
import numpy


img = cv2.imread('c3.png')

height, width, channel = img.shape
img = cv2.resize(img , (0,0), fx=1 , fy=1)

imgc = img

imgc = cv2.cvtColor(imgc , cv2.COLOR_BGR2GRAY)
imgc = cv2.GaussianBlur(imgc, (5, 5), 0)
retVal ,imgc = cv2.threshold(imgc ,240,255, cv2.THRESH_BINARY_INV)

contours, hierarchy = cv2.findContours(imgc, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

for c in contours:
	M = cv2.moments(c)
	cx = int(M['m10'] / M['m00'])
	cy = int(M['m01'] / M['m00'])
	color = img[cy,cx]
	text = '('+str(color[2])+','+str(color[1])+','+str(color[0])+')'
	cv2.putText(img, text, (cx - 45, cy - 15),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
	print('The RGB Value is: (',color[2],',',color[1],',',color[0],')')
	cv2.drawContours(img, [c], -1, (0, 0, 0), 2)
	cv2.imshow("Image", img)
	cv2.waitKey(0)
cv2.destroyAllWindows()