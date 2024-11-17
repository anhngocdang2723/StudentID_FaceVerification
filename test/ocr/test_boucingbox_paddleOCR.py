import cv2
import paddle
from paddleocr import PaddleOCR, draw_ocr
import numpy as np
import os

# Khởi tạo PaddleOCR
ocr = PaddleOCR(use_angle_cls=True, lang='vi', use_gpu=True)  # Bật GPU nếu có

# Hàm tiền xử lý ảnh
def preprocess_image(img_path):
    # Đọc ảnh
    img = cv2.imread(img_path)

    if img is None:
        raise ValueError("Không thể đọc ảnh từ đường dẫn: {}".format(img_path))

    # Chuyển đổi ảnh sang xám để giảm nhiễu và tăng tốc độ
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Áp dụng làm mờ để giảm nhiễu (blur)
    gray_img = cv2.GaussianBlur(gray_img, (5, 5), 0)

    # Chuyển ảnh xám thành ảnh nhị phân (để tăng cường độ tương phản)
    _, binary_img = cv2.threshold(gray_img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Trả về ảnh đã xử lý
    return binary_img

# Hàm phát hiện văn bản và vẽ bounding boxes
def detect_text_and_draw(img_path, save_path):
    # Tiền xử lý ảnh
    preprocessed_img = preprocess_image(img_path)

    # Lưu ảnh đã xử lý (nếu muốn kiểm tra ảnh sau khi tiền xử lý)
    preprocessed_path = img_path.replace('.jpg', '_preprocessed.jpg')
    cv2.imwrite(preprocessed_path, preprocessed_img)

    # Chạy OCR trên ảnh đã được tiền xử lý
    result = ocr.ocr(preprocessed_img, cls=True)

    if not result:
        raise ValueError("Không phát hiện được văn bản trong ảnh.")

    # Vẽ các bounding box lên ảnh gốc
    img = cv2.imread(img_path)

    # Vẽ bounding boxes và văn bản
    for line in result[0]:
        points = line[0]
        text = line[1][0]
        # Convert points từ danh sách ra thành một tứ giác (bounding box)
        pts = np.array(points, dtype=np.int32).reshape((-1, 1, 2))
        cv2.polylines(img, [pts], isClosed=True, color=(0, 255, 0), thickness=2)

        # Vẽ văn bản lên ảnh
        x, y = int(points[0][0]), int(points[0][1]) - 10  # Chỉnh vị trí text để không chồng lên bounding box
        cv2.putText(img, text, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        print(f"Văn bản: {text}")

    # Lấy tên ảnh gốc và thêm "_with_bboxes" vào tên file để lưu kết quả
    img_name = os.path.basename(img_path)
    name_without_extension, ext = os.path.splitext(img_name)
    output_file_name = f"{name_without_extension}_with_bboxes{ext}"
    output_file_path = os.path.join(save_path, output_file_name)

    # Lưu kết quả vào thư mục output
    cv2.imwrite(output_file_path, img)

    # Hiển thị ảnh kết quả
    # img_show = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    # cv2.imshow("Result", img_show)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    return output_file_path

# Đường dẫn tới ảnh thẻ sinh viên
img_path = r"D:\Edu\Python\StudentID_FaceVerification\student-id-face-matching\test\imgTest\NgocPhuongIDCard.jpg"
output_path = r'D:\Edu\Python\StudentID_FaceVerification\student-id-face-matching\test\ocr\resultOCR'

# Gọi hàm để phát hiện văn bản và vẽ bounding box
output_img_path = detect_text_and_draw(img_path, output_path)
print(f"Ảnh kết quả đã được lưu tại: {output_img_path}")
