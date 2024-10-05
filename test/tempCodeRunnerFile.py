import cv2
import numpy as np
from paddleocr import PaddleOCR

# Khởi tạo PaddleOCR
ocr = PaddleOCR(use_angle_cls=True, lang='en') 

# Đọc ảnh
img_path = r'D:\Edu\Python\StudentID_FaceVerification\student-id-face-matching\test\imgTest\NgocAnhIDCard_processed.jpg'
img = cv2.imread(img_path)

# Chạy OCR để lấy kết quả
result = ocr.ocr(img_path, cls=True)

# Vẽ các box quanh text
for line in result:
    for word_info in line:
        # Lấy tọa độ các góc của box (dạng 4 điểm)
        points = word_info[0]
        # Convert tọa độ sang dạng integer
        points = [(int(point[0]), int(point[1])) for point in points]
        # Vẽ đường viền box (dùng màu xanh lá)
        cv2.polylines(img, [np.array(points)], isClosed=True, color=(0, 255, 0), thickness=2)

# Hiển thị ảnh với box đã vẽ
cv2.imshow('Image with OCR boxes', img)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Lưu ảnh ra file nếu cần
cv2.imwrite(r'D:\Edu\Python\StudentID_FaceVerification\student-id-face-matching\test\resultTest\image_with_boxes.jpg', img)
