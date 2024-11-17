import cv2
import numpy as np
import os
import re
import logging
from vietocr.tool.predictor import Predictor
from vietocr.tool.config import Cfg
from paddleocr import PaddleOCR
from PIL import Image

# Khởi tạo PaddleOCR
ocr = PaddleOCR(use_angle_cls=True, lang='vi', use_gpu=True)

# Cấu hình VietOCR
config = Cfg.load_config_from_name('vgg_transformer')
predictor = Predictor(config)

# Hàm tiền xử lý ảnh (resize và chuyển sang xám nếu cần thiết)
def preprocess_for_vietocr(img):
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray_img = cv2.resize(gray_img, (256, 32))
    return gray_img

# Hàm phát hiện văn bản và vẽ bounding boxes
def detect_text_and_draw(img_path, save_path):
    result = ocr.ocr(img_path, cls=True)
    img = cv2.imread(img_path)

    for line in result[0]:
        points = line[0]
        text = line[1][0]
        pts = np.array(points, dtype=np.int32).reshape((-1, 1, 2))
        cv2.polylines(img, [pts], isClosed=True, color=(0, 255, 0), thickness=2)
        x, y = int(points[0][0]), int(points[0][1]) - 10
        cv2.putText(img, text, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    img_name = os.path.basename(img_path)
    name_without_extension, ext = os.path.splitext(img_name)
    output_file_name = f"{name_without_extension}_with_bboxes{ext}"
    output_file_path = os.path.join(save_path, output_file_name)
    cv2.imwrite(output_file_path, img)

    img_show = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    cv2.imshow("Result", img_show)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return result

# Hàm trích xuất các khu vực chứa văn bản từ các bounding boxes
def extract_text_region(img, bounding_box):
    pts = np.array(bounding_box, dtype=np.int32)
    rect = cv2.boundingRect(pts)
    x, y, w, h = rect
    return img[y:y+h, x:x+w]

# Hàm nhận diện văn bản với VietOCR
def recognize_text_with_vietocr(img):
    pil_img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    result = predictor.predict(pil_img)
    return result

# Hàm để trích xuất và phân loại thông tin từ kết quả OCR
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

    for line in result[0]:
        text = line[1][0].strip()
        if "THE SINH VIEN" in text.upper():
            next_line_is_name = True
            continue

        if next_line_is_name:
            fields["Tên"] = clean_text(text)
            next_line_is_name = False
            next_line_is_major = True
            continue

        if not found_msv and ("MSV" in text.upper() or re.search(r"\d{9,}", text)):
            msv_match = re.search(r"\d{9,}", text)
            if msv_match:
                fields["MSV"] = msv_match.group(0)
                found_msv = True
            continue

        if next_line_is_major:
            fields["Ngành"] = clean_text(text)
            next_line_is_major = False
            next_line_is_faculty = True
            continue

        if next_line_is_faculty:
            fields["Đơn vị"] = clean_text(text)
            next_line_is_faculty = False
            continue

        if re.search(r"\d{4}-\d{4}", text):
            fields["Khoá"] = text

    logging.info(f"Thông tin trích xuất: {fields}")
    return fields

def clean_text(text):
    """Hàm để làm sạch văn bản, loại bỏ các ký tự không mong muốn."""
    return re.sub(r"[^a-zA-Z0-9\sÀÁÂÃÈÉÊÌÍÒÓÔÕÙÚĂĐĨŨƠàáâãèéêìíòóôõùúăđĩũơưƯĂẠẢẤẦẨẪẬẮẰẲẴẶẸẺẼỀỀểếỆỈỊỌỎỐỒỔỖỘỚỜỞỠỢỤỦỨỪễữựỳỵỷỹý]", "", text)

# Hàm chính để xử lý ảnh
def process_image(img_path, save_path):
    result = detect_text_and_draw(img_path, save_path)
    img = cv2.imread(img_path)

    for line in result[0]:
        points = line[0]
        cropped_img = extract_text_region(img, points)
        preprocessed_img = preprocess_for_vietocr(cropped_img)
        recognized_text = recognize_text_with_vietocr(preprocessed_img)
        print(f"Văn bản nhận diện được với VietOCR: {recognized_text}")

    # Gọi hàm để trích xuất thông tin từ kết quả OCR và sắp xếp vào fields
    fields = extract_info_from_ocr(result)
    print("Thông tin sắp xếp vào các trường:", fields)

# Đường dẫn đến ảnh thẻ sinh viên
img_path = r"D:\Edu\Python\StudentID_FaceVerification\student-id-face-matching\test\imgTest\ThaiTuanIDCard.jpg"
output_path = r'D:\Edu\Python\StudentID_FaceVerification\student-id-face-matching\test\ocr\resultOCR'

# Gọi hàm xử lý ảnh
process_image(img_path, output_path)
