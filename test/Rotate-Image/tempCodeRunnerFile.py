import cv2
import numpy as np
from ultralytics import YOLO
from stackImages import stackImages
from detectAndCropCard import detect_and_crop_student_card
from preprocess import preprocess

# Load the image
image_path = r"D:\Edu\Python\StudentID_FaceVerification\student-id-face-matching\api\(delete)img\z6064540674209_d2867f1b56ed095258b42b3cc840cd0a.jpg"
model_path = r"D:\\Edu\\Python\\StudentID_FaceVerification\\student-id-face-matching\\api\\models\\best.pt"

# Step 1: Detect and crop the student card
cropped_card, bbox = detect_and_crop_student_card(image_path, model_path)
if cropped_card is not None:
    print("Student card cropped successfully.")

    # Step 2: Preprocess the cropped card
    imgGrayscale, imgThresh = preprocess(cropped_card)
    imgStack = stackImages(0.6, [[cropped_card, imgGrayscale, imgThresh]])

    # Step 3: Find contours in the thresholded image
    contours, hierarchy = cv2.findContours(imgThresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    print(f"Number of contours found: {len(contours)}")

    # Sort contours by area in descending order
    sorted_contours = sorted(contours, key=cv2.contourArea, reverse=True)

    # Take the top 10 largest contours
    top_10_contours = sorted_contours[:10]

    # Draw the top 10 contours on a copy of the cropped card
    imgContours = cropped_card.copy()
    cv2.drawContours(imgContours, top_10_contours, -1, (0, 255, 0), 2)  # Green contours

    # Display results
    result_stack = stackImages(0.6, [[cropped_card, imgThresh, imgContours]])
    cv2.imwrite("cropped.jpg", cropped_card)
    cv2.imshow("Top 10 Contours on Student Card", result_stack)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

else:
    print("Failed to detect student card.")
