
import cv2
import numpy as np
from paddleocr import PaddleOCR
import os
import logging

# Khởi tạo OCR và CascadeClassifier một lần khi khởi động module
ocr = PaddleOCR(use_angle_cls=True, lang='en')
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

logging.basicConfig(level=logging.INFO)

def resize_image(img, scale_percent):
    width = int(img.shape[1] * scale_percent / 100)
    height = int(img.shape[0] * scale_percent / 100)
    dim = (width, height)
    return cv2.resize(img, dim)

def detect_face(img, scale_percent=50):
    resized_img = resize_image(img, scale_percent)
    faces = face_cascade.detectMultiScale(cv2.cvtColor(resized_img, cv2.COLOR_BGR2GRAY), scaleFactor=1.1, minNeighbors=5)
    
    if len(faces) > 0:
        (x, y, w, h) = faces[0]
        # Điều chỉnh tọa độ theo kích thước gốc
        x = int(x * (100 / scale_percent))
        y = int(y * (100 / scale_percent))
        w = int(w * (100 / scale_percent))
        h = int(h * (100 / scale_percent))
        return img[y:y+h, x:x+w]
    return None

def apply_ocr(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
    result = ocr.ocr(thresh, cls=True)

    for line in result:
        for word_info in line:
            points = word_info[0]
            points = [(int(point[0]), int(point[1])) for point in points]
            cv2.polylines(thresh, [np.array(points)], isClosed=True, color=(0, 255, 0), thickness=2)
    return thresh

def process_student_id(img_path, output_face_path, output_processed_path):
    try:
        img = cv2.imread(img_path)
        if img is None:
            raise ValueError(f"Không thể đọc được ảnh từ đường dẫn {img_path}")
        
        logging.info("Đã đọc thành công ảnh.")
        
        face_img = detect_face(img)

        if face_img is not None:
            cv2.imwrite(output_face_path, face_img)
            processed_img = apply_ocr(img)
            cv2.imwrite(output_processed_path, processed_img)
            logging.info("Xử lý hoàn tất.")
            return True
        else:
            logging.warning("Không tìm thấy khuôn mặt.")
            return False
    except Exception as e:
        logging.error(f"Lỗi trong quá trình xử lý: {e}")
        return False
