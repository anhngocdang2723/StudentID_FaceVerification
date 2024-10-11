from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from paddleocr import PaddleOCR
import cv2
import re
import os

from face_extraction import process_student_id

app = FastAPI()

ocr = PaddleOCR(use_angle_cls=True, lang='vi')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
RESULTS_FOLDER = os.path.join(BASE_DIR, "results")
FACES_FOLDER = os.path.join(RESULTS_FOLDER, "student_card_faces")
CARDS_FOLDER = os.path.join(RESULTS_FOLDER, "student_card")
STATIC_FOLDER = os.path.join(BASE_DIR, "static")

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
        "Trường/Khoa/Viện": "",
        "Khoá": "",
        "MSV": ""
    }

    sorted_result = sorted(result[0], key=lambda x: x[0][0][1])

    next_line_is_name = False  # flag tìm tên
    next_line_is_major = False  # flag tìm ngành
    next_line_is_faculty = False  # flag tìm trường/khoa/viện
    found_msv = False  # flag tìm MSV

    for line in sorted_result:
        text = line[1][0].strip()
        if "THE SINH VIEN" in text.upper():
            next_line_is_name = True
            continue
        if next_line_is_name:
            fields["Tên"] = text
            next_line_is_name = False  # reset flag sau khi tìm thấy tên
            next_line_is_major = True
            continue
        if not found_msv and "MSV" in text.upper():
            msv_match = re.search(r"\\d{9,}", text)
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
        if re.search(r"\\d{4}-\\d{4}", text):  # tìm năm học có dạng xxxx-xxxx
            fields["Khoá"] = text
    return fields

def compare_with_list(student_info, extracted_list):
    for entry in extracted_list:
        name, msv = entry.split(" - ")
        if student_info['Tên'].strip().lower() == name.strip().lower() and student_info['MSV'] == msv.strip():
            return f"Sinh viên: {student_info['Tên']} có mặt trong danh sách phòng thi."
    return f"Sinh viên: {student_info['Tên']} không có mặt trong danh sách phòng thi."

def read_extracted_list(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            extracted_list = f.readlines()
        return [entry.strip() for entry in extracted_list]  # Xóa ký tự newline và khoảng trắng thừa
    except FileNotFoundError:
        print(f"File {file_path} không tồn tại.")
        return []

@app.post("/api/upload-image")
async def upload_image(file: UploadFile = File(...)):

    file_location = os.path.join(UPLOAD_FOLDER, file.filename)
    with open(file_location, "wb") as f:
        f.write(file.file.read())

    output_face_path = os.path.join(FACES_FOLDER, f"{file.filename}_face.jpg")
    output_processed_path = os.path.join(CARDS_FOLDER, f"{file.filename}_processed.jpg")

    if process_student_id(file_location, output_face_path, output_processed_path):
        result = ocr.ocr(output_processed_path, cls=True)

        extracted_info = extract_info_from_ocr(result)

        student_info = {
            "Tên": extracted_info["Tên"],
            "MSV": extracted_info["MSV"]
        }

        file_path = r'D:\Edu\Python\StudentID_FaceVerification\student-id-face-matching\api\List of candidates\extracted_list\student_list_from_excel.txt'
        extracted_list = read_extracted_list(file_path)

        if extracted_list:
            comparison_result = compare_with_list(student_info, extracted_list)
            return {
                "Thông báo": "OCR thành công",
                "Thông tin trích xuất được": extracted_info,
                "Kết quả đối chiếu": comparison_result,
                #"Hình ảnh khuôn mặt": output_face_path,  # Trả về đường dẫn ảnh khuôn mặt
                #"Hình ảnh đã xử lý": output_processed_path  # Trả về đường dẫn ảnh đã xử lý
            }
        else:
            return {
                "Thông báo": "Không thể đọc danh sách sinh viên.",
            }
    else:
        return {
            "Thông báo": "Không thể xử lý ảnh.",
        }
