import cv2
import numpy as np
import os
import re
import logging
from paddleocr import PaddleOCR
from vietocr.tool.predictor import Predictor
from vietocr.tool.config import Cfg
from PIL import Image

# Cấu hình PaddleOCR và VietOCR
ocr = PaddleOCR(use_angle_cls=True, lang='vi', use_gpu=True)  # Chạy với GPU nếu có
config = Cfg.load_config_from_name('vgg_transformer')  # Cấu hình cho VietOCR
predictor = Predictor(config)

# Cấu hình logging
logging.basicConfig(level=logging.INFO)

# Tiền xử lý ảnh (phẳng ảnh, tăng độ tương phản nếu cần)
def preprocess_text_region(img):
    # Chuyển ảnh sang ảnh xám
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Làm phẳng ảnh (có thể tùy chỉnh thêm các bước nếu cần)
    _, threshed = cv2.threshold(gray_img, 150, 255, cv2.THRESH_BINARY)
    return threshed

# Cắt các vùng chứa văn bản
def extract_text_regions(image_path):
    try:
        # Chạy OCR bằng PaddleOCR
        result = ocr.ocr(image_path, cls=True)
        if result and len(result) > 0:
            # Sắp xếp kết quả theo vị trí y (từ trên xuống dưới)
            sorted_result = sorted(result[0], key=lambda x: x[0][0][1])
            logging.info(f"OCR thành công với {len(sorted_result)} dòng.")
            return sorted_result
        else:
            logging.warning("Không tìm thấy văn bản nào.")
            return None
    except Exception as e:
        logging.error(f"Lỗi trong quá trình OCR: {e}")
        return None

# Nhận diện văn bản với VietOCR
def recognize_text_with_vietocr(cropped_img):
    # Chuyển ảnh thành định dạng PIL
    pil_img = Image.fromarray(cv2.cvtColor(cropped_img, cv2.COLOR_BGR2RGB))
    # Dự đoán văn bản từ ảnh cắt bằng VietOCR
    result = predictor.predict(pil_img)
    return result

# Gán thông tin đã trích xuất vào các trường
def extract_info_from_ocr(result):
    fields = {
        "Tên": "",
        "Ngành": "",
        "Đơn vị": "",
        "Khoá": "",
        "MSV": ""
    }

    next_line_is_name = False
    next_line_is_major = False
    next_line_is_faculty = False
    found_msv = False

    for line in result:
        text = line.strip()
        if "THE SINH VIEN" in text.upper():
            next_line_is_name = True
            continue
        if next_line_is_name:
            fields["Tên"] = text
            next_line_is_name = False
            next_line_is_major = True
            continue
        if not found_msv and "MSV" in text.upper():
            msv_match = re.search(r"\d{9,}", text)
            if msv_match:
                fields["MSV"] = msv_match.group(0)
            found_msv = True
        if next_line_is_major:
            fields["Ngành"] = text
            next_line_is_major = False
            next_line_is_faculty = True
            continue
        if next_line_is_faculty:
            fields["Đơn vị"] = text
            next_line_is_faculty = False
            continue
        if re.search(r"\d{4}-\d{4}", text):
            fields["Khoá"] = text

    logging.info(f"Thông tin trích xuất: {fields}")
    return fields

# Hàm chính để xử lý ảnh
def process_image(image_path):
    # Lấy kết quả OCR từ PaddleOCR
    result = extract_text_regions(image_path)
    if not result:
        return None

    fields = {}

    # Duyệt qua các bounding boxes và xử lý từng đoạn văn bản
    for line in result:
        points = line[0]
        text = line[1][0]  # Lấy văn bản từ mỗi bounding box

        # Trích xuất và tiền xử lý các đoạn văn bản
        pts = np.array(points, dtype=np.int32)
        rect = cv2.boundingRect(pts)
        x, y, w, h = rect
        cropped_img = cv2.imread(image_path)[y:y+h, x:x+w]

        # Tiền xử lý ảnh (phẳng hóa, làm sắc nét, v.v...)
        preprocessed_img = preprocess_text_region(cropped_img)

        # Nhận diện văn bản với VietOCR
        recognized_text = recognize_text_with_vietocr(preprocessed_img)
        logging.info(f"Nhận diện văn bản: {recognized_text}")

        # Cập nhật kết quả vào các trường
        fields = extract_info_from_ocr(recognized_text)

    return fields

# Đường dẫn đến ảnh thẻ sinh viên
image_path = r"D:\Edu\Python\StudentID_FaceVerification\student-id-face-matching\test\imgTest\ThaiTuanIDCard.jpg"

# Gọi hàm xử lý ảnh
fields = process_image(image_path)
if fields:
    print(f"Thông tin đã trích xuất: {fields}")
else:
    print("Không có thông tin trích xuất được.")
