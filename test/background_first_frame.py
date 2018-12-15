from __future__ import print_function
import cv2 as cv

capture = cv.VideoCapture(0)
ret, frame_first = capture.read()
ret, frame_first = capture.read()
ret, frame_first = capture.read()
ret, frame_first = capture.read()
ret, frame_first = capture.read()
frame_first_gray = cv.cvtColor(frame_first, cv.COLOR_BGR2GRAY)
frame_first_blurred = cv.GaussianBlur(frame_first_gray, (5, 5), 0)

while True:
    start = cv.getTickCount()
    _, frame = capture.read()

    if frame is None:
        break

    frame_gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    frame_blurred = cv.GaussianBlur(frame_gray, (5, 5), 0)
    # frame_canny = cv.Canny(frame_blurred, 50, 150)

    difference = cv.absdiff(frame_first_blurred, frame_blurred)
    _, difference = cv.threshold(difference, 25, 255, cv.THRESH_BINARY)
    difference_blurred = cv.GaussianBlur(difference, (5, 5), 0)

    cv.imshow('BG Filtered', difference_blurred)

    keyboard = cv.waitKey(30)
    if keyboard == 'q' or keyboard == 27:
        break

    key = cv.waitKey(1)
    if key == 27:
        break

capture.release()
cv.destroyAllWindows()
