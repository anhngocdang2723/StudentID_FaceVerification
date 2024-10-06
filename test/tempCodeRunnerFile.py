import cv2
import numpy as np

def detect_and_crop_card(image_path):
    # Đọc ảnh
    img = cv2.imread(image_path)
    
    # Chuyển đổi ảnh sang màu xám
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Ngưỡng để chỉ lấy vùng thẻ sinh viên (đảo ngược)
    retval, thresh_gray = cv2.threshold(gray, 220, 255, cv2.THRESH_BINARY_INV)  # Thay đổi giá trị ngưỡng

    # Tìm contour trong ảnh nhị phân
    contours, hierarchy = cv2.findContours(thresh_gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Tìm đối tượng có bounding box lớn nhất
    mx = (0, 0, 0, 0)  # bounding box lớn nhất
    mx_area = 0
    aspect_ratio_target = 1.6  # Tỷ lệ khung hình của thẻ sinh viên (khoảng 1.6:1)

    for cont in contours:
        x, y, w, h = cv2.boundingRect(cont)
        area = w * h
        
        # Tính tỷ lệ
        aspect_ratio = float(w) / h if h != 0 else 0
        
        # Kiểm tra diện tích và tỷ lệ
        if area > mx_area and aspect_ratio > 1.2 and aspect_ratio < 2.0:
            mx = (x, y, w, h)
            mx_area = area
            
    x, y, w, h = mx

    if mx_area == 0:
        print("Không tìm thấy thẻ sinh viên.")
        return

    # Cắt và lưu ảnh
    roi = img[y:y+h, x:x+w]
    cv2.imwrite("Cropped_Student_ID_Card.jpg", roi)

    # Vẽ hình chữ nhật bounding box (để debug)
    cv2.rectangle(img, (x, y), (x+w, y+h), (200, 0, 0), 2)
    cv2.imwrite("Image_cont.jpg", img)

# Đường dẫn đến ảnh thẻ sinh viên
image_path = r'D:\Edu\Python\StudentID_FaceVerification\student-id-face-matching\test\imgTest\ThaiTuanIDCard.jpg'
detect_and_crop_card(image_path)
