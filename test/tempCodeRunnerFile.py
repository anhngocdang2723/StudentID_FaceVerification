import cv2
import numpy as np

# Module level constants
GAUSSIAN_SMOOTH_FILTER_SIZE = (5, 5)
ADAPTIVE_THRESH_BLOCK_SIZE = 19
ADAPTIVE_THRESH_WEIGHT = 9

def setWindowProperties(windowName, width, height, x, y):
    """
    Sets the size and position of a window.

    Args:
        windowName (str): Name of the window.
        width (int): Desired width of the window.
        height (int): Desired height of the window.
        x (int): X-coordinate of the top-left corner of the window.
        y (int): Y-coordinate of the top-left corner of the window.
    """
    cv2.namedWindow(windowName, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(windowName, width, height)
    cv2.moveWindow(windowName, x, y)

def extractValue(imgOriginal):
    """
    Extracts the Value channel from the HSV color space.

    Args:
        imgOriginal (numpy.ndarray): Input color image.

    Returns:
        numpy.ndarray: Grayscale image based on the Value channel.
    """
    imgHSV = cv2.cvtColor(imgOriginal, cv2.COLOR_BGR2HSV)
    _, _, imgValue = cv2.split(imgHSV)  # Extract only the Value channel
    return imgValue

def maximizeContrast(imgGrayscale):
    """
    Enhances contrast using morphological operations.

    Args:
        imgGrayscale (numpy.ndarray): Grayscale input image.

    Returns:
        numpy.ndarray: Contrast-enhanced grayscale image.
    """
    structuringElement = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))

    # Morphological transformations
    imgTopHat = cv2.morphologyEx(imgGrayscale, cv2.MORPH_TOPHAT, structuringElement, iterations=10)
    imgBlackHat = cv2.morphologyEx(imgGrayscale, cv2.MORPH_BLACKHAT, structuringElement, iterations=10)

    # Combine transformations
    imgGrayscalePlusTopHat = cv2.add(imgGrayscale, imgTopHat)
    imgGrayscalePlusTopHatMinusBlackHat = cv2.subtract(imgGrayscalePlusTopHat, imgBlackHat)

    return imgGrayscalePlusTopHatMinusBlackHat

def preprocess(imgOriginal, debug=False):
    """
    Preprocess the input image for better feature extraction.

    Args:
        imgOriginal (numpy.ndarray): Input color image.
        debug (bool): If True, displays intermediate processing steps.

    Returns:
        tuple: Grayscale image and thresholded binary image.
    """
    step_images = []  # List to hold images at each step

    # Step 1: Extract the Value channel
    imgGrayscale = extractValue(imgOriginal)
    step_images.append(imgGrayscale)  # Add to list
    if debug:
        windowName = "Step 1: Grayscale Image (Value Channel)"
        cv2.imshow(windowName, imgGrayscale)

    # Step 2: Maximize contrast
    imgMaxContrastGrayscale = maximizeContrast(imgGrayscale)
    step_images.append(imgMaxContrastGrayscale)  # Add to list
    if debug:
        windowName = "Step 2: Maximized Contrast"
        cv2.imshow(windowName, imgMaxContrastGrayscale)

    # Step 3: Gaussian Blur
    imgBlurred = cv2.GaussianBlur(imgMaxContrastGrayscale, GAUSSIAN_SMOOTH_FILTER_SIZE, 0)
    step_images.append(imgBlurred)  # Add to list
    if debug:
        windowName = "Step 3: Gaussian Blurred"
        cv2.imshow(windowName, imgBlurred)

    # Step 4: Adaptive Thresholding
    imgThresh = cv2.adaptiveThreshold(
        imgBlurred,
        255.0,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY_INV,
        ADAPTIVE_THRESH_BLOCK_SIZE,
        ADAPTIVE_THRESH_WEIGHT
    )
    step_images.append(imgThresh)  # Add to list
    if debug:
        windowName = "Step 4: Thresholded Binary Image"
        cv2.imshow(windowName, imgThresh)

    # Combine all images into one for display
    if step_images:
        stacked_img = np.hstack(step_images)  # Concatenate images horizontally
        cv2.imshow("Processing Steps", stacked_img)
        cv2.waitKey(0)

    return imgGrayscale, imgThresh

def findCorners(imgThresh, debug=False):
    """
    Finds the four corners of the largest rectangular contour in the binary image.

    Args:
        imgThresh (numpy.ndarray): Thresholded binary image.
        debug (bool): If True, displays intermediate processing steps.

    Returns:
        numpy.ndarray or None: Array of four corner points if found, otherwise None.
    """
    edges = cv2.Canny(imgThresh, 100, 200)
    if debug:
        windowName = "Edges Detected"
        cv2.imshow(windowName, edges)

    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)

    for contour in contours:
        peri = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, 0.02 * peri, True)

        if len(approx) == 4:
            if debug:
                imgContours = cv2.cvtColor(imgThresh, cv2.COLOR_GRAY2BGR)
                cv2.drawContours(imgContours, [approx], -1, (0, 255, 0), 2)
                windowName = "Detected Contour with Four Corners"
                cv2.imshow(windowName, imgContours)

            return approx.reshape(4, 2)

    return None

# Testing the Corner Detection Pipeline
if __name__ == "__main__":
    imgPath = r"D:\Edu\Python\StudentID_FaceVerification\student-id-face-matching\test\imgTest\z5903394151288_49235aed016f400877949e1d25163e52.jpg"
    imgOriginal = cv2.imread(imgPath)

    if imgOriginal is None:
        print("Error: Image not found!")
    else:
        imgGrayscale, imgThresh = preprocess(imgOriginal, debug=True)
        corners = findCorners(imgThresh, debug=True)

        if corners is not None:
            print("Detected Corners:")
            print(corners)
        else:
            print("No rectangle with four corners was detected.")

        cv2.waitKey(0)
        cv2.destroyAllWindows()
