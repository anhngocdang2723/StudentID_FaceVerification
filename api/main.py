#region Import Libraries
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from werkzeug.utils import secure_filename
import os
import logging
import cv2

from image_processing import preprocess_image
from ocr_processing import perform_ocr, extract_info_from_ocr
from face_extraction import process_student_id
from face_comparison import compare_faces
from excel_reader_byPandas import read_from_excel
from compare_student import compare_with_student_list
from generate_exam_ticket import generate_exam_ticket_pdf
#endregion

#region functions
app = FastAPI()
students_list: List[dict] = []
#endregion

#region folder path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FE_FOLDER = os.path.join(BASE_DIR, r"D:\\Edu\\Python\\StudentID_FaceVerification\\student-id-face-matching\\frontend")
UPLOAD_FOLDER = os.path.join(BASE_DIR, r"D:\\Edu\\Python\\StudentID_FaceVerification\\student-id-face-matching\\uploads\\user_uploads")
RESULTS_FOLDER = os.path.join(BASE_DIR, r"D:\\Edu\\Python\\StudentID_FaceVerification\\student-id-face-matching\\results")
FACES_FOLDER = os.path.join(RESULTS_FOLDER, "student_card_faces")
# EXAM_TICKET_DIR = os.path.join(BASE_DIR, "tickets")

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULTS_FOLDER, exist_ok=True)
os.makedirs(FACES_FOLDER, exist_ok=True)

app.mount("/api/css", StaticFiles(directory=os.path.join(FE_FOLDER, "css")), name="css")
app.mount("/api/js", StaticFiles(directory=os.path.join(FE_FOLDER, "js")), name="js")
app.mount("/api/static", StaticFiles(directory=os.path.join(FE_FOLDER, "static")), name="static")
# app.mount("/tickets", StaticFiles(directory="tickets"), name="tickets")
#endregion

#region CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],  #Spring Boot port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
#endregion

@app.get("/", response_class=HTMLResponse)
async def get_home():
    with open(os.path.join(FE_FOLDER, "index.html"), "r", encoding="utf-8") as f:
        html_content = f.read()
    return HTMLResponse(content=html_content)

@app.post("/api/read-excel", tags=["Excel Processing"])
async def read_excel(file: UploadFile = File(...)):
    global students_list

    if file:
        if file.content_type != "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
            raise HTTPException(status_code=400, detail="Chỉ hỗ trợ định dạng file Excel (XLSX).")
        try:
            file_location = os.path.join(UPLOAD_FOLDER, file.filename)
            contents = await file.read()
            with open(file_location, "wb") as f:
                f.write(contents)
            print(f"File đã được lưu tại: {file_location}")

            excel_data = read_from_excel(file_location)
            # print(excel_data) # Log dữ liệu sinh viên
            if excel_data:
                students_list = excel_data
                # print("Dữ liệu sinh viên đã được lưu vào biến tạm thành công.", students_list) # Log dữ liệu sinh viên
                return {"students": excel_data}
            else:
                raise HTTPException(status_code=400, detail="Không đọc được dữ liệu từ file Excel. Kiểm tra cấu trúc file.")
        except Exception as e:
            logging.error(f"Error processing Excel file: {e}")
            raise HTTPException(status_code=500, detail="Có lỗi xảy ra khi xử lý file Excel.")
    else:
        raise HTTPException(status_code=400, detail="Không có file nào được nhận.")

# @app.post("/api/upload-image", tags=["Image Processing"])
# async def upload_image(file: UploadFile = File(...)):
    if file:
        if file.content_type not in ["image/jpeg", "image/png"]:
            raise HTTPException(status_code=400, detail="Chỉ hỗ trợ các định dạng file JPEG và PNG.")
        try:
            file_location = os.path.join(UPLOAD_FOLDER, file.filename)
            contents = await file.read()
            with open(file_location, "wb") as f:
                f.write(contents)
            processed_image_path = preprocess_image(file_location)
            ocr_result = perform_ocr(processed_image_path)
            extracted_info = extract_info_from_ocr(ocr_result) if ocr_result else None
            face_image_base64 = process_student_id(file_location)
            uploaded_image = cv2.imread(file_location)
            comparison_result = compare_faces(uploaded_image, face_image_base64)

            if isinstance(extracted_info, dict) and compare_with_student_list(extracted_info, students_list):
                student_verification_status = "Thông tin sinh viên khớp với danh sách."
                ticket_result = generate_exam_ticket_pdf(
                    extracted_info['Tên'], extracted_info['MSV'], "Thi giac may tinh", "62 (2021-2026)", 10
                )
                ticket_path = ticket_result["ticket_file"]
            else:
                student_verification_status = "Thông tin sinh viên không khớp với danh sách."
                ticket_path = None

            return {
                "Thông báo": "Xử lý ảnh thành công.",
                "Thông tin trích xuất được": extracted_info,
                # "Trạng thái xác thực": student_verification_status,
                "Phiếu thi": ticket_path,
                "comparison": comparison_result,
                "face_image": face_image_base64
            }
        except Exception as e:
            logging.error(f"Error processing file: {e}")
            raise HTTPException(status_code=500, detail="Có lỗi xảy ra khi xử lý ảnh.")
    else:
        raise HTTPException(status_code=400, detail="Không có file nào được nhận.")

@app.post("/api/upload-image", tags=["Processing"])
async def upload_image(file: UploadFile = File(...)):
    if not file:
        raise HTTPException(status_code=400, detail="Không có file nào được nhận.")

    if file.content_type not in ["image/jpeg", "image/png"]:
        raise HTTPException(status_code=400, detail="Chỉ hỗ trợ các định dạng file JPEG và PNG.")

    file.filename = secure_filename(file.filename)
    file_location = os.path.join(UPLOAD_FOLDER, file.filename)

    try:
        # Lưu file tạm thời
        contents = await file.read()
        with open(file_location, "wb") as f:
            f.write(contents)

        # Xử lý ảnh và OCR
        processed_image_path = preprocess_image(file_location)
        ocr_result = perform_ocr(processed_image_path)
        extracted_info = extract_info_from_ocr(ocr_result) if ocr_result else None

        # So sánh khuôn mặt
        face_image_base64 = process_student_id(file_location)
        uploaded_image = cv2.imread(file_location)
        comparison_result = compare_faces(uploaded_image, face_image_base64)

        # Xác thực sinh viên
        if isinstance(extracted_info, dict) and compare_with_student_list(extracted_info, students_list):
            student_verification_status = "Thông tin sinh viên khớp với danh sách."
            ticket_result = generate_exam_ticket_pdf(
                extracted_info['Tên'], extracted_info['MSV'], "Thi giac may tinh", "62 (2021-2026)", 10
            )
            ticket_path = ticket_result["ticket_file"]
            ticket_info = ticket_result.get("ticket_info", {})
        else:
            student_verification_status = "Thông tin sinh viên không khớp với danh sách."
            ticket_path = None
            ticket_info = {}

        # Trả kết quả
        return {
            "Thông báo": "Xử lý ảnh thành công.",
            "Thông tin trích xuất được": extracted_info,
            "Trạng thái xác thực": student_verification_status,
            "Kết quả so sánh khuôn mặt": comparison_result,
            "Phiếu thi": {
                "file_path": ticket_path,
                "ticket_info": ticket_info
            },
            "Hình ảnh khuôn mặt (base64)": face_image_base64
        }
    except Exception as e:
        logging.error(f"Error processing file {file.filename}: {e}")
        raise HTTPException(status_code=500, detail="Có lỗi xảy ra khi xử lý ảnh.")
    finally:
        # Xóa file tạm
        if os.path.exists(file_location):
            os.remove(file_location)

@app.get("/api/serve-ticket/{student_msv}")
async def serve_ticket(student_msv: str):
    ticket_filename = f"{student_msv}_exam_ticket.pdf"
    ticket_path = os.path.join("tickets", ticket_filename)

    if not os.path.exists(ticket_path):
        raise HTTPException(status_code=404, detail="Không tìm thấy phiếu thi cho sinh viên này.")

    return {"message": "Phiếu thi đã được tạo", "ticket_url": f"/tickets/{ticket_filename}"}
