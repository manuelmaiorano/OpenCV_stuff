import cv2 as cv

lower, upper = 100, 200

img = cv.imread('./img/wmn.jpeg')
edges = cv.Canny(img, lower, upper)

def set_th(val, up = False):#true if up false if low
    global lower, upper, edges
    if up : upper = val
    else: lower = val
    edges = cv.Canny(img, lower, upper)


cv.namedWindow('edges')


cv.createTrackbar('upper','edges',upper,255, lambda x : set_th(x, up = True))
cv.createTrackbar('lower','edges',lower,255, lambda x : set_th(x))

cv.imshow('img', img)

while True:
    cv.imshow('edges', edges)
    k = cv.waitKey(30) & 0xFF
    if k == ord('q'):
        break


cv.destroyAllWindows()