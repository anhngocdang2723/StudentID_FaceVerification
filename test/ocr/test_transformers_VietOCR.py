import cv2
import numpy as np
import os
from vietocr.tool.predictor import Predictor
from vietocr.tool.config import Cfg
from paddleocr import PaddleOCR
from PIL import Image

ocr = PaddleOCR(use_angle_cls=True, lang='vi', use_gpu=True)
config = Cfg.load_config_from_name('vgg_transformer')
predictor = Predictor(config)

def preprocess_for_vietocr(img):
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray_img = cv2.resize(gray_img, (256, 32))
    return gray_img

def detect_text_and_draw(img_path, save_path):
    if not os.path.exists(img_path):
        print("Không tìm thấy ảnh, kiểm tra lại đường dẫn.")
        return []

    result = ocr.ocr(img_path, cls=True)
    img = cv2.imread(img_path)

    if img is None:
        print("Không thể đọc ảnh, kiểm tra định dạng và đường dẫn.")
        return []

    for line in result[0]:
        points = line[0]
        text = line[1][0]
        pts = np.array(points, dtype=np.int32).reshape((-1, 1, 2))
        cv2.polylines(img, [pts], isClosed=True, color=(0, 255, 0), thickness=2)

        x, y = int(points[0][0]), int(points[0][1]) - 10
        cv2.putText(img, text, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    output_file_path = os.path.join(save_path, f"{os.path.splitext(os.path.basename(img_path))[0]}_with_bboxes.jpg")
    cv2.imwrite(output_file_path, img)
    print(f"Ảnh đã lưu tại: {output_file_path}")

    return result

def extract_text_region(img, bounding_box):
    pts = np.array(bounding_box, dtype=np.int32)
    rect = cv2.boundingRect(pts)
    x, y, w, h = rect
    return img[y:y+h, x:x+w]

def recognize_text_with_vietocr(img):
    pil_img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    result = predictor.predict(pil_img)
    return result

def process_image(img_path, save_path):
    result = detect_text_and_draw(img_path, save_path)
    if not result:
        return

    img = cv2.imread(img_path)
    for line in result[0]:
        points = line[0]
        cropped_img = extract_text_region(img, points)
        preprocessed_img = preprocess_for_vietocr(cropped_img)
        recognized_text = recognize_text_with_vietocr(preprocessed_img)
        print(f"Văn bản nhận diện được với VietOCR: {recognized_text}")

img_path = r"D:\Edu\Python\StudentID_FaceVerification\student-id-face-matching\test\imgTest\ThaiTuanIDCard.jpg"
output_path = r'D:\Edu\Python\StudentID_FaceVerification\student-id-face-matching\test\ocr\resultOCR'

process_image(img_path, output_path)
