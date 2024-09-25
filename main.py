import cv2
import pytesseract
import face_recognition
from PIL import Image
import numpy as np

# Đường dẫn đến file Tesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def extract_text_from_card(card_image_path):
    """Trích xuất thông tin từ ảnh thẻ sinh viên bằng Tesseract OCR"""
    card_img = cv2.imread(card_image_path)
    card_img_rgb = cv2.cvtColor(card_img, cv2.COLOR_BGR2RGB)
    
    # Sử dụng Tesseract OCR để trích xuất văn bản
    extracted_text = pytesseract.image_to_string(card_img_rgb)
    return extracted_text

def load_and_encode_image(image_path):
    """Tải và mã hóa khuôn mặt từ ảnh"""
    img = face_recognition.load_image_file(image_path)
    face_encodings = face_recognition.face_encodings(img)
    
    if len(face_encodings) > 0:
        return face_encodings[0]
    else:
        return None

def compare_faces(card_face_encoding, live_face_encoding):
    """So sánh hai khuôn mặt xem có khớp nhau không"""
    if card_face_encoding is None or live_face_encoding is None:
        return False
    
    results = face_recognition.compare_faces([card_face_encoding], live_face_encoding)
    return results[0]

def main(card_image_path, live_image_path):
    # Bước 1: Trích xuất thông tin từ thẻ sinh viên
    print("Trích xuất thông tin từ thẻ sinh viên...")
    extracted_text = extract_text_from_card(card_image_path)
    print("Thông tin trên thẻ sinh viên: \n", extracted_text)

    # Bước 2: Nhận diện khuôn mặt trên thẻ sinh viên và ảnh sống
    print("\nNhận diện khuôn mặt...")
    card_face_encoding = load_and_encode_image(card_image_path)
    live_face_encoding = load_and_encode_image(live_image_path)

    # Bước 3: So sánh hai khuôn mặt
    match_result = compare_faces(card_face_encoding, live_face_encoding)

    if match_result:
        print("\nKết quả: Khuôn mặt khớp!")
    else:
        print("\nKết quả: Khuôn mặt không khớp!")

if __name__ == "__main__":
    card_image_path = r"StudentID_FaceVerification/student-id-face-matching/img/R.jpg"
    live_image_path = r"StudentID_FaceVerification/student-id-face-matching/img/face.jpg"
    
    main(card_image_path, live_image_path)
