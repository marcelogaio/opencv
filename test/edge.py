import cv2 as cv

scale = 1
delta = 0
ddepth = cv.CV_16S
canny_threshold = 10
filter_threshold = 20
canny_index = 3
kernel_size = 3

def preProcess(frame):
    # Convert image to grayscale
    frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    # Cleanup image using gaussian blur
    frame = cv.GaussianBlur(frame, (5, 5), 0)
    return frame


def sketchCanny(frame):
    # Extract Edges
    frame = cv.Canny(frame, canny_threshold, canny_threshold*canny_index, kernel_size)
    return frame


def sketchInvert(frame):
    # Do an invert binarize the image
    _, frame = cv.threshold(frame, filter_threshold, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C)
    return frame


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


def on_trackbar_canny_threshold(val):
    global canny_threshold
    canny_threshold = val


def on_trackbar_canny_index(val):
    global canny_index
    canny_index = val


def on_trackbar_kernel_size(val):
    global kernel_size
    kernel_size = val


def on_trackbar_filter_threshold(val):
    global filter_threshold
    filter_threshold = val


# init video capture
capture = cv.VideoCapture(0)
capture.set(cv.CAP_PROP_FPS, 1)

# declare trackbars
trackbar_canny_threshold = ['Canny Threshold', 0, 200, canny_threshold, on_trackbar_canny_threshold]
trackbar_canny_index = ['Canny Index', 0, 100, canny_index, on_trackbar_canny_index]
trackbar_kernel_size = ['Kernel Size', 0, 100, kernel_size, on_trackbar_kernel_size]
trackbar_filter_threshold = ['Invert Threshold', 0, 255, filter_threshold, on_trackbar_filter_threshold]
trackbars = [trackbar_canny_threshold, trackbar_canny_index, trackbar_kernel_size, trackbar_filter_threshold]

# create windows
createWindow("Original", 20, 20, trackbars)
createWindow("Filter", 820, 20)
createWindow("Canny", 20, 520)
createWindow("Filter+Canny", 820, 520)

# loop frames
while True:
    start = cv.getTickCount()
    _, frame = capture.read()
    if frame is not None:
        frame = preProcess(frame)
        threshold_frame = sketchInvert(frame)
        canny_frame = sketchCanny(frame)
        threshold_canny_frame = sketchCanny(threshold_frame)
        # update images
        updateImage("Original", frame)
        updateImage("Filter", threshold_frame)
        updateImage("Canny", canny_frame)
        updateImage("Filter+Canny", threshold_canny_frame)

    # capture esc key
    key = cv.waitKey(1)
    if key == 27:
        break

# release video capture
capture.release()
# destroy windows
cv.destroyAllWindows()
