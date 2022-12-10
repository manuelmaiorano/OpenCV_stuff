import os
import cv2 as cv

class SlideShow:
    def __init__(self, path):
        self.images = []
        for file in os.listdir(path):
            im = cv.imread(os.path.join(path, file))
            self.images.append(im)

        self.currentIndex = 0
        self.currentImg = self.images[self.currentIndex]
        self.transition = False
        self.alphaCounter = 0

        self.framerate = 30
        self.timeout = self.framerate * 5

    def run(self):
        if not self.transition:
            self.timeout -= 1
            if self.timeout < 0:
                self.transition = True
                self.timeout = self.framerate * 5
        else:
            im1 = self.images[self.currentIndex]
            im2 = self.images[self.nextIndex()]
            

            alpha = self.alphaCounter/100

            self.currentImg = cv.addWeighted(im1, 1-alpha, im2, alpha, 0)

            self.alphaCounter += 1
            if self.alphaCounter > 100: 
                self.alphaCounter = 0
                self.currentIndex = self.nextIndex()
                self.transition = False

    def nextIndex(self):
        if self.currentIndex < len(self.images) - 1:
            return self.currentIndex + 1
        else: return 0


if __name__ == '__main__':

    sl = SlideShow('./img')
    cv.namedWindow('slideshow')

    while True:
        cv.imshow('slideshow', sl.currentImg)
        k = cv.waitKey(30)
        if k == ord('q'): break
        sl.run()

    cv.destroyAllWindows()