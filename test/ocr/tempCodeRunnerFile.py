import cv2
import numpy as np
import os
from vietocr.tool.predictor import Predictor
from vietocr.tool.config import Cfg
from paddleocr import PaddleOCR, draw_ocr
from PIL import Image

# Khởi tạo PaddleOCR
ocr = PaddleOCR(use_angle_cls=True, lang='vi', use_gpu=True)  # Tắt GPU nếu không có GPU

# Cấu hình VietOCR
config = Cfg.load_config_from_name('vgg_transformer')
predictor = Predictor(config)

# Hàm tiền xử lý ảnh (resize và chuyển sang xám nếu cần thiết)
def preprocess_for_vietocr(img):
    # Chuyển đổi ảnh sang xám
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Resize ảnh cho phù hợp với mô hình
    gray_img = cv2.resize(gray_img, (256, 32))  # Điều chỉnh kích thước cho mô hình
    return gray_img

# Hàm phát hiện văn bản và vẽ bounding boxes
def detect_text_and_draw(img_path, save_path):
    # Chạy OCR trên ảnh gốc với PaddleOCR
    result = ocr.ocr(img_path, cls=True)
    
    # Đọc ảnh gốc
    img = cv2.imread(img_path)

    # Vẽ các bounding boxes và văn bản lên ảnh
    for line in result[0]:
        points = line[0]
        text = line[1][0]
        # Convert points từ danh sách ra thành một tứ giác (bounding box)
        pts = np.array(points, dtype=np.int32).reshape((-1, 1, 2))
        cv2.polylines(img, [pts], isClosed=True, color=(0, 255, 0), thickness=2)

        # Vẽ văn bản lên ảnh
        x, y = int(points[0][0]), int(points[0][1]) - 10  # Chỉnh vị trí text để không chồng lên bounding box
        cv2.putText(img, text, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Lưu ảnh với các bounding box vẽ trên đó
    img_name = os.path.basename(img_path)
    name_without_extension, ext = os.path.splitext(img_name)
    output_file_name = f"{name_without_extension}_with_bboxes{ext}"
    output_file_path = os.path.join(save_path, output_file_name)
    cv2.imwrite(output_file_path, img)

    # Hiển thị ảnh kết quả
    img_show = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    cv2.imshow("Result", img_show)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return result  # Trả về kết quả nhận diện văn bản

# Hàm trích xuất các khu vực chứa văn bản từ các bounding boxes
def extract_text_region(img, bounding_box):
    # bounding_box là danh sách các điểm tạo thành tứ giác (polygon)
    pts = np.array(bounding_box, dtype=np.int32)
    rect = cv2.boundingRect(pts)
    x, y, w, h = rect
    return img[y:y+h, x:x+w]

# Hàm nhận diện văn bản với VietOCR
def recognize_text_with_vietocr(img):
    # Chuyển đổi ảnh từ numpy.ndarray sang PIL.Image
    pil_img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

    # Dự đoán văn bản với VietOCR
    result = predictor.predict(pil_img)  # predictor đã được khởi tạo trước đó

    return result

# Hàm chính để xử lý ảnh
def process_image(img_path, save_path):
    # Tiến hành phát hiện văn bản và vẽ bounding boxes
    result = detect_text_and_draw(img_path, save_path)

    # Đọc lại ảnh gốc
    img = cv2.imread(img_path)

    # Duyệt qua các bounding boxes và trích xuất văn bản từ từng khu vực
    for line in result[0]:
        points = line[0]
        text = line[1][0]  # Lấy văn bản từ mỗi bounding box

        # Trích xuất khu vực văn bản từ bounding box
        cropped_img = extract_text_region(img, points)

        # Tiền xử lý ảnh nếu cần thiết trước khi đưa vào mô hình VietOCR
        preprocessed_img = preprocess_for_vietocr(cropped_img)

        # Chuyển đổi ảnh đã tiền xử lý thành văn bản và nhận diện văn bản với VietOCR
        recognized_text = recognize_text_with_vietocr(preprocessed_img)

        # In ra văn bản nhận diện được
        print(f"Văn bản nhận diện được với VietOCR: {recognized_text}")

# Đường dẫn đến ảnh thẻ sinh viên
img_path = r"D:\Edu\Python\StudentID_FaceVerification\student-id-face-matching\test\imgTest\ThaiTuanIDCard.jpg"
output_path = r'D:\Edu\Python\StudentID_FaceVerification\student-id-face-matching\test\ocr\resultOCR'

# Gọi hàm xử lý ảnh
process_image(img_path, output_path)
