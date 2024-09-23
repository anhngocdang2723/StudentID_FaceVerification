from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import Request
from PIL import Image
import pytesseract
import cv2
import numpy as np
import face_recognition
import os

app = FastAPI()

# Đường dẫn tới Tesseract OCR trong hệ thống của bạn (cài đặt đúng đường dẫn nếu cần)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Cấu hình template và static folder
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def main_page(request: Request):
    # Render trang HTML upload
    return templates.TemplateResponse("upload.html", {"request": request})


@app.post("/process_student_card/")
async def process_student_card(student_card: UploadFile = File(...), face_image: UploadFile = File(...)):
    # 1. Lưu và mở ảnh thẻ sinh viên
    student_card_image = Image.open(student_card.file)
    student_card_image.save("static/student_card.png")
    
    # 2. Trích xuất văn bản bằng OCR
    extracted_text = pytesseract.image_to_string(student_card_image, lang='vie')
    
    # 3. Cắt ảnh khuôn mặt từ thẻ sinh viên (giả sử bạn biết vị trí mặt trên thẻ)
    image_cv = cv2.imread("static/student_card.png")
    x, y, w, h = 50, 120, 170, 200  # Toạ độ cần điều chỉnh theo vị trí khuôn mặt
    student_face_image = image_cv[y:y+h, x:x+w]
    cv2.imwrite("static/student_face.png", student_face_image)
    
    # 4. Nhận diện và so sánh khuôn mặt
    # Load ảnh khuôn mặt từ thẻ và ảnh đối chiếu
    student_face_encoding = face_recognition.face_encodings(student_face_image)[0]
    
    # 5. Lưu và load ảnh đối chiếu từ người dùng
    face_to_compare_image = Image.open(face_image.file)
    face_to_compare_image.save("static/face_to_compare.jpg")
    face_to_compare_cv = np.array(face_to_compare_image)

    # Nhận diện khuôn mặt từ ảnh người dùng
    face_to_compare_encoding = face_recognition.face_encodings(face_to_compare_cv)[0]
    
    # So sánh hai khuôn mặt
    results = face_recognition.compare_faces([student_face_encoding], face_to_compare_encoding)
    
    if results[0]:
        match_result = "Khuôn mặt khớp với sinh viên."
    else:
        match_result = "Khuôn mặt không khớp."

    # Trả về kết quả
    return {
        "extracted_text": extracted_text,
        "match_result": match_result
    }
