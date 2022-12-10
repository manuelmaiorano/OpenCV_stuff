import cv2 as cv

def getCameraCapture():
    capture = cv.VideoCapture(0)
    if not capture.isOpened(): 
        print('cannot open camera')
        exit()

    return capture

"""
To be called on opencv mouse event(set as callback on cv.setMouseCallback).
Wraps a user specified callback to which passes the rectangle currently drawn.
"""
class RectangleDrawingCallback:
    def __init__(self, action):
        self.drawing = False
        self.initialPos, self.finalPos = None, None
        self.action = action

    def __call__(self, event,x,y,flags,param):
        if event == cv.EVENT_LBUTTONDOWN:
            self.drawing = True
            self.initialPos = x,y

        elif event == cv.EVENT_MOUSEMOVE:
            if self.drawing == True: 
                self.finalPos = x,y

        elif event == cv.EVENT_LBUTTONUP:
            self.drawing = False

        if self.initialPos and self.finalPos: 
            self.action(self.initialPos, self.finalPos)