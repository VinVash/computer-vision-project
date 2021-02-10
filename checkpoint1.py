#must press escape[esc] to exit loop

import cv2 
import numpy as np

#trackbar callback function
def nothing(x):
    pass

#making window
cv2.namedWindow('Image')

#enter image to be tested
img = cv2.imread('CHECKPOINT1.png') 

#resizing image to fit screen; change 1 to 0.5 to view orignal picture masked
img = cv2.resize(img , (0,0), fx=0.5 , fy=0.5)


#making background image of same size as test image
bg = np.zeros([img.shape[0],img.shape[1],img.shape[2]],dtype=np.uint8)

#making mask
mask = img
mask = cv2.cvtColor(mask , cv2.COLOR_BGR2GRAY)
mask = cv2.GaussianBlur(mask, (5, 5), 0)
retVal ,mask = cv2.threshold(mask ,240,255, cv2.THRESH_BINARY_INV)
mask_inverse = cv2.bitwise_not(mask)

#making trackbar
cv2.createTrackbar('R','Image',0,255,nothing)
cv2.createTrackbar('G','Image',0,255,nothing)
cv2.createTrackbar('B','Image',0,255,nothing)

while True:
    #logic
    fg = cv2.bitwise_and(img, img, mask=mask)
    bg = cv2.bitwise_and(bg, bg, mask=mask_inverse)
    final = cv2.bitwise_or(fg, bg)
    cv2.imshow('Image',final)
    
    #to exit loop press esc
    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break

    #updating background
    r = cv2.getTrackbarPos('R','Image')
    g = cv2.getTrackbarPos('G','Image')
    b = cv2.getTrackbarPos('B','Image')
    bg[:] = [b,g,r]

#destroy all window   
cv2.destroyAllWindows()