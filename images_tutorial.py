import cv2 as cv
import sys

img = cv.imread('.\img\starry_night.jpg')

if img is None:
    sys.exit('could not find file')

img[:,:,1] = 0
cv.imwrite('.\img\starry_night_not_yl.jpg', img)