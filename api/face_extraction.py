import cv2
import logging

# Khởi tạo CascadeClassifier một lần khi khởi động module
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

logging.basicConfig(level=logging.INFO)

def resize_image(img, scale_percent):
    width = int(img.shape[1] * scale_percent / 100)
    height = int(img.shape[0] * scale_percent / 100)
    dim = (width, height)
    return cv2.resize(img, dim)

def detect_face(img, scale_percent=50):  # scale_percent = 100 == kích thước gốc
    resized_img = resize_image(img, scale_percent)
    faces = face_cascade.detectMultiScale(cv2.cvtColor(resized_img, cv2.COLOR_BGR2GRAY), scaleFactor=1.1, minNeighbors=5)
    
    if len(faces) > 0:
        (x, y, w, h) = faces[0]
        # Chuyển đổi lại tỷ lệ cho khuôn mặt đã phát hiện
        x = int(x * (100 / scale_percent))
        y = int(y * (100 / scale_percent))
        w = int(w * (100 / scale_percent))
        h = int(h * (100 / scale_percent))
        return img[y:y+h, x:x+w]
    return None

def process_student_id(img_path, output_face_path):
    try:
        img = cv2.imread(img_path)
        if img is None:
            raise ValueError(f"Không thể đọc được ảnh từ đường dẫn {img_path}")
        
        logging.info("Đã đọc thành công ảnh.")
        
        face_img = detect_face(img)

        if face_img is not None:
            cv2.imwrite(output_face_path, face_img)
            logging.info("Đã lưu khuôn mặt.")
            return True
        else:
            logging.warning("Không tìm thấy khuôn mặt.")
            return False
    except Exception as e:
        logging.error(f"Lỗi trong quá trình xử lý: {e}")
        return False
