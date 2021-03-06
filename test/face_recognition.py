import cv2 as cv

scale = 1
delta = 0
ddepth = cv.CV_16S


def preProcess(frame):
    # Convert image to grayscale
    frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    # Cleanup image using gaussian blur
    frame = cv.GaussianBlur(frame, (5, 5), 0)
    return frame


def sketchCanny(frame):
    # Extract Edges
    canny = cv.Canny(frame, 10, 70)
    # Do an invert binarize the image
    ret, frame = cv.threshold(canny, 70, 255, cv.THRESH_BINARY)
    return frame


def showWindow(title, frame, x, y):
    fps = round(cv.getTickFrequency() / (cv.getTickCount() - start))
    cv.namedWindow(title, cv.WINDOW_NORMAL)
    cv.resizeWindow(title, 800, 500)
    cv.putText(frame, str(fps), (0, 30), cv.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255))
    cv.imshow(title, frame)
    cv.moveWindow(title, x, y)


# init video capture
capture = cv.VideoCapture(0)
capture.set(cv.CAP_PROP_FPS, 1)


# loop frames
while True:
    start = cv.getTickCount()
    _, frame = capture.read()
    if frame is not None:
        frame = preProcess(frame)
        showWindow("Frame", frame, 20, 20)
        showWindow("Canny", sketchCanny(frame), 820, 20)

    key = cv.waitKey(1)
    if key == 27:
        break

# release video capture
capture.release()
# destroy windows
cv.destroyAllWindows()
