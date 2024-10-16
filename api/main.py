from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import os
import logging
from image_processing import preprocess_image
from ocr_processing import perform_ocr, extract_info_from_ocr
from face_extraction import process_student_id
app = FastAPI()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
RESULTS_FOLDER = os.path.join(BASE_DIR, "results")
FACES_FOLDER = os.path.join(RESULTS_FOLDER, "student_card_faces")
STATIC_FOLDER = os.path.join(BASE_DIR, "static")

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULTS_FOLDER, exist_ok=True)
os.makedirs(FACES_FOLDER, exist_ok=True)
os.makedirs(STATIC_FOLDER, exist_ok=True)

# Mount thư mục static
app.mount("/api/static", StaticFiles(directory=STATIC_FOLDER), name="static")

@app.get("/", response_class=HTMLResponse)
async def get_home():
    # Trả về trang chủ từ thư mục static
    with open(os.path.join(STATIC_FOLDER, "index.html"), "r", encoding="utf-8") as f:
        html_content = f.read()
    return HTMLResponse(content=html_content)

@app.post("/api/upload-image")
async def upload_image(file: UploadFile = File(...)):
    file_location = os.path.join(UPLOAD_FOLDER, file.filename)
    output_face_path = os.path.join(FACES_FOLDER, f"{file.filename}_face.jpg")

    with open(file_location, "wb") as f:
        f.write(file.file.read())

    if process_student_id(file_location, output_face_path):
        processed_image_path = preprocess_image(file_location)
        ocr_result = perform_ocr(processed_image_path)

        if ocr_result:
            extracted_info = extract_info_from_ocr(ocr_result)
            return {
                "Thông báo": "OCR thành công",
                "Thông tin trích xuất được": extracted_info
            }
        else:
            return {"Thông báo": "OCR thất bại."}
    else:
        return {"Thông báo": "Không tìm thấy khuôn mặt."}


########################### Các hàm kiểm tra sinh viên #######################
def read_extracted_list(file_path): ### Sẽ update đọc từ database ###
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            extracted_list = f.readlines()
        return [entry.strip() for entry in extracted_list]  # Xóa ký tự xuống dòng
    except FileNotFoundError:
        return []

def compare_with_list(student_info, extracted_list):
    for entry in extracted_list:
        name, msv = entry.split(" - ")
        if student_info['Tên'].strip().lower() == name.strip().lower() and student_info['MSV'] == msv.strip():
            return f"Sinh viên: {student_info['Tên']} có mặt trong danh sách phòng thi."
    return f"Sinh viên: {student_info['Tên']} không có mặt trong danh sách phòng thi."

@app.get("/api/check-exam-list")
async def check_exam_list(student_name: str, student_id: str):
    extracted_list = read_extracted_list("extracted_list.txt")
    student_info = {
        "Tên": student_name,
        "MSV": student_id
    }
    return compare_with_list(student_info, extracted_list)
#######################################################################################
