from ultralytics import YOLO
import cv2
import numpy as np

def detect_and_crop_student_card(image_path, model_path, confidence_threshold=0.8, expansion_factor=0.1):
    model = YOLO(model_path)
    image = cv2.imread(image_path)
    height, width, _ = image.shape
    results = model(image)

    for result in results:
        for box in result.boxes:
            confidence = box.conf[0]
            if confidence < confidence_threshold:
                continue

            x1, y1, x2, y2 = map(int, box.xyxy[0])
            box_width = x2 - x1
            box_height = y2 - y1

            # Expand the bounding box
            x1 = max(0, x1 - int(expansion_factor * box_width))
            y1 = max(0, y1 - int(expansion_factor * box_height))
            x2 = min(width, x2 + int(expansion_factor * box_width))
            y2 = min(height, y2 + int(expansion_factor * box_height))

            cropped_card = image[y1:y2, x1:x2]
            return cropped_card, (x1, y1, x2, y2)

    print("No student card detected with sufficient confidence.")
    return None, None

def preprocess_image(image, resize_dim=(500, 500)):
    """
    Perform preprocessing steps and display intermediate results for debugging.
    - Resize
    - Convert to grayscale
    - Reduce noise
    - Enhance contrast
    - Apply edge detection

    Args:
        image (numpy.ndarray): The input image to preprocess.
        resize_dim (tuple): Dimensions to resize the image to (width, height).

    Returns:
        edges (numpy.ndarray): Processed edges of the image.
    """
    # Step 1: Resize the image
    resized = cv2.resize(image, resize_dim, interpolation=cv2.INTER_AREA)
    cv2.imshow("Step 1: Resized Image", resized)

    # Step 2: Convert to grayscale
    gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
    cv2.imshow("Step 2: Grayscale Image", gray)

    # Step 3: Noise reduction with Gaussian blur
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    cv2.imshow("Step 3: Blurred Image", blurred)

    # Step 4: Contrast enhancement (Histogram Equalization)
    enhanced = cv2.equalizeHist(blurred)
    cv2.imshow("Step 4: Enhanced Contrast Image", enhanced)

    # Step 5: Edge detection using Canny
    edges = cv2.Canny(enhanced, 50, 150)
    cv2.imshow("Step 5: Edge Detection", edges)

    # Wait for a key press to inspect each step
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return edges

def find_corners_and_align(cropped_image):
    """
    Detect the 4 corners of the student card in the cropped image and return them.

    Args:
        cropped_image (numpy.ndarray): Cropped student card image.

    Returns:
        rect (numpy.ndarray): Sorted corners of the student card in the order:
                              [top-left, top-right, bottom-right, bottom-left].
    """
    if cropped_image is None:
        print("No cropped image to process.")
        return None

    # Step 1: Preprocess the image
    edges = preprocess_image(cropped_image)

    # Find contours
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Check if contours are found
    if not contours:
        print("No contours found.")
        return None

    # Filter out small contours based on area (if needed)
    contours = [cnt for cnt in contours if cv2.contourArea(cnt) > 1000]

    # If no valid contours after filtering, return None
    if not contours:
        print("No valid contours found.")
        return None

    # Find the largest contour
    largest_contour = max(contours, key=cv2.contourArea)

    # Approximate the contour to a polygon
    epsilon = 0.02 * cv2.arcLength(largest_contour, True)
    approx = cv2.approxPolyDP(largest_contour, epsilon, True)

    # Ensure it has 4 corners
    if len(approx) == 4:
        corners = approx.reshape((4, 2))

        # Sort corners: [top-left, top-right, bottom-right, bottom-left]
        rect = np.zeros((4, 2), dtype="float32")
        s = corners.sum(axis=1)
        rect[0] = corners[np.argmin(s)]  # Top-left
        rect[2] = corners[np.argmax(s)]  # Bottom-right

        diff = np.diff(corners, axis=1)
        rect[1] = corners[np.argmin(diff)]  # Top-right
        rect[3] = corners[np.argmax(diff)]  # Bottom-left

        # Draw corners for visualization
        for i, point in enumerate(rect):
            cv2.circle(cropped_image, tuple(point.astype(int)), 5, (0, 255, 0), -1)
            cv2.putText(
                cropped_image, f"{i}", tuple(point.astype(int)),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2
            )

        # Display the result with corners
        cv2.imshow("Corners Detected", cropped_image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        return rect
    else:
        print("Could not find 4 corners.")
        return None

# Main program
if __name__ == "__main__":
    # Paths to the model and input image
    model_path = r"D:\\Edu\\Python\\StudentID_FaceVerification\\student-id-face-matching\\api\\models\\best.pt"
    image_path = r"D:\Edu\Python\StudentID_FaceVerification\student-id-face-matching\api\(delete)img\z6064540687987_233d13005fcf206b079f54a25a4f0ed1.jpg"

    # Step 1: Detect and crop the student card
    cropped_card, bbox = detect_and_crop_student_card(image_path, model_path)
    if cropped_card is not None:
        print("Student card cropped successfully.")

        # Step 2: Find corners in the cropped card
        corners = find_corners_and_align(cropped_card)
        if corners is not None:
            print("Detected corners:", corners)
        else:
            print("Failed to detect corners.")
    else:
        print("No card detected.")
