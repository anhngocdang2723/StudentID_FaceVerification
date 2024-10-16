from paddleocr import PaddleOCR
import re
import logging

ocr = PaddleOCR(use_angle_cls=True, lang='vi')

logging.basicConfig(level=logging.INFO)

def perform_ocr(image_path): #hàm ocr và sắp xếp kết quả
    try:
        result = ocr.ocr(image_path, cls=True)
        if result and len(result) > 0:
            sorted_result = sorted(result[0], key=lambda x: x[0][0][1])  # Sắp xếp theo tọa độ y của dòng văn bản
            logging.info(f"OCR thành công với {len(sorted_result)} dòng.")
            return sorted_result
        else:
            logging.warning("Không tìm thấy văn bản nào.")
            return None
    except Exception as e:
        logging.error(f"Lỗi trong quá trình OCR: {e}")
        return None

def extract_info_from_ocr(result): #hàm trích xuất thông tin từ kết quả đã sắp xếp
    fields = {
        "Tên": "",
        "Ngành": "",
        "Trường/Khoa/Viện": "",
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
            fields["Trường/Khoa/Viện"] = text
            next_line_is_faculty = False
            continue
        if re.search(r"\d{4}-\d{4}", text):
            fields["Khoá"] = text

    logging.info(f"Thông tin trích xuất: {fields}")
    return fields
