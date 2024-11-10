#region Import Libraries
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import os
import logging
import cv2

from image_processing import preprocess_image
from ocr_processing import perform_ocr, extract_info_from_ocr
from face_extraction import process_student_id
from face_comparison import compare_faces
from excel_reader_byPandas import read_from_excel
from compare_student import compare_with_student_list
from generate_exam_ticket import generate_exam_ticket
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

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULTS_FOLDER, exist_ok=True)
os.makedirs(FACES_FOLDER, exist_ok=True)

app.mount("/api/css", StaticFiles(directory=os.path.join(FE_FOLDER, "css")), name="css")
app.mount("/api/js", StaticFiles(directory=os.path.join(FE_FOLDER, "js")), name="js")
app.mount("/api/static", StaticFiles(directory=os.path.join(FE_FOLDER, "static")), name="static")
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
    global students_list  # Khai báo biến global
    
    if file:
        if file.content_type != "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
            raise HTTPException(status_code=400, detail="Chỉ hỗ trợ định dạng file Excel (XLSX).")
        try:
            file_location = os.path.join(UPLOAD_FOLDER, file.filename) # Lưu file tạm thời
            contents = await file.read()
            with open(file_location, "wb") as f:
                f.write(contents)
            print(f"File đã được lưu tại: {file_location}")

            excel_data = read_from_excel(file_location)
            print(excel_data)
            if excel_data:
                students_list = excel_data      # Lưu dữ liệu vào biến global students_list
                print("Dữ liệu sinh viên đã được lưu vào biến tạm thành công.", students_list)
                return {"students": excel_data}
            else:
                raise HTTPException(status_code=400, detail="Không đọc được dữ liệu từ file Excel. Kiểm tra cấu trúc file.")
        except Exception as e:
            logging.error(f"Error processing Excel file: {e}")
            raise HTTPException(status_code=500, detail="Có lỗi xảy ra khi xử lý file Excel.")
    else:
        raise HTTPException(status_code=400, detail="Không có file nào được nhận.")

@app.post("/api/upload-image", tags=["Image Processing"])
async def upload_image(file: UploadFile = File(...)):
    if file:
        if file.content_type not in ["image/jpeg", "image/png"]:
            raise HTTPException(status_code=400, detail="Chỉ hỗ trợ các định dạng file JPEG và PNG.")
        try:
            file_location = os.path.join(UPLOAD_FOLDER, file.filename)  # Lưu file tạm thời
            contents = await file.read()
            with open(file_location, "wb") as f:
                f.write(contents)
            processed_image_path = preprocess_image(file_location)
            ocr_result = perform_ocr(processed_image_path)
            if ocr_result:
                extracted_info = extract_info_from_ocr(ocr_result)
                # print("Thông tin trích xuất từ OCR:", extracted_info)  # Log giá trị trích xuất
            else:
                extracted_info = None  # Lỗi không OCR được
            face_image_base64 = process_student_id(file_location)
            uploaded_image = cv2.imread(file_location)
            comparison_result = compare_faces(uploaded_image, face_image_base64)
            # print("Kết quả so sánh:", comparison_result)

            if isinstance(extracted_info, dict):  # So sánh OCR với students_list
                # print("Thông tin trích xuất từ OCR:", extracted_info)  # Log giá trị trích xuất
                if compare_with_student_list(extracted_info, students_list):
                    student_verification_status = "Thông tin sinh viên khớp với danh sách."
                    student_name = extracted_info['Tên']
                    student_msv = extracted_info['MSV']
                    exam_name = "Thi giac may tinh"  # Ví dụ, bạn có thể lấy từ cơ sở dữ liệu
                    exam_code = "62 (2021-2026)"  # Ví dụ
                    seat_position = 10  # Bạn có thể lấy vị trí ngồi từ cơ sở dữ liệu hoặc tính toán

                    # Gọi hàm tạo phiếu thi
                    ticket_path = generate_exam_ticket(student_name, student_msv, exam_name, exam_code, seat_position)
                else:
                    student_verification_status = "Thông tin sinh viên không khớp với danh sách."
            else:
                student_verification_status = "Không thể so sánh vì thông tin OCR không hợp lệ."
            
            if face_image_base64:
                return {
                    "Thông báo": "Khuôn mặt và OCR được xử lý thành công.",
                    "Thông tin trích xuất được": extracted_info,
                    # "Kết quả so sánh": comparison_result,
                    "comparison": comparison_result,
                    "Trạng thái xác thực": student_verification_status,
                    "face_image": face_image_base64,
                    "Phiếu thi": ticket_path if student_verification_status == "Thông tin sinh viên khớp với danh sách." else None
                }
            else:
                return {
                    "Thông báo": "Không tìm thấy khuôn mặt, nhưng đã thực hiện OCR.",
                    "Thông tin trích xuất được": extracted_info,
                    "Trạng thái xác thực": student_verification_status,
                    "Phiếu thi": ticket_path if student_verification_status == "Thông tin sinh viên khớp với danh sách." else None
                }
        except FileNotFoundError:
            logging.error(f"File not found: {file_location}")
            raise HTTPException(status_code=404, detail="Không tìm thấy file đã tải lên.")
        except Exception as e:
            logging.error(f"Error processing file: {e}")
            raise HTTPException(status_code=500, detail="Có lỗi xảy ra khi xử lý ảnh.")
    else:
        raise HTTPException(status_code=400, detail="Không có file nào được nhận.")
