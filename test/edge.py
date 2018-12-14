import cv2 as cv
#import numpy as np

capture = cv.VideoCapture(0)

scale = 1
delta = 0
ddepth = cv.CV_16S

while True:
    _, frame = capture.read()
    frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    blurred_frame = cv.GaussianBlur(frame, (5, 5), 0)

    # laplacian = cv.Laplacian(blurred_frame, cv.CV_64F)
    canny = cv.Canny(blurred_frame, 100, 250)

    grad_x = cv.Sobel(blurred_frame, ddepth, 1, 0, ksize=3, scale=scale, delta=delta, borderType=cv.BORDER_DEFAULT)
    grad_y = cv.Sobel(blurred_frame, ddepth, 0, 1, ksize=3, scale=scale, delta=delta, borderType=cv.BORDER_DEFAULT)
    abs_grad_x = cv.convertScaleAbs(grad_x)
    abs_grad_y = cv.convertScaleAbs(grad_y)
    sobel = cv.addWeighted(abs_grad_x, 0.5, abs_grad_y, 0.5, 0)

    cv.imshow("Blurred Frame", blurred_frame)
    # cv.imshow("Laplacian", laplacian)
    cv.imshow("Sobel", sobel)
    cv.imshow("Canny", canny)

    key = cv.waitKey(1)
    if key == 27:
        break

capture.release()
cv.destroyAllWindows()
