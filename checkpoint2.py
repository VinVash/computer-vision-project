import cv2 
import numpy

#drawLines function
def drawLines(c):
    for i in range(len(c)):
        if i < len(c)-1:
            j = i+1
        elif i == len(c)-1:
            j = 0
        cv2.line(img,(c[i][0],c[i][1]),(c[j][0],c[j][1]),(255,0,0),4)

#input image
img = cv2.imread('checkpoint2.png')

#performing operation to get binary image and contours
height, width, channel = img.shape
img = cv2.resize(img , (0,0), fx=1 , fy=1)
imgc = img
imgc = cv2.cvtColor(imgc , cv2.COLOR_BGR2GRAY)
imgc = cv2.GaussianBlur(imgc, (5, 5), 0)
retVal ,imgc = cv2.threshold(imgc ,240,255, cv2.THRESH_BINARY_INV)
contours, hierarchy = cv2.findContours(imgc, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

#defining variable used
max_area=0
max_c = None
green_points = []


for c in contours:
    #filtering green circles
    M = cv2.moments(c)
    cx = int(M['m10'] / M['m00'])
    cy = int(M['m01'] / M['m00'])
    color = img[cy,cx]
    if color[1]>=140 and color[0]<127 and color[2]<127:
        green_points.append([cx,cy])
        #print(green_points)
    
    #finding largest circle
    area = cv2.contourArea(c)
    if max_area <= area:
        max_area = area
        max_c = c
    else:
        pass
    
#drawing lines on green circles
drawLines(green_points)

#marking biggest circle
M = cv2.moments(max_c)
cx = int(M['m10'] / M['m00'])
cy = int(M['m01'] / M['m00'])
color = img[cy,cx]
text = 'Largest Circle'
cv2.putText(img, text, (cx -50, cy),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)   
cv2.drawContours(img, [max_c], -1, (0, 0, 0), 2)

#displaying image
cv2.imshow("Image", img)
cv2.waitKey(0)
cv2.destroyAllWindows()