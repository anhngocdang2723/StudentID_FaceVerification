from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from paddleocr import PaddleOCR
import cv2
import re
import os

# Import preprocess_image từ file image_processing.py
from image_processing import preprocess_image

app = FastAPI()

ocr = PaddleOCR(use_angle_cls=True, lang='vi')

# Lấy file path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
RESULTS_FOLDER = os.path.join(BASE_DIR, "results")
STATIC_FOLDER = os.path.join(BASE_DIR, "static")

# Tạo file path nếu chưa tồn tại
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULTS_FOLDER, exist_ok=True)
os.makedirs(STATIC_FOLDER, exist_ok=True)

app.mount("/api/static", StaticFiles(directory=STATIC_FOLDER), name="static")

@app.get("/", response_class=HTMLResponse)
async def get_home():
    with open(os.path.join(STATIC_FOLDER, "index.html"), "r", encoding="utf-8") as f:
        html_content = f.read()
    return HTMLResponse(content=html_content)

def extract_info_from_ocr(result):
    fields = {
        "Tên": "",
        "Ngành": "",
        "Khoa/Viện": "",
        "Khoá": "",
        "MSV": ""
    }

    # Được sắp xếp theo tọa độ y (trên xuống)
    sorted_result = sorted(result[0], key=lambda x: x[0][0][1])

    next_line_is_name = False
    found_msv = False

    for line in sorted_result:
        text = line[1][0].strip()
        if "THE SINH VIEN" in text.upper():
            next_line_is_name = True
            continue
        if next_line_is_name:
            fields["Tên"] = text
            next_line_is_name = False
        if not found_msv and "MSV" in text.upper():
            msv_match = re.search(r"\d{9,}", text)
            if msv_match:
                fields["MSV"] = msv_match.group(0)
            found_msv = True
        if "NGANH" in text.upper() or "C." in text.upper():
            fields["Ngành"] = text
        if "VIEN" in text.upper():
            fields["Khoa/Viện"] = text
        if re.search(r"\d{4}-\d{4}", text):
            fields["Khoá"] = text
    return fields

# Hàm so sánh với danh sách đã trích xuất
def compare_with_list(student_info, extracted_list):
    for entry in extracted_list:
        name, msv = entry.split(" - ")
        if student_info['Tên'].strip().lower() == name.strip().lower() and student_info['MSV'] == msv.strip():
            return f"Sinh viên {student_info['Tên']} có mặt trong danh sách phòng thi."
    return f"Sinh viên {student_info['Tên']} không có mặt trong danh sách phòng thi."

# Đọc danh sách từ file đã lưu
def read_extracted_list(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            extracted_list = f.readlines()
        return [entry.strip() for entry in extracted_list]  # Xóa ký tự newline và khoảng trắng thừa
    except FileNotFoundError:
        print(f"File {file_path} không tồn tại.")
        return []

# Endpoint để xử lý ảnh và thực hiện OCR
@app.post("/api/upload-image")
async def upload_image(file: UploadFile = File(...)):
    # Lưu file ảnh vào thư mục uploads
    file_location = os.path.join(UPLOAD_FOLDER, file.filename)
    with open(file_location, "wb") as f:
        f.write(file.file.read())

    # Tiền xử lý ảnh
    processed_image_path = preprocess_image(file_location)

    # OCR: Nhận diện văn bản từ ảnh đã tiền xử lý
    result = ocr.ocr(processed_image_path, cls=True)

    # Trích xuất thông tin từ kết quả OCR
    extracted_info = extract_info_from_ocr(result)

    # Lưu thông tin vào student_info
    student_info = {
        "Tên": extracted_info["Tên"],
        "MSV": extracted_info["MSV"]
    }

    # Đọc danh sách từ file đã lưu
    file_path = r'D:\Edu\Python\StudentID_FaceVerification\student-id-face-matching\api\List of candidates\extracted_list\student_list_from_excel.txt'
    extracted_list = read_extracted_list(file_path)

    # So sánh và in kết quả
    if extracted_list:
        result = compare_with_list(student_info, extracted_list)
        return {
            "message": "OCR thành công",
            "extracted_info": extracted_info,
            "comparison_result": result
        }
    else:
        return {
            "message": "Không thể đọc danh sách sinh viên.",
            "extracted_info": extracted_info
        }
