import cv2
import pytesseract
import face_recognition
import numpy as np

# Đường dẫn đến file Tesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def extract_text_from_card(card_image_path):
    """Trích xuất thông tin từ ảnh thẻ sinh viên bằng Tesseract OCR"""
    try:
        card_img = cv2.imread(card_image_path)
        if card_img is None:
            print(f"Không thể tải ảnh từ đường dẫn: {card_image_path}")
            return None

        card_img_rgb = cv2.cvtColor(card_img, cv2.COLOR_BGR2RGB)
        
        # Sử dụng Tesseract OCR để trích xuất văn bản
        extracted_text = pytesseract.image_to_string(card_img_rgb)
        return extracted_text
    except Exception as e:
        print(f"Đã xảy ra lỗi khi trích xuất văn bản: {e}")
        return None

def detect_and_encode_face(image_path):
    """Tải và phát hiện khuôn mặt từ ảnh, sau đó mã hóa khuôn mặt"""
    try:
        # Đọc ảnh và tìm khuôn mặt bằng face_recognition
        image = face_recognition.load_image_file(image_path)
        face_locations = face_recognition.face_locations(image)

        if len(face_locations) == 0:
            print(f"Không tìm thấy khuôn mặt trong ảnh: {image_path}")
            return None

        # Mã hóa khuôn mặt
        face_encodings = face_recognition.face_encodings(image, face_locations)
        if len(face_encodings) > 0:
            return face_encodings[0]
        else:
            print(f"Không thể mã hóa khuôn mặt trong ảnh: {image_path}")
            return None
    except Exception as e:
        print(f"Đã xảy ra lỗi khi phát hiện và mã hóa khuôn mặt: {e}")
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
    
    if extracted_text:
        print("Thông tin trên thẻ sinh viên: \n", extracted_text)
    else:
        print("Không thể trích xuất thông tin từ thẻ sinh viên.")
        return

    # Bước 2: Nhận diện và mã hóa khuôn mặt trên thẻ sinh viên và ảnh sống
    print("\nNhận diện khuôn mặt...")
    card_face_encoding = detect_and_encode_face(card_image_path)
    live_face_encoding = detect_and_encode_face(live_image_path)

    # Bước 3: So sánh hai khuôn mặt
    if card_face_encoding is not None and live_face_encoding is not None:
        match_result = compare_faces(card_face_encoding, live_face_encoding)
        if match_result:
            print("\nKết quả: Khuôn mặt khớp!")
        else:
            print("\nKết quả: Khuôn mặt không khớp!")
    else:
        print("Không thể thực hiện so sánh khuôn mặt do thiếu mã hóa khuôn mặt.")

if __name__ == "__main__":
    card_image_path = r"StudentID_FaceVerification/student-id-face-matching/img/R.jpg"
    live_image_path = r"StudentID_FaceVerification/student-id-face-matching/img/face.jpg"
    
    main(card_image_path, live_image_path)
