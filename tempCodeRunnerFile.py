from paddleocr import PaddleOCR
import os

# Khởi tạo PaddleOCR với ngôn ngữ Tiếng Việt
ocr = PaddleOCR(use_angle_cls=True, lang='en')

# Đường dẫn đến file danh sách thí sinh (có thể là file PDF hoặc ảnh)
img_path = r"D:\Edu\Python\StudentID_FaceVerification\student-id-face-matching\List of candidates\image.png"

# Kiểm tra file có tồn tại không
if not os.path.exists(img_path):
    print(f"File {img_path} không tồn tại.")
else:
    # Nhận diện văn bản từ file danh sách
    result = ocr.ocr(img_path, cls=True)

    # Trích xuất văn bản từ kết quả OCR
    extracted_names = []
    for line in result[0]:  # Xử lý từng dòng được OCR nhận diện
        text = line[1][0].strip()
        extracted_names.append(text)

    # In kết quả sau khi đọc danh sách
    print("Kết quả trích xuất từ danh sách thí sinh:")
    for name in extracted_names:
        print(name)

    # Bạn có thể lưu kết quả vào file TXT hoặc CSV nếu muốn
    with open('extracted_list.txt', 'w', encoding='utf-8') as f:
        for name in extracted_names:
            f.write(name + '\n')
        print("Kết quả đã được lưu vào file 'extracted_list.txt'.")
