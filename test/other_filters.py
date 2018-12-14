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


def sketchLaplacian(frame):
    # Laplacian filter
    frame = cv.Laplacian(frame, cv.CV_64F)
    # Do an invert binarize the image
    ret, frame = cv.threshold(frame, 70, 255, cv.THRESH_BINARY)
    return frame


def sketchSobel(frame):
    # Sobel filter
    grad_x = cv.Sobel(frame, ddepth, 1, 0, ksize=3, scale=scale, delta=delta, borderType=cv.BORDER_DEFAULT)
    grad_y = cv.Sobel(frame, ddepth, 0, 1, ksize=3, scale=scale, delta=delta, borderType=cv.BORDER_DEFAULT)
    abs_grad_x = cv.convertScaleAbs(grad_x)
    abs_grad_y = cv.convertScaleAbs(grad_y)
    frame = cv.addWeighted(abs_grad_x, 0.5, abs_grad_y, 0.5, 0)
    return frame


def showWindow(title, frame, x, y):
    cv.namedWindow(title, cv.WINDOW_NORMAL)
    cv.resizeWindow(title, 800, 500)
    # cv.putText(frame, text, (0, 30), cv.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255))
    cv.imshow(title, frame)
    cv.moveWindow(title, x, y)


# init video capture
capture = cv.VideoCapture(0)
capture.set(cv.CAP_PROP_FPS, 1)


# loop frames
while True:
    _, frame = capture.read()
    if frame is not None:
        frame = preProcess(frame)
        showWindow("Frame", frame, 20, 20)
        showWindow("Laplacian", sketchLaplacian(frame), 820, 20)
        showWindow("Sobel", sketchSobel(frame), 20, 550)

    key = cv.waitKey(1)
    if key == 27:
        break

# release video capture
capture.release()
# destroy windows
cv.destroyAllWindows()
