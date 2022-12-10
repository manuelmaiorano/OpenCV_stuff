import cv2 as cv
import numpy as np
from paintbrush import PaintBrush

class App:
    def __init__(self, image):
        self.image = image

        self.imageShown = np.copy(self.image)
        self.modifiedImg = self.image
        self.mask = np.zeros(self.image.shape[:2], np.uint8)

        self.bgdModel = np.zeros((1,65),np.float64)
        self.fgdModel = np.zeros((1,65),np.float64)

        cv.namedWindow('original')
        cv.namedWindow('modified')
        cv.setMouseCallback('original', self.onMouseAction)

        self.brush = PaintBrush(self.imageShown)
        self.brush.size = 3

        self.mode = 'initial'
        self.drawing = False
        self.rect = None
        self.markBg = False
        
    
    def onMouseAction(self, event,x,y,flags,param):
        if self.mode == 'initial':
            rect = self.getRect(event, (x,y))
            
            if rect: 
                self.rect = rect
                img = np.copy(self.image)
                cv.rectangle(img, *self.rect, (255,0,0), 3)
                self.imageShown = img
        else: 
            self.brush.img = self.imageShown
            self.brush.color = (0,0,0) if self.markBg else (255,255,255)
            self.brush.draw_circle(event, x, y, flags, param)

    def getRect(self, event, pos):
        if event == cv.EVENT_LBUTTONDOWN:
            self.drawing = True
            self.initialPos = pos

        elif event == cv.EVENT_MOUSEMOVE:
            if self.drawing == True: 
                self.finalPos = pos
                return self.initialPos, self.finalPos

        elif event == cv.EVENT_LBUTTONUP:
            self.drawing = False
            return self.initialPos, self.finalPos


        return None

    def processImage(self):
        
        if self.mode == 'initial':
            x,y,w,h = self.rect[0][0], self.rect[0][1], \
                        self.rect[1][0] -self.rect[0][0], self.rect[1][1]-self.rect[0][1]
            cv.grabCut(self.image, self.mask, (x,y,w,h),self.bgdModel,self.fgdModel,5,cv.GC_INIT_WITH_RECT)
            self.mode = 'final'
        else:
            newmask = cv.cvtColor(self.imageShown, cv.COLOR_BGR2GRAY)
            self.mask[newmask == 255] = 1
            self.mask[newmask == 0] = 0

            cv.grabCut(self.image, self.mask, None,self.bgdModel,self.fgdModel,5,cv.GC_INIT_WITH_MASK)

        
        mask2 = np.where((self.mask==2)|(self.mask==0),0,1).astype('uint8')
        self.modifiedImg = self.image*mask2[:,:,np.newaxis]

    def handleKey(self, key):
        if key == 27:
            self.running = False
        elif key == ord('n'):
            self.processImage()
        elif key == ord('1'):
            self.markBg = True
        elif key == ord('2'):
            self.markBg = False

        

    def run(self):
        self.running = True
        while self.running:
            
            cv.imshow('original', self.imageShown)
            cv.imshow('modified', self.modifiedImg)

            k = cv.waitKey(30) & 0xFF
            self.handleKey(k)

        cv.destroyAllWindows()

if __name__ == '__main__':
    image = cv.imread('.\img\\for_grab.jpg')

    App(image).run()