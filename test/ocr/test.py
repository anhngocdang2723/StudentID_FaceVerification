import cv2
from paddleocr import PaddleOCR
from PIL import Image
from vietocr.tool.predictor import Predictor
from vietocr.tool.config import Cfg

# Khởi tạo PaddleOCR
ocr = PaddleOCR(use_angle_cls=True, lang='en')  # Dùng ngôn ngữ 'en' để phát hiện văn bản

# Cấu hình lại VietOCR để dùng mô hình seq2seq
config = Cfg.load_config_from_name('vgg_seq2seq')  # Thay đổi thành vgg_seq2seq
config['weights'] = 'path_to_your_seq2seq_model.pth'  # Đường dẫn đến mô hình seq2seq
config['device'] = 'cuda'  # Sử dụng 'cuda' nếu có GPU, không thì dùng 'cpu'
predictor = Predictor(config)

def extract_text_with_paddle_and_vietocr(image_path):
    # Đọc ảnh bằng OpenCV
    image = cv2.imread(image_path)
    
    # Dùng PaddleOCR để phát hiện văn bản
    results = ocr.ocr(image, cls=True)
    
    for line in results:
        for word_info in line:
            bbox, text, score = word_info
            # bbox chứa tọa độ 4 góc của vùng chứa văn bản
            x_min = int(min(point[0] for point in bbox))
            y_min = int(min(point[1] for point in bbox))
            x_max = int(max(point[0] for point in bbox))
            y_max = int(max(point[1] for point in bbox))
            
            # Cắt vùng chứa văn bản từ ảnh
            cropped_img = image[y_min:y_max, x_min:x_max]
            
            # Chuyển đổi ảnh cắt sang định dạng PIL cho VietOCR
            pil_img = Image.fromarray(cv2.cvtColor(cropped_img, cv2.COLOR_BGR2RGB))
            
            # Nhận diện văn bản với VietOCR
            recognized_text = predictor.predict(pil_img)
            print(f"Văn bản nhận diện được: {recognized_text}")

# Đường dẫn đến ảnh cần xử lý
img_path = r"D:\Edu\Python\StudentID_FaceVerification\student-id-face-matching\test\imgTest\ThaiTuanIDCard.jpg"
extract_text_with_paddle_and_vietocr(img_path)
