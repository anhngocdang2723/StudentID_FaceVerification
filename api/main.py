#region Import Libraries
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import os
import logging
import cv2

from image_processing import preprocess_image
from ocr_processing import perform_ocr, extract_info_from_ocr
from face_extraction import process_student_id
from face_comparison import compare_faces
from excel_reader_byPandas import read_from_excel
#endregion

#region functions
app = FastAPI()
students_list = []
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

def compare_with_student_list(student_info, students_list):
    for entry in students_list:
        name = entry['Tên']
        msv = entry['MSV']
        # So sánh Tên và MSV, không phân biệt chữ hoa và chữ thường
        if student_info['Tên'].strip().lower() == name.strip().lower() and student_info['MSV'] == msv.strip():
            return True
    return False

@app.post("/api/upload-image", tags=["Image Processing"])
async def upload_image(file: UploadFile = File(...)):
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

            if ocr_result:
                extracted_info = extract_info_from_ocr(ocr_result)
            else:
                extracted_info = "OCR thất bại hoặc không có thông tin."

            face_image_base64 = process_student_id(file_location)

            uploaded_image = cv2.imread(file_location)
            comparison_result = compare_faces(uploaded_image, face_image_base64)
            print("Kết quả so sánh:", comparison_result) #in ra console để test kết quả so sánh
            # print(f"Chuỗi Base64 có chiều dài: {len(face_image_base64)}")
            
            if face_image_base64:
                return {
                    "Thông báo": "Khuôn mặt và OCR được xử lý thành công.",
                    "Thông tin trích xuất được": extracted_info,
                    "comparison": comparison_result,
                    "face_image": face_image_base64
                }
            else:
                return {
                    "Thông báo": "Không tìm thấy khuôn mặt, nhưng đã thực hiện OCR.",
                    "Thông tin trích xuất được": extracted_info
                }
                
        except FileNotFoundError:
            logging.error(f"File not found: {file_location}")
            raise HTTPException(status_code=404, detail="Không tìm thấy file đã tải lên.")

        except Exception as e:
            logging.error(f"Error processing file: {e}")
            raise HTTPException(status_code=500, detail="Có lỗi xảy ra khi xử lý ảnh.")
    
    else:
        raise HTTPException(status_code=400, detail="Không có file nào được nhận.")

@app.post("/api/read-excel", tags=["Excel Processing"])
async def read_excel(file: UploadFile = File(...)):
    if file:
        if file.content_type != "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
            raise HTTPException(status_code=400, detail="Chỉ hỗ trợ định dạng file Excel (XLSX).")

        try:
            # Lưu file Excel tạm thời
            file_location = os.path.join(UPLOAD_FOLDER, file.filename)
            contents = await file.read()
            with open(file_location, "wb") as f:
                f.write(contents)
            print(f"File đã được lưu tại: {file_location}")

            # Đọc dữ liệu từ file Excel bằng module `excel_reader_byPandas`
            excel_data = read_from_excel(file_location)
            print(excel_data)
            if excel_data:
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
#     if file:
#         if file.content_type not in ["image/jpeg", "image/png"]:
#             raise HTTPException(status_code=400, detail="Chỉ hỗ trợ các định dạng file JPEG và PNG.")
        
#         try:
#             # Lưu file ảnh vào thư mục tạm
#             file_location = os.path.join(UPLOAD_FOLDER, file.filename)
#             contents = await file.read()
#             with open(file_location, "wb") as f:
#                 f.write(contents)
            
#             # Tiền xử lý ảnh
#             processed_image_path = preprocess_image(file_location)
#             ocr_result = perform_ocr(processed_image_path)
            
#             if not ocr_result:
#                 raise HTTPException(status_code=400, detail="OCR thất bại hoặc không có thông tin.")

#             extracted_info = extract_info_from_ocr(ocr_result)
#             if not extracted_info:
#                 raise HTTPException(status_code=400, detail="Không trích xuất được thông tin từ OCR.")

#             # Xử lý và so sánh khuôn mặt
#             face_image_base64 = process_student_id(file_location)
#             uploaded_image = cv2.imread(file_location)
#             comparison_result = compare_faces(uploaded_image, face_image_base64)

#             if comparison_result != "Matched":
#                 logging.error(f"Error comparing faces: {comparison_result}")
#                 raise HTTPException(status_code=400, detail="Khuôn mặt không khớp hoặc không xác định được.")
            
#             # So sánh thông tin OCR với danh sách sinh viên
#             if not compare_with_student_list(extracted_info, students_list):
#                 raise HTTPException(status_code=400, detail="Thông tin không khớp với danh sách sinh viên.")
            
#             return {
#                 "Thông báo": "Khuôn mặt và OCR được xử lý, so sánh thành công.",
#                 "Thông tin trích xuất được": extracted_info,
#                 "comparison": comparison_result,
#                 "face_image": face_image_base64
#             }
        
#         except Exception as e:
#             logging.error(f"Error processing file: {e}")
#             raise HTTPException(status_code=500, detail="Có lỗi xảy ra khi xử lý ảnh.")


# @app.post("/api/read-excel", tags=["Excel Processing"])
# async def read_excel(file: UploadFile = File(...)):
    global students_list  # Sử dụng biến toàn cục
    if file:
        if file.content_type != "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
            raise HTTPException(status_code=400, detail="Chỉ hỗ trợ định dạng file Excel (XLSX).")

        try:
            # Lưu file Excel tạm thời
            file_location = os.path.join(UPLOAD_FOLDER, file.filename)
            contents = await file.read()
            with open(file_location, "wb") as f:
                f.write(contents)
            print(f"File đã được lưu tại: {file_location}")

            # Đọc dữ liệu từ file Excel
            excel_data = read_from_excel(file_location)
            print(excel_data)

            if excel_data:
                # Lưu vào biến tạm
                students_list = excel_data
                return {"message": "Dữ liệu sinh viên đã được lưu vào biến tạm thành công.", "students": excel_data}
            else:
                raise HTTPException(status_code=400, detail="Không đọc được dữ liệu từ file Excel. Kiểm tra cấu trúc file.")
        
        except Exception as e:
            logging.error(f"Error processing Excel file: {e}")
            raise HTTPException(status_code=500, detail="Có lỗi xảy ra khi xử lý file Excel.")
    else:
        raise HTTPException(status_code=400, detail="Không có file nào được nhận.")
    
# Hàm kiểm tra sinh viên và so sánh thông tin phòng thi (có thể giữ nguyên)
# def read_extracted_list(file_path):  # Sẽ update đọc từ database sau
#     try:
#         with open(file_path, 'r', encoding='utf-8') as f:
#             extracted_list = f.readlines()
#         return [entry.strip() for entry in extracted_list]
#     except FileNotFoundError:
#         return []

# @app.get("/api/check-exam-list", tags=["Exam Verification"])
# async def check_exam_list(student_name: str, student_id: str):
#     student_info = {
#         "Tên": student_name,
#         "MSV": student_id
#     }
#     return compare_with_list(student_info, students_list)
