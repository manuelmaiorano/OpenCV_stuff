import cv2 as cv
import numpy as np
from utils import *

class App():
    def __init__(self):
        cv.namedWindow('img')
        cv.setMouseCallback('img', RectangleDrawingCallback(self.update))

        self.capture = cv.VideoCapture(0)
        if not self.capture.isOpened(): 
            print('cannot open camera')
            exit()
        
        _,self.initialFrame = self.capture.read()
        self.imgtoshow = self.initialFrame
        self.isTracking = False

        self.track_window = None

        self.term_crit = ( cv.TERM_CRITERIA_EPS | cv.TERM_CRITERIA_COUNT, 10, 1 )

    def update(self, topleft, bottomright):
        if not self.isTracking:
            x, y = topleft
            w, h = (bottomright[i] - topleft[i] for i in (0,1))

            self.track_window = x, y, w, h

            img = np.copy(self.initialFrame)
            cv.rectangle(img, topleft, bottomright, (255, 0, 0), 3)
            self.imgtoshow = img

    def getHist(self):
        x, y, w, h = self.track_window
        roi = self.initialFrame[y:y+h, x:x+w]
        hsv_roi =  cv.cvtColor(roi, cv.COLOR_BGR2HSV)

        mask = cv.inRange(hsv_roi, np.array((0., 60.,32.)), np.array((180.,255.,255.)))
        self.roi_hist = cv.calcHist([hsv_roi],[0],mask,[180],[0,180])
        cv.normalize(self.roi_hist,self.roi_hist,0,255,cv.NORM_MINMAX)

    def track(self, frame):
        hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
        dst = cv.calcBackProject([hsv],[0],self.roi_hist,[0,180],1)
        # apply camshift to get the new location
        ret, self.track_window = cv.CamShift(dst, self.track_window, self.term_crit)
        # Draw it on image
        pts = cv.boxPoints(ret)
        pts = np.int0(pts)
        self.imgtoshow = cv.polylines(frame,[pts],True, 255,2)

    def run(self):
        
        while True:
            if self.isTracking:
                ret, newFrame = self.capture.read()
                if not ret: break

                self.track(newFrame)
                
            cv.imshow('img', self.imgtoshow)

            k = cv.waitKey(30) & 0xFF
            if k == 27: break
            elif k == ord('d'): 
                self.getHist()
                self.isTracking = True

        cv.destroyAllWindows()


if __name__ == '__main__':
    App().run()