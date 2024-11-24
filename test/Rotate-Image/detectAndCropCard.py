# detectAndCropCard.py

from ultralytics import YOLO
import cv2
import numpy as np

def detect_and_crop_student_card(image_path, model_path, confidence_threshold=0.8, expansion_factor=0.05):
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
            # x1 = max(0, x1-5)
            # y1 = max(0, y1-5)
            # x2 = min(width, x2 + 5)
            # y2 = min(height, y2 + 5)

            # # Expand the bounding box
            x1 = max(0, x1 - int(expansion_factor * box_width))
            y1 = max(0, y1 - int(expansion_factor * box_height))
            x2 = min(width, x2 + int(expansion_factor * box_width))
            y2 = min(height, y2 + int(expansion_factor * box_height))

            cropped_card = image[y1:y2, x1:x2]
            return cropped_card, (x1, y1, x2, y2)

    print("No student card detected with sufficient confidence.")
    return None, None