from paddleocr import PaddleOCR, draw_ocr
import cv2

# Khởi tạo mô hình PaddleOCR với ngôn ngữ Tiếng Việt
ocr = PaddleOCR(use_angle_cls=True, lang='vi')  # 'vi' cho Tiếng Việt

# Đường dẫn tới ảnh thẻ sinh viên
img_path = r"StudentID_FaceVerification/student-id-face-matching/img/R.jpg"

# Nhận diện văn bản từ ảnh
result = ocr.ocr(img_path, cls=True)

# Hiển thị kết quả
for line in result[0]:
    print(f"Văn bản: {line[1][0]}, Độ tin cậy: {line[1][1]}")

# Nếu muốn vẽ kết quả lên ảnh
image = cv2.imread(img_path)
boxes = [elements[0] for elements in result[0]]
texts = [elements[1][0] for elements in result[0]]
scores = [elements[1][1] for elements in result[0]]

# Vẽ box và văn bản lên ảnh
for box, text, score in zip(boxes, texts, scores):
    cv2.polylines(image, [np.array(box).astype(np.int32)], isClosed=True, color=(0, 255, 0), thickness=2)
    cv2.putText(image, text, (int(box[0][0]), int(box[0][1] - 10)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)

# Hiển thị ảnh với kết quả
cv2.imshow('PaddleOCR Result', image)
cv2.waitKey(0)
cv2.destroyAllWindows()
