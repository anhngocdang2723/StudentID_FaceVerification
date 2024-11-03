from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import os
import logging

from image_processing import preprocess_image
from ocr_processing import perform_ocr, extract_info_from_ocr
from face_extraction import process_student_id
#from camera_detection import detect_card_from_camera
app = FastAPI()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FE_FOLDER = os.path.join(BASE_DIR, r"D:\\Edu\\Python\\StudentID_FaceVerification\\student-id-face-matching\\frontend")  # Chỉ định tới thư mục FE
UPLOAD_FOLDER = os.path.join(BASE_DIR, r"D:\\Edu\\Python\\StudentID_FaceVerification\\student-id-face-matching\\uploads\\user_uploads")
RESULTS_FOLDER = os.path.join(BASE_DIR, r"D:\\Edu\\Python\\StudentID_FaceVerification\\student-id-face-matching\\results")
FACES_FOLDER = os.path.join(RESULTS_FOLDER, "student_card_faces")

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULTS_FOLDER, exist_ok=True)
os.makedirs(FACES_FOLDER, exist_ok=True)

# Cấu hình CORS cho phép truy cập từ Spring Boot
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],  # Cổng chạy Spring Boot
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount thư mục tĩnh
app.mount("/api/css", StaticFiles(directory=os.path.join(FE_FOLDER, "css")), name="css")
app.mount("/api/js", StaticFiles(directory=os.path.join(FE_FOLDER, "js")), name="js")
app.mount("/api/static", StaticFiles(directory=os.path.join(FE_FOLDER, "static")), name="static")

@app.get("/", response_class=HTMLResponse)
async def get_home():
    with open(os.path.join(FE_FOLDER, "index.html"), "r", encoding="utf-8") as f:
        html_content = f.read()
    return HTMLResponse(content=html_content)

@app.post("/api/upload-image")
async def upload_image(file: UploadFile = File(...)):
    if file:
        try:
            file_location = os.path.join(UPLOAD_FOLDER, file.filename)

            # Lưu tệp hình ảnh tải lên
            with open(file_location, "wb") as f:
                f.write(file.file.read())

            processed_image_path = preprocess_image(file_location)  # Hàm xử lý ảnh khác, nếu cần
            ocr_result = perform_ocr(processed_image_path)         # Hàm thực hiện OCR

            if ocr_result:
                extracted_info = extract_info_from_ocr(ocr_result)  # Trích xuất thông tin từ OCR
            else:
                extracted_info = "OCR thất bại hoặc không có thông tin."

            face_image_base64 = process_student_id(file_location)    # Cắt khuôn mặt và trả về base64

            if face_image_base64:
                return {
                    "Thông báo": "Khuôn mặt và OCR được xử lý thành công.",
                    "Thông tin trích xuất được": extracted_info,
                    "face_image": face_image_base64  # Trả về ảnh khuôn mặt dưới dạng base64
                }
            else:
                return {
                    "Thông báo": "Không tìm thấy khuôn mặt, nhưng đã thực hiện OCR.",
                    "Thông tin trích xuất được": extracted_info
                }
        except Exception as e:
            logging.error(f"Error processing file: {e}")
            return {"Thông báo": "Có lỗi xảy ra khi xử lý ảnh."}, 500
    else:
        return {"Thông báo": "Không có file nào được nhận."}, 400

# @app.get("/api/detect-card")
# async def detect_card():
#     return await detect_card_from_camera()

# ################# test api ########################
# from pydantic import BaseModel
# class TextInput(BaseModel):
#     text: str
# @app.post("/api/print")
# async def print_text(text_input: TextInput):
#     # Phản hồi lại nội dung nhận được từ frontend
#     return {"received_text": text_input.text}
# ###################################################

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