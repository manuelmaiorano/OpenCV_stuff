import numpy as np
import cv2 as cv
from paintbrush import PaintBrush


def blank_image(img):
    img[:] = 0

# Create a black image, a window
img = np.zeros((300,512,3), np.uint8)

brush = PaintBrush(img)

cv.namedWindow('image')
cv.setMouseCallback('image', brush.draw_circle)


# create trackbars for color change
cv.createTrackbar('R','image',0,255, lambda x : brush.set_r(x))
cv.createTrackbar('G','image',0,255, lambda x : brush.set_g(x))
cv.createTrackbar('B','image',0,255, lambda x : brush.set_b(x))

#size
cv.createTrackbar('size','image',0,15, lambda x : brush.set_size(x))


# create switch for ON/OFF functionality
switch = 'cllick to erase'
cv.createTrackbar(switch, 'image',0,1,lambda x : blank_image(img))


while(1):
    cv.imshow('image',img)
    k = cv.waitKey(30)
    if k == 27:
        break


cv.destroyAllWindows()