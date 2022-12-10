import cv2 as cv


class PaintBrush:
    def __init__(self, img):
        self.img = img
        self.drawing = False
        self.color = [0,0,0]
        self.size = 0

    def set_r(self, val): self.color[2] = val

    def set_g(self, val): self.color[1] = val

    def set_b(self, val): self.color[0] = val

    def set_size(self, val): self.size = val

    def draw_circle(self, event,x,y,flags,param):

        if event == cv.EVENT_LBUTTONDOWN:
            self.drawing = True

        elif event == cv.EVENT_MOUSEMOVE:
            if self.drawing == True:
                cv.circle(self.img, (x,y), self.size, self.color,-1)

        elif event == cv.EVENT_LBUTTONUP:
            self.drawing = False

if __name__ == '__main__':
    import numpy as np

    img = np.zeros((300,512,3), np.uint8)
    brush = PaintBrush(img)

    cv.namedWindow('image')
    cv.setMouseCallback('image', brush.draw_circle)
    
    while True:
        cv.imshow('image',img)
        k = cv.waitKey(10) & 0xFF
        if k == ord('q'):
            break

    cv.destroyAllWindows()

