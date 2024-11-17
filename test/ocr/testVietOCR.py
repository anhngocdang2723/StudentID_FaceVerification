import os
import cv2
import matplotlib.pyplot as plt
from PIL import Image
import torch

# Import từ thư viện VietOCR
from vietocr.tool.predictor import Predictor
from vietocr.tool.config import Cfg

# Import từ thư viện PaddleOCR
from paddleocr import PaddleOCR, draw_ocr

# Đường dẫn tới font chữ
FONT = r'D:\Edu\Python\StudentID_FaceVerification\student-id-face-matching\test\ocr\latin.ttf'

# Hàm dự đoán sử dụng PaddleOCR và VietOCR
def predict(recognitor, detector, img_path, save_path, padding=4, dpi=100):
    # Đọc ảnh
    img = cv2.imread(img_path)
    
    if img is None:
        raise ValueError("Không thể đọc ảnh. Kiểm tra lại đường dẫn ảnh.")

    # Phát hiện văn bản bằng PaddleOCR
    result = detector.ocr(img_path, cls=False, det=True, rec=False)
    if not result or not result[0]:
        raise ValueError("Không phát hiện được văn bản trong ảnh.")
    
    result = result[0]  # Lấy kết quả phát hiện đầu tiên

    # Lọc và thêm padding vào các hộp
    boxes = []
    for line in result:
        x1, y1 = int(line[0][0]), int(line[0][1])
        x2, y2 = int(line[2][0]), int(line[2][1])
        
        # Thêm padding và kiểm tra giới hạn ảnh
        x1 = max(0, x1 - padding)
        y1 = max(0, y1 - padding)
        x2 = min(img.shape[1], x2 + padding)
        y2 = min(img.shape[0], y2 + padding)
        
        if (x2 - x1) > 0 and (y2 - y1) > 0:
            boxes.append([[x1, y1], [x2, y2]])

    # Nhận diện văn bản bằng VietOCR
    texts = []
    for box in boxes:
        x1, y1 = box[0]
        x2, y2 = box[1]
        cropped_image = img[y1:y2, x1:x2]
        
        if cropped_image.size == 0:  # Kiểm tra nếu ảnh bị lỗi
            continue
        
        try:
            cropped_image = Image.fromarray(cv2.cvtColor(cropped_image, cv2.COLOR_BGR2RGB))
        except Exception as e:
            print(f"Lỗi khi chuyển đổi ảnh: {e}")
            continue

        rec_result = recognitor.predict(cropped_image)
        texts.append(rec_result)

    # Vẽ các hộp và văn bản trên ảnh
    _boxes = [[(box[0][0], box[0][1]), (box[1][0], box[0][1]), (box[1][0], box[1][1]), (box[0][0], box[1][1])] for box in boxes]
    img = draw_ocr(img, _boxes, texts, scores=None, font_path=FONT)

    # Kiểm tra thư mục output và tạo nếu cần
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    # Lưu ảnh kết quả
    img_name = os.path.basename(img_path)
    output_file_path = os.path.join(save_path, img_name)
    cv2.imwrite(output_file_path, img)
    
    # Chuyển đổi BGR sang RGB để hiển thị
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    plt.imshow(img)
    plt.axis('off')
    plt.show()

    return boxes, texts

# Cấu hình cho PaddleOCR
detector = PaddleOCR(use_angle_cls=False, lang="vi", use_gpu=torch.cuda.is_available())

# Cấu hình cho VietOCR
config = Cfg.load_config_from_file(r'D:\Edu\Python\StudentID_FaceVerification\student-id-face-matching\test\ocr\config.yml')
config['device'] = 'cuda' if torch.cuda.is_available() else 'cpu'

recognitor = Predictor(config)

# Đường dẫn tới ảnh đầu vào và đầu ra
img_path = r"D:\Edu\Python\StudentID_FaceVerification\student-id-face-matching\test\imgTest\CuuChuongIDCard.jpg"
output_path = r'D:\Edu\Python\StudentID_FaceVerification\student-id-face-matching\test\ocr'

# Chạy dự đoán
try:
    boxes, texts = predict(recognitor, detector, img_path, output_path)
    print("Văn bản được nhận diện:", texts)
except Exception as e:
    print("Lỗi:", e)
