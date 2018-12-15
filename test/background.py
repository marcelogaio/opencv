from __future__ import print_function
import cv2 as cv

capture = cv.VideoCapture(0)
algo = 'MOG2' ''' MOG2 or KNN '''

if algo == 'MOG2':
    backSub = cv.createBackgroundSubtractorMOG2()
else:
    backSub = cv.createBackgroundSubtractorKNN()


def preProcess(frame):
    # Convert image to grayscale
    frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    # Cleanup image using gaussian blur
    frame = cv.GaussianBlur(frame, (5, 5), 0)
    return frame


def showWindow(title, frame, x, y):
    fps = round(cv.getTickFrequency() / (cv.getTickCount() - start))
    cv.namedWindow(title, cv.WINDOW_NORMAL)
    cv.resizeWindow(title, 800, 500)
    cv.putText(frame, str(fps), (0, 30), cv.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255))
    cv.imshow(title, frame)
    cv.moveWindow(title, x, y)


while True:
    start = cv.getTickCount()
    _, frame = capture.read()
    if frame is not None:
        frame = preProcess(frame)

        frame_gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        frame_blurred = cv.GaussianBlur(frame_gray, (5, 5), 0)
        frame_canny = cv.Canny(frame_blurred, 50, 150)

        fgMask = backSub.apply(frame)

        cv.rectangle(frame, (10, 2), (100, 20), (255, 255, 255), -1)
        cv.putText(frame, str(capture.get(cv.CAP_PROP_POS_FRAMES)), (15, 15),cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0))

        showWindow("Canny", frame_canny, 20, 20)
        showWindow("FG Mask", fgMask, 820, 20)

    key = cv.waitKey(1)
    if key == 27:
        break

capture.release()
cv.destroyAllWindows()
