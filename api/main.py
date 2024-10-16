from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import os
import logging
from image_processing import preprocess_image  # Hàm xử lý ảnh trong module riêng
from ocr_processing import perform_ocr, extract_info_from_ocr  # Import từ module ocr_processing
from face_extraction import process_student_id  # Hàm xử lý ảnh trong module riêng
app = FastAPI()

# Cấu hình thư mục
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
RESULTS_FOLDER = os.path.join(BASE_DIR, "results")
FACES_FOLDER = os.path.join(RESULTS_FOLDER, "student_card_faces")
#CARDS_FOLDER = os.path.join(RESULTS_FOLDER, "student_card")
STATIC_FOLDER = os.path.join(BASE_DIR, "static")

# Tạo các thư mục nếu chưa có
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULTS_FOLDER, exist_ok=True)
os.makedirs(FACES_FOLDER, exist_ok=True)
#os.makedirs(CARDS_FOLDER, exist_ok=True)
os.makedirs(STATIC_FOLDER, exist_ok=True)

# Mount thư mục static
app.mount("/api/static", StaticFiles(directory=STATIC_FOLDER), name="static")

@app.get("/", response_class=HTMLResponse)
async def get_home():
    # Trả về trang chủ từ thư mục static
    with open(os.path.join(STATIC_FOLDER, "index.html"), "r", encoding="utf-8") as f:
        html_content = f.read()
    return HTMLResponse(content=html_content)

def read_extracted_list(file_path):
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

@app.post("/api/upload-image")
async def upload_image(file: UploadFile = File(...)):

    file_location = os.path.join(UPLOAD_FOLDER, file.filename)
    output_face_path = os.path.join(FACES_FOLDER, f"{file.filename}_face.jpg")

    with open(file_location, "wb") as f:
        f.write(file.file.read())

    # Gọi hàm process_student_id để phát hiện và cắt khuôn mặt
    if process_student_id(file_location, output_face_path):
        # Thực hiện tiền xử lý ảnh trước khi OCR
        processed_image_path = preprocess_image(file_location)

        # Thực hiện OCR trên ảnh đã xử lý
        ocr_result = perform_ocr(processed_image_path)

        if ocr_result:
            # Trích xuất thông tin từ kết quả OCR
            extracted_info = extract_info_from_ocr(ocr_result)

            return {
                "Thông báo": "OCR thành công",
                "Thông tin trích xuất được": extracted_info
            }
        else:
            return {"Thông báo": "OCR thất bại."}
    else:
        return {"Thông báo": "Không tìm thấy khuôn mặt."}