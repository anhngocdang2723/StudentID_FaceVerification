import cv2
import logging
import base64
from PIL import Image
import io

# Khởi tạo CascadeClassifier
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

logging.basicConfig(level=logging.INFO)

def resize_image(img, scale_percent):
    width = int(img.shape[1] * scale_percent / 100)
    height = int(img.shape[0] * scale_percent / 100)
    dim = (width, height)
    return cv2.resize(img, dim)

def detect_face(img, scale_percent=50, expand_ratio=0.2):  # expand_ratio = 20%
    resized_img = resize_image(img, scale_percent)
    faces = face_cascade.detectMultiScale(cv2.cvtColor(resized_img, cv2.COLOR_BGR2GRAY), scaleFactor=1.1, minNeighbors=5)
    
    if len(faces) > 0:
        (x, y, w, h) = faces[0]
        # Chuyển đổi lại tỷ lệ cho khuôn mặt đã phát hiện
        x = int(x * (100 / scale_percent))
        y = int(y * (100 / scale_percent))
        w = int(w * (100 / scale_percent))
        h = int(h * (100 / scale_percent))

        # Mở rộng kích thước khuôn mặt
        expand_w = int(w * expand_ratio)
        expand_h = int(h * expand_ratio)
        
        # Cập nhật lại tọa độ với kích thước mở rộng
        x = max(x - expand_w // 2, 0)  # không để x âm
        y = max(y - expand_h // 2, 0)  # không để y âm
        w = min(w + expand_w, img.shape[1] - x)  # không vượt quá chiều rộng ảnh
        h = min(h + expand_h, img.shape[0] - y)  # không vượt quá chiều cao ảnh
        
        return img[y:y+h, x:x+w]
    return None

def process_student_id(img_path):  # Hàm xử lý ảnh thẻ sinh viên và trả về khuôn mặt dưới dạng base64
    try:
        img = cv2.imread(img_path)
        if img is None:
            raise ValueError(f"Không thể đọc được ảnh từ đường dẫn {img_path}")
        
        logging.info("Đã đọc thành công ảnh.")
        face_img = detect_face(img)

        if face_img is not None:
            # Chuyển đổi ảnh khuôn mặt thành định dạng base64
            pil_img = Image.fromarray(cv2.cvtColor(face_img, cv2.COLOR_BGR2RGB))  # Chuyển đổi từ BGR sang RGB
            buffered = io.BytesIO()
            pil_img.save(buffered, format="JPEG")
            img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')
            logging.info("Đã cắt và mã hóa khuôn mặt thành công.")
            return img_str
        else:
            logging.warning("Không tìm thấy khuôn mặt.")
            return None
    except Exception as e:
        logging.error(f"Lỗi trong quá trình xử lý: {e}")
        return None
