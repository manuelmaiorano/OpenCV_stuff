import cv2 as cv
import numpy as np

lower_blue, upper_blue = np.array([110,50,100]),  np.array([130,255,255])
lower_red, upper_red = np.array([0,100,100]),  np.array([10,255,255])
lower_green, upper_green = np.array([50,100,100]),  np.array([70,255,255])



cap = cv.VideoCapture(0)

while cap.isOpened():
    _, frame = cap.read()

    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

    bluemask = cv.inRange(hsv, lower_blue, upper_blue)
    redmask = cv.inRange(hsv, lower_red, upper_red)
    greenmask =  cv.inRange(hsv, lower_green, upper_green)

    mask = cv.bitwise_or(bluemask, greenmask)
    #mask1 = cv.bitwise_or(mask, redmask)

    res = cv.bitwise_and(frame, frame, mask = greenmask)

    cv.imshow('frame', frame)
    cv.imshow('result', res)

    k = cv.waitKey(30) & 0xFF
    if k == 27: break

cv.destroyAllWindows()
print(frame.shape)


