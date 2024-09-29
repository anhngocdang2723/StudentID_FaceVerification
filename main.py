from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse, FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from paddleocr import PaddleOCR
import cv2
import re
import os
import csv

#khởi tạo FastAPI
app = FastAPI()

#khởi tạo PaddleOCR để đọc tiếng việt
ocr = PaddleOCR(use_angle_cls=True, lang='vi')

#đường dẫn lưu trữ đến các thư mục chứa ảnh, ảnh đã xử lý và kết quả
UPLOAD_FOLDER = "uploads/"
PROCESSED_FOLDER = "processed/"
RESULTS_FOLDER = "results/"

#kiểm tra và tạo thư mục nếu chưa tồn tại
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)
os.makedirs(RESULTS_FOLDER, exist_ok=True)

#mount static files (CSS, JS, etc.)
app.mount("/static", StaticFiles(directory="static"), name="static")


#Endpoints hiển thị web
@app.get("/", response_class=HTMLResponse)
async def get_home():
    with open("static/index.html", "r", encoding="utf-8") as f:
        html_content = f.read()
    return HTMLResponse(content=html_content)


#tiền xử lý ảnh (grayscale và ngưỡng hóa)
def preprocess_image(image_path: str) -> str:
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)

    processed_image_path = os.path.join(PROCESSED_FOLDER, f"processed_{os.path.basename(image_path)}")
    cv2.imwrite(processed_image_path, thresh)
    return processed_image_path


#trích xuất thông tin từ kết quả OCR
def extract_info_from_ocr(result):
    fields = {
        "Tên": "",
        "Ngành": "",
        "Khoa/Viện": "",
        "Khoá": "",
        "MSV": ""
    }

    #sắp xếp kết quả theo thứ tự từ trên xuống dưới theo trục y
    sorted_result = sorted(result[0], key=lambda x: x[0][0][1])

    next_line_is_name = False
    found_msv = False

    for line in sorted_result:
        text = line[1][0].strip()

        #kiểm tra từ khóa "Thẻ Sinh Viên"
        if "THE SINH VIEN" in text.upper():
            next_line_is_name = True
            continue

        #nếu dòng tiếp theo sau "Thẻ Sinh Viên" thì có là tên
        if next_line_is_name:
            fields["Tên"] = text
            next_line_is_name = False

        #trích xuất MSV 
        if not found_msv and "MSV" in text.upper():
            msv_match = re.search(r"\d{9,}", text)
            if msv_match:
                fields["MSV"] = msv_match.group(0)
            found_msv = True

        #trích xuất ngành học dựa trên từ khóa "Ngành"
        if "NGANH" in text.upper() in text.upper():
            fields["Ngành"] = text

        #trích xuất Khoa/Viện dựa trên từ khóa "Khoa" hoặc "Viện"
        if "VIEN" in text.upper():
            fields["Khoa/Viện"] = text

        #trích xuất Khoá học dựa trên định dạng "xxxx-xxxx"
        if re.search(r"\d{4}-\d{4}", text):
            fields["Khoá"] = text

    return fields

### Sẽ update để lưu vào database
#lưu kết quả vào file TXT
def save_results_to_txt(filename, extracted_info):
    result_file = os.path.join(RESULTS_FOLDER, f"{filename}_result.txt")
    with open(result_file, "w", encoding="utf-8") as f:
        for field, value in extracted_info.items():
            f.write(f"{field}: {value}\n")
    return result_file
#lưu kết quả vào file CSV
def save_results_to_csv(filename, extracted_info):
    result_file = os.path.join(RESULTS_FOLDER, f"{filename}_result.csv")
    with open(result_file, "w", newline='', encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Field", "Value"])
        for field, value in extracted_info.items():
            writer.writerow([field, value])
    return result_file


#Endpoint để xử lý ảnh và thực hiện OCR
@app.post("/upload-image")
async def upload_image(file: UploadFile = File(...)):
    #lưu file ảnh vào thư mục uploads
    file_location = os.path.join(UPLOAD_FOLDER, file.filename)
    with open(file_location, "wb") as f:
        f.write(file.file.read())

    #tiền xử lý ảnh
    processed_image_path = preprocess_image(file_location)

    #OCR: Nhận diện văn bản từ ảnh đã tiền xử lý
    result = ocr.ocr(processed_image_path, cls=True)

    #trích xuất thông tin từ kết quả OCR
    extracted_info = extract_info_from_ocr(result)

    ##### Sẽ update để lưu vào database #####
    #lưu kết quả vào file TXT và CSV
    txt_file_path = save_results_to_txt(os.path.splitext(file.filename)[0], extracted_info)
    csv_file_path = save_results_to_csv(os.path.splitext(file.filename)[0], extracted_info)

    #thông báo thành công và trả về thông tin trích xuất
    return {
        "message": "OCR thành công",
        "extracted_info": extracted_info
    }

#Sẽ sửa thành update vào database
# # Endpoint để tải file kết quả TXT
# @app.get("/results/{filename}", response_class=FileResponse)
# async def download_file(filename: str):
#     file_path = os.path.join(RESULTS_FOLDER, filename)
#     return FileResponse(file_path)
