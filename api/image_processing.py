import cv2
import numpy as np
import os

PROCESSED_FOLDER = "processed_images"
##### Train model YoloV11 với custom dataset để detect thẻ tự động ####################
#######################################################################################


##### Đây là hàm tiền xử lý ảnh thẻ sinh viên ################################################################
# ở đây sẽ sử dụng model Yolo được train để detect thẻ sinh viên, sau đó crop ảnh thẻ và xử lý ảnh
# sau đó lưu ảnh đã xử lý vào thư mục PROCESSED_FOLDER để module face_extraction.py cắt khuôn mặt khỏi thẻ
##############################################################################################################

##### Cải tiến hàm preprocess_image
def preprocess_image(image_path: str) -> str:
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)

    processed_image_path = os.path.join(PROCESSED_FOLDER, f"processed_{os.path.basename(image_path)}")
    cv2.imwrite(processed_image_path, thresh)
    return processed_image_path