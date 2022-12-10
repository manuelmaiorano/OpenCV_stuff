import cv2 as cv
import numpy as np
import random


def findtargetPoint(mask):
    conts,_ = cv.findContours(mask, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    if conts: 
        x,y,w,h = cv.boundingRect(conts[0])
        center = x+w/2, y+h/2#(int(x+w/2), int(y+h/2))
        return center
    else: None

class PointFilter:
    def __init__(self, length):
        self.prev_points = np.zeros((length, 2))
        self.length = self.prev_points.shape[0]
        self.index = 0

    def __call__(self, new_point):
        self.prev_points[self.index, :] = new_point
        self.index += 1
        self.index %= self.length

        return self.filter().astype(int)

    def filter(self):
        return np.sum(self.prev_points, axis=0)/self.length

def app():
    lower_green, upper_green = np.array([50,100,100]),  np.array([70,255,255])

    kernel = np.ones((5,5), np.uint8)
    pfilter = PointFilter(15)

    cap = cv.VideoCapture(0)
    CAM_FRAME_SHAPE = (480, 640, 3)
    target = np.zeros(CAM_FRAME_SHAPE, np.uint8)


    while cap.isOpened():
        _, frame = cap.read()

        hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
        mask = cv.inRange(hsv, lower_green, upper_green)
        filtered_mask = cv.erode(mask, kernel, iterations=1)

        
        point = findtargetPoint(filtered_mask)
        if point: 
            point = pfilter(point)
            mirrored_point = CAM_FRAME_SHAPE[1] - point[0], point[1]
            cv.circle(target, mirrored_point, 5, (0,0,255), -1)
        
        
        cv.imshow('mask', target)

        k = cv.waitKey(30) & 0xFF
        if k == 27: break
        elif k == ord('d'): target.fill(0)


    cv.destroyAllWindows()

if __name__ == '__main__':
    app()