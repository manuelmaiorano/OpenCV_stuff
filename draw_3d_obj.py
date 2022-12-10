import cv2 as cv
import numpy as np
from utils import *

def draw(img, corners, imgpts):
    corner = np.int32(corners[0].ravel())
    imgpts = np.int32(imgpts)
    cv.line(img, corner, tuple(imgpts[0].ravel()), (255,0,0), 5)
    cv.line(img, corner, tuple(imgpts[1].ravel()), (0,255,0), 5)
    cv.line(img, corner, tuple(imgpts[2].ravel()), (0,0,255), 5)

class CameraCalibration:
    def __init__(self):
        cv.namedWindow('calibration')

        self.capture = getCameraCapture()

        self.objp = np.zeros((6*8,3), np.float32)
        self.objp[:,:2] = np.mgrid[0:8,0:6].T.reshape(-1,2)

        self.objpoints = []
        self.imgpoints = []

        self.isCalDone = False

    def calibrate(self):
        h,  w = self.newFrame.shape[:2]

        ret, self.mtx, self.dist, rvecs, tvecs = cv.calibrateCamera(self.objpoints, self.imgpoints, 
                                                            (w, h), None, None)

        self.newcameramtx, self.roi = cv.getOptimalNewCameraMatrix(self.mtx, self.dist, (w,h), 1, (w,h))

        np.savez('.\cal\B.npz', mtx = self.mtx, dist = self.dist, rvecs = rvecs, tvecs = tvecs)
        self.isCalDone = True

    def handleKey(self, key):
        if not self.isCalDone:
            if key == ord('c'):
                gray = cv.cvtColor(self.newFrame, cv.COLOR_BGR2GRAY)
                # Find the chess board corners
                ret, corners = cv.findChessboardCorners(gray, (8,6), None)
                # If found, add object points, image points (after refining them)
                if ret == True:
                    print('found pattern')
                    self.objpoints.append(self.objp)
                    self.imgpoints.append(corners)
                else: print('not found')

            elif key == ord('d'):
                self.calibrate()

    def run(self):
        while True:
            ret, self.newFrame = self.capture.read()
            if not ret: break

            if self.isCalDone:
                # undistort
                dst = cv.undistort(self.newFrame, self.mtx, self.dist, None, self.newcameramtx)
                # crop the image
                x, y, w, h = self.roi
                dst = dst[y:y+h, x:x+w]

                cv.imshow('calibration', dst)
            else:
                cv.imshow('calibration', self.newFrame)

            k = cv.waitKey(30) & 0xFF
            if k == 27: break
            else: self.handleKey(k)

        cv.destroyAllWindows()

class CameraDraw3D:
    def __init__(self):
        cv.namedWindow('draw3d')

        self.capture = getCameraCapture()

        self.criteria = cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001

        self.objp = np.zeros((6*8,3), np.float32)
        self.objp[:,:2] = np.mgrid[0:8,0:6].T.reshape(-1,2)

        self.axis = np.float32([[3,0,0], [0,3,0], [0,0,-3]]).reshape(-1,3)

        with np.load('.\cal\B.npz') as X:
            self.mtx, self.dist, _, _ = [X[i] for i in ('mtx','dist','rvecs','tvecs')]

    def run(self):
        while True:
            ret, frame = self.capture.read()
            if not ret: break

            gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
            ret1, corners = cv.findChessboardCorners(gray, (8,6),None)

            if ret1 == True:
                corners2 = cv.cornerSubPix(gray,corners,(11,11),(-1,-1), self.criteria)
                # Find the rotation and translation vectors.
                ret,rvecs, tvecs = cv.solvePnP(self.objp, corners2, self.mtx, self.dist)
                # project 3D points to image plane
                imgpts, jac = cv.projectPoints(self.axis, rvecs, tvecs, self.mtx, self.dist)
                draw(frame,corners2,imgpts)

            cv.imshow('draw3d', frame)

            k = cv.waitKey(60) & 0xFF
            if k == 27: break

        cv.destroyAllWindows()

        
        

if __name__ == '__main__':
    CameraDraw3D().run()