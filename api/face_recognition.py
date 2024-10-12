import cv2
import numpy as np
from fastapi import UploadFile

# Hàm đọc ảnh từ file tải lên
def read_image(file: UploadFile):
    image = np.fromstring(file.file.read(), np.uint8)
    return cv2.imdecode(image, cv2.IMREAD_COLOR)

# Hàm nhận diện khuôn mặt trong ảnh
def detect_faces(image):
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # Chuyển sang ảnh xám
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    return faces

# Hàm so sánh hai khuôn mặt từ hai ảnh
def compare_faces(image1, image2):
    faces1 = detect_faces(image1)
    faces2 = detect_faces(image2)

    if len(faces1) == 0:
        return "ảnh 1 không tìm thấy khuôn mặt"
    if len(faces2) == 0:
        return "ảnh 2 không tìm thấy khuôn mặt"
    
    # Cắt khuôn mặt
    (x1, y1, w1, h1) = faces1[0]
    face1 = image1[y1:y1+h1, x1:x1+w1]
    (x2, y2, w2, h2) = faces2[0]
    face2 = image2[y2:y2+h2, x2:x2+w2]
    
    # Resize 2 ảnh khuôn mặt về cùng kích thước
    face1_resized = cv2.resize(face1, (200, 200))
    face2_resized = cv2.resize(face2, (200, 200))

    # So sánh histogram của 2 ảnh khuôn mặt
    hist1 = cv2.calcHist([face1_resized], [0], None, [256], [0, 256])
    hist2 = cv2.calcHist([face2_resized], [0], None, [256], [0, 256])

    # Chuẩn hóa histogram
    hist1 = cv2.normalize(hist1, hist1)
    hist2 = cv2.normalize(hist2, hist2)

    # Tính độ tương đồng giữa 2 histogram
    similarity = cv2.compareHist(hist1, hist2, cv2.HISTCMP_CORREL)

    # Ngưỡng xác định cùng 1 người hay không
    if similarity > 0.7:
        return "Cùng 1 người"
    else:
        return "2 người khác nhau"
