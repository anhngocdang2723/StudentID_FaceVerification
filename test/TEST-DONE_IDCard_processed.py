import cv2
import numpy as np
from paddleocr import PaddleOCR

ocr = PaddleOCR(use_angle_cls=True, lang='en')

img_path = r"D:\\Edu\\Python\\StudentID_FaceVerification\\student-id-face-matching\\test\\imgTest\\NgocAnhIDCard.jpg"
img = cv2.imread(img_path)

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# giảm kích thước ảnh
scale_percent = 50
width = int(img.shape[1] * scale_percent / 100)
height = int(img.shape[0] * scale_percent / 100)
dim = (width, height)
resized_img = cv2.resize(img, dim)

faces = face_cascade.detectMultiScale(cv2.cvtColor(resized_img, cv2.COLOR_BGR2GRAY), scaleFactor=1.1, minNeighbors=5)

if len(faces) > 0:
    (x, y, w, h) = faces[0]
    
    # chuyển toạ độ theo kích thước gốc
    x = int(x * (100 / scale_percent))
    y = int(y * (100 / scale_percent))
    w = int(w * (100 / scale_percent))
    h = int(h * (100 / scale_percent))

    face_img = img[y:y+h, x:x+w]
    cv2.imwrite(r"D:\\Edu\\Python\\StudentID_FaceVerification\\student-id-face-matching\\test\\resultTest\\NgocAnhIDCard_face.jpg", face_img)

    cv2.imshow("Face", face_img)

    # ap dụng ngưỡng hóa để tạo ảnh nhị phân
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)

    # Chạy OCR trên ảnh ngưỡng hóa
    result = ocr.ocr(thresh, cls=True)

    # Vẽ box lên ảnh ngưỡng hóa
    for line in result:
        for word_info in line:
            # Lấy toạ độ các góc của box
            points = word_info[0]
            # Chuyển đổi toạ độ sang dạng integer
            points = [(int(point[0]), int(point[1])) for point in points]
            # Vẽ viền theo points
            cv2.polylines(thresh, [np.array(points)], isClosed=True, color=(0, 255, 0), thickness=2)

    cv2.imwrite(r'D:\\Edu\\Python\\StudentID_FaceVerification\\student-id-face-matching\\test\\resultTest\\NgocAnhIDCard_processed_with_boxes.jpg', thresh)

    cv2.imshow('Processed Image with OCR boxes', thresh)

else:
    print("Không tìm thấy khuôn mặt.")

cv2.waitKey(0)
cv2.destroyAllWindows()
