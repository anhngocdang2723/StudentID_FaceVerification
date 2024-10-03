from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from paddleocr import PaddleOCR
import cv2
import re
import os
from pymongo import MongoClient

# Khởi tạo FastAPI
app = FastAPI()

# Khởi tạo PaddleOCR để đọc tiếng việt
ocr = PaddleOCR(use_angle_cls=True, lang='vi')

# Đường dẫn lưu trữ đến các thư mục chứa ảnh, ảnh đã xử lý và kết quả
UPLOAD_FOLDER = "uploads/"
PROCESSED_FOLDER = "processed/"
RESULTS_FOLDER = "results/"

# Kiểm tra và tạo thư mục nếu chưa tồn tại
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)
os.makedirs(RESULTS_FOLDER, exist_ok=True)

# Mount static files (CSS, JS, etc.)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Kết nối MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['student_database']  # Tên database
collection = db['student_cards']  # Tên collection

# Endpoints hiển thị web
@app.get("/", response_class=HTMLResponse)
async def get_home():
    with open("static/index.html", "r", encoding="utf-8") as f:
        html_content = f.read()
    return HTMLResponse(content=html_content)

# Tiền xử lý ảnh (grayscale và ngưỡng hóa)
def preprocess_image(image_path: str) -> str:
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)

    processed_image_path = os.path.join(PROCESSED_FOLDER, f"processed_{os.path.basename(image_path)}")
    cv2.imwrite(processed_image_path, thresh)
    return processed_image_path

# Trích xuất thông tin từ kết quả OCR
def extract_info_from_ocr(result):
    fields = {
        "Tên": "",
        "Ngành": "",
        "Khoa/Viện": "",
        "Khoá": "",
        "MSV": ""
    }

    # Sắp xếp kết quả theo thứ tự từ trên xuống dưới theo trục y
    sorted_result = sorted(result[0], key=lambda x: x[0][0][1])

    next_line_is_name = False
    found_msv = False

    for line in sorted_result:
        text = line[1][0].strip()

        # Kiểm tra từ khóa "Thẻ Sinh Viên"
        if "THE SINH VIEN" in text.upper():
            next_line_is_name = True
            continue

        # Nếu dòng tiếp theo sau "Thẻ Sinh Viên" thì có là tên
        if next_line_is_name:
            fields["Tên"] = text
            next_line_is_name = False

        # Trích xuất MSV
        if not found_msv and "MSV" in text.upper():
            msv_match = re.search(r"\d{9,}", text)
            if msv_match:
                fields["MSV"] = msv_match.group(0)
            found_msv = True

        # Trích xuất ngành học dựa trên từ khóa "Ngành"
        if "NGANH" in text.upper() or "C." in text.upper() in text.upper():
            fields["Ngành"] = text

        # Trích xuất Khoa/Viện dựa trên từ khóa "Khoa" hoặc "Viện"
        if "VIEN" in text.upper():
            fields["Khoa/Viện"] = text

        # Trích xuất Khoá học dựa trên định dạng "xxxx-xxxx"
        if re.search(r"\d{4}-\d{4}", text):
            fields["Khoá"] = text

    return fields

# Lưu kết quả vào file TXT
def save_results_to_txt(filename, extracted_info):
    result_file = os.path.join(RESULTS_FOLDER, f"{filename}_result.txt")
    with open(result_file, "w", encoding="utf-8") as f:
        for field, value in extracted_info.items():
            f.write(f"{field}: {value}\n")
    return result_file

# Lưu kết quả vào MongoDB
def save_results_to_db(extracted_info):
    collection.insert_one(extracted_info)
    print("Đã lưu kết quả vào MongoDB thành công")

# Endpoint để xử lý ảnh và thực hiện OCR
@app.post("/upload-image")
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

    # Lưu kết quả vào file TXT và MongoDB
    txt_file_path = save_results_to_txt(os.path.splitext(file.filename)[0], extracted_info)
    save_results_to_db(extracted_info)

    # Thông báo thành công và trả về thông tin trích xuất
    return {
        "message": "OCR thành công",
        "extracted_info": extracted_info
    }
