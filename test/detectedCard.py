import cv2
import numpy as np

# Load the original image
image_path = r'D:\Edu\Python\StudentID_FaceVerification\student-id-face-matching\test\imgTest\NgocPhuongIDCard.jpg'
original_image = cv2.imread(image_path)

# Resize image if it's too large (optional)
scale_percent = 40  # percent of original size, you can adjust this if needed
width = int(original_image.shape[1] * scale_percent / 100)
height = int(original_image.shape[0] * scale_percent / 100)
dim = (width, height)
resized_image = cv2.resize(original_image, dim, interpolation=cv2.INTER_AREA)

# Convert the image to grayscale
gray_image = cv2.cvtColor(resized_image, cv2.COLOR_BGR2GRAY)

# Apply Gaussian blur to reduce noise
blurred_image = cv2.GaussianBlur(gray_image, (5, 5), 0)

# Use Canny edge detection to detect edges
edges = cv2.Canny(blurred_image, 50, 150)

# Find contours from the edges
contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Initialize variable to hold the largest contour (the ID card)
id_card_contour = None
max_area = 0

# Loop through the contours and find the largest rectangular contour
for contour in contours:
    perimeter = cv2.arcLength(contour, True)
    approx = cv2.approxPolyDP(contour, 0.02 * perimeter, True)
    
    # Check if the contour has 4 points (rectangle) and is larger than the current max
    if len(approx) == 4:
        area = cv2.contourArea(contour)
        if area > max_area:
            max_area = area
            id_card_contour = approx

# If a contour was found
if id_card_contour is not None:
    # Get the bounding rectangle of the ID card
    x, y, w, h = cv2.boundingRect(id_card_contour)
    
    # Crop the image to this bounding box
    cropped_id_card = resized_image[y:y+h, x:x+w]
    
    # Save the cropped image
    cropped_image_path = 'NgocAnhIDCard_Cropped.jpg'
    cv2.imwrite(cropped_image_path, cropped_id_card)
    print(f"Cropped image saved at: {cropped_image_path}")
    
    # Optionally display the cropped image
    # cv2.imshow("Cropped ID Card", cropped_id_card)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    
else:
    print("No ID card contour detected.")
