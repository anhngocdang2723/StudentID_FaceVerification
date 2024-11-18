from ultralytics import YOLO
import cv2
import time
import os
import logging
from paddleocr import PaddleOCR
import re

ocr = PaddleOCR(use_angle_cls=True, lang='vi')

model = YOLO(r"D:\Edu\Python\StudentID_FaceVerification\student-id-face-matching\api\models\best.pt")

video_path = r"D:\Edu\Python\StudentID_FaceVerification\student-id-face-matching\test\imgTest\5974983164661.mp4"
cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    print("Không thể mở video.")
    exit()

# Ngưỡng confidence tối thiểu để lưu ảnh
confidence_threshold = 0.94
padding = 10

logging.basicConfig(level=logging.INFO)

def perform_ocr(image_path):
    try:
        result = ocr.ocr(image_path, cls=True)
        if result and len(result) > 0:
            sorted_result = sorted(result[0], key=lambda x: x[0][0][1])
            logging.info(f"OCR thành công với {len(sorted_result)} dòng.")
            return sorted_result
        else:
            logging.warning("Không tìm thấy văn bản nào.")
            return None
    except Exception as e:
        logging.error(f"Lỗi trong quá trình OCR: {e}")
        return None

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
        text = line[1][0].strip()
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

while True:
    ret, frame = cap.read()
    if not ret:
        print("Đã đến cuối video hoặc không thể đọc khung hình.")
        break

    results = model.predict(source=frame, show=False, conf=0.25)

    max_confidence = 0
    best_box = None

    for box in results[0].boxes:
        confidence = box.conf[0]
        if confidence > max_confidence and confidence > confidence_threshold:
            max_confidence = confidence
            best_box = box

    if best_box is not None:
        x1, y1, x2, y2 = map(int, best_box.xyxy[0])

        x1 = max(x1 - padding, 0)
        y1 = max(y1 - padding, 0)
        x2 = min(x2 + padding, frame.shape[1])
        y2 = min(y2 + padding, frame.shape[0])

        detected_object = frame[y1:y2, x1:x2]

        filename = time.strftime(r"D:\Edu\Python\StudentID_FaceVerification\student-id-face-matching\test\output\best_detected_object_%Y%m%d%H%M%S.jpg")
        cv2.imwrite(filename, detected_object)
        print(f"Ảnh đã được lưu tại: {filename} với độ tương đồng {max_confidence:.2f}")

        ocr_result = perform_ocr(filename)
        if ocr_result:
            extracted_info = extract_info_from_ocr(ocr_result)
            print(f"Kết quả OCR: {extracted_info}")

    annotated_frame = results[0].plot()
    cv2.imshow("YOLO Video Detection", annotated_frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord('p'):
        print("Đang dừng video... Nhấn phím bất kỳ để tiếp tục.")
        cv2.waitKey(0)
        cv2.imshow("OCR Result", frame)

cap.release()
cv2.destroyAllWindows()
