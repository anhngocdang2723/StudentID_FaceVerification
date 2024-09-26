from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse, FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from paddleocr import PaddleOCR
import cv2
import re
import os
import csv

# Khởi tạo ứng dụng FastAPI
app = FastAPI()

# Khởi tạo PaddleOCR cho Tiếng Việt
ocr = PaddleOCR(use_angle_cls=True, lang='vi')

# Đường dẫn đến các thư mục xử lý
UPLOAD_FOLDER = "uploads/"
PROCESSED_FOLDER = "processed/"
RESULTS_FOLDER = "results/"

# Đảm bảo các thư mục tồn tại
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)
os.makedirs(RESULTS_FOLDER, exist_ok=True)

# Mount static files (for CSS, JS, etc.)
app.mount("/static", StaticFiles(directory="static"), name="static")


# Endpoint trả về file HTML (Giao diện web)
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

    # Sắp xếp kết quả nhận diện theo tọa độ y_min
    sorted_result = sorted(result[0], key=lambda x: x[0][0][1])

    next_line_is_name = False
    found_msv = False

    for line in sorted_result:
        text = line[1][0].strip()

        # Kiểm tra từ khóa "Thẻ Sinh Viên"
        if "THE SINH VIEN" in text.upper():
            next_line_is_name = True
            continue

        # Nếu dòng tiếp theo sau "Thẻ Sinh Viên" thì có khả năng là tên
        if next_line_is_name:
            fields["Tên"] = text
            next_line_is_name = False

        # Trích xuất MSV
        if not found_msv and "MSV" in text.upper():
            msv_match = re.search(r"\d{9,}", text)
            if msv_match:
                fields["MSV"] = msv_match.group(0)
            found_msv = True

        # Trích xuất Ngành học
        if "NGANH" in text.upper() or "C." in text.upper():
            fields["Ngành"] = text

        # Trích xuất Khoa/Viện
        if "VIEN" in text.upper():
            fields["Khoa/Viện"] = text

        # Trích xuất Khoá (dòng chứa năm học)
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


# Lưu kết quả vào file CSV
def save_results_to_csv(filename, extracted_info):
    result_file = os.path.join(RESULTS_FOLDER, f"{filename}_result.csv")
    with open(result_file, "w", newline='', encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Field", "Value"])
        for field, value in extracted_info.items():
            writer.writerow([field, value])
    return result_file


# Endpoint để xử lý ảnh và thực hiện OCR
@app.post("/upload-image")
async def upload_image(file: UploadFile = File(...)):
    # Lưu ảnh tải lên
    file_location = os.path.join(UPLOAD_FOLDER, file.filename)
    with open(file_location, "wb") as f:
        f.write(file.file.read())

    # Tiền xử lý ảnh
    processed_image_path = preprocess_image(file_location)

    # OCR: Nhận diện văn bản từ ảnh đã tiền xử lý
    result = ocr.ocr(processed_image_path, cls=True)

    # Trích xuất thông tin từ kết quả OCR
    extracted_info = extract_info_from_ocr(result)

    # Lưu kết quả vào file TXT và CSV
    txt_file_path = save_results_to_txt(os.path.splitext(file.filename)[0], extracted_info)
    csv_file_path = save_results_to_csv(os.path.splitext(file.filename)[0], extracted_info)

    # Trả về đường dẫn đến file TXT và CSV
    return {
        "message": "OCR thành công",
        "txt_file": txt_file_path,
        "csv_file": csv_file_path,
        "extracted_info": extracted_info
    }


# Endpoint để tải file kết quả TXT
@app.get("/results/{filename}", response_class=FileResponse)
async def download_file(filename: str):
    file_path = os.path.join(RESULTS_FOLDER, filename)
    return FileResponse(file_path)
