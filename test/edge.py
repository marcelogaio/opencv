import cv2 as cv

scale = 1
delta = 0
ddepth = cv.CV_16S
canny_threshold = 10

def preProcess(frame):
    # Convert image to grayscale
    frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    # Cleanup image using gaussian blur
    frame = cv.GaussianBlur(frame, (5, 5), 0)
    return frame


def sketchCanny(frame):
    # Extract Edges
    frame = cv.Canny(frame, canny_threshold, canny_threshold*3, 3)
    return frame


def sketchInvert(frame):
    # Do an invert binarize the image
    _, frame = cv.threshold(frame, 20, 255, cv.THRESH_BINARY)
    return frame


def on_trackbar_canny(val):
    canny_threshold = val
    print(val)


def createWindow(title, x, y, trackbar_array=()):
    # create window
    cv.namedWindow(title, cv.WINDOW_NORMAL)
    # create trackbars
    for values in trackbar_array:
        trackbar_name = values[0]
        trackbar_min_val = values[1]
        trackbar_max_val = values[2]
        trackbar_current_val = values[3]
        trackbar_function = values[4]
        trackbar_name = trackbar_name + ' x %d' % trackbar_max_val
        cv.createTrackbar(trackbar_name, title, trackbar_current_val, trackbar_max_val, trackbar_function)
        cv.setTrackbarMin(trackbar_name, title, trackbar_min_val)
    cv.resizeWindow(title, 800, 500)
    cv.moveWindow(title, x, y)


def updateImage(title, frame):
    fps = round(cv.getTickFrequency() / (cv.getTickCount() - start))
    cv.putText(frame, str(fps), (0, 30), cv.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255))
    cv.imshow(title, frame)


# init video capture
capture = cv.VideoCapture(0)
capture.set(cv.CAP_PROP_FPS, 1)

# declare trackbars
trackbar_canny = [['Canny Threshold', 0, 100, canny_threshold, on_trackbar_canny]]

# create windows
createWindow("Canny", 20, 20, trackbar_canny)
createWindow("Canny + Invert", 820, 20)

# loop frames
while True:
    start = cv.getTickCount()
    _, frame = capture.read()
    if frame is not None:
        frame = preProcess(frame)
        # update images
        updateImage("Canny", sketchCanny(frame))
        updateImage("Canny + Invert", sketchCanny(sketchInvert(frame)))

    # capture esc key
    key = cv.waitKey(1)
    if key == 27:
        break

# release video capture
capture.release()
# destroy windows
cv.destroyAllWindows()
