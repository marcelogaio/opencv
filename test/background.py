from __future__ import print_function
import cv2 as cv

capture = cv.VideoCapture(0)
algo = 'MOG2' ''' MOG2 or KNN '''

if algo == 'MOG2':
    backSub = cv.createBackgroundSubtractorMOG2()
else:
    backSub = cv.createBackgroundSubtractorKNN()

while True:
    ret, frame = capture.read()
    frame_gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    frame_blurred = cv.GaussianBlur(frame_gray, (5, 5), 0)
    frame_canny = cv.Canny(frame_blurred, 50, 150)

    if frame is None:
        break
    fgMask = backSub.apply(frame)

    cv.rectangle(frame, (10, 2), (100, 20), (255, 255, 255), -1)
    cv.putText(frame, str(capture.get(cv.CAP_PROP_POS_FRAMES)), (15, 15),
               cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0))

    cv.imshow('Canny', frame_canny)
    cv.imshow('FG Mask', fgMask)

    key = cv.waitKey(1)
    if key == 27:
        break

capture.release()
cv.destroyAllWindows()
