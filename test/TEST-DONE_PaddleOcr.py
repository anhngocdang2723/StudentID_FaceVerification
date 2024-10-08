from paddleocr import PaddleOCR
import re

# Khởi tạo mô hình PaddleOCR với ngôn ngữ Tiếng Việt
ocr = PaddleOCR(use_angle_cls=True, lang='vi')

# Đường dẫn đến ảnh thẻ sinh viên đã tiền xử lý
img_path = r"D:\Edu\Python\StudentID_FaceVerification\student-id-face-matching\test\imgTest\NgocAnhIDCard_processed.jpg"

# Nhận diện văn bản từ ảnh
result = ocr.ocr(img_path, cls=True)

# Chuẩn bị từ khóa để trích xuất thông tin
fields = {
    "Tên": "",
    "Ngành": "",
    "Khoa/Viện": "",
    "Khoá": "",
    "MSV": ""
}

# Lấy kết quả nhận diện và sắp xếp theo tọa độ y_min (từ trên xuống dưới)
sorted_result = sorted(result[0], key=lambda x: x[0][0][1])  # Sắp xếp theo tọa độ y_min của điểm đầu tiên của box

# Biến lưu trữ tên và flag để tìm tên sau "Thẻ Sinh Viên"
next_line_is_name = False
next_line_is_khoa = False
found_msv = False

# Duyệt qua kết quả nhận diện đã sắp xếp
for line in sorted_result:
    text = line[1][0].strip()
    print(f"Detected Text: {text}")  # In kết quả OCR thô để kiểm tra

    # Kiểm tra từ khóa "Thẻ Sinh Viên"
    if "THE SINH VIEN" in text.upper():
        next_line_is_name = True
        continue

    # Nếu dòng tiếp theo sau "Thẻ Sinh Viên" thì có khả năng là tên
    if next_line_is_name:
        fields["Tên"] = text
        next_line_is_name = False  # Sau khi tìm thấy tên thì reset flag
    
    # Trích xuất MSV
    if not found_msv and "MSV" in text.upper():
        msv_match = re.search(r"\d{9,}", text)  # Tìm MSV là dãy số dài (ít nhất 9 chữ số)
        if msv_match:
            fields["MSV"] = msv_match.group(0)
        found_msv = True

    # Trích xuất Ngành học 
    if "NGANH" in text.upper() or "C." in text.upper():  # Kiểm tra cả từ "C." cho trường hợp viết tắt
        fields["Ngành"] = text

    # Trích xuất Khoa/Viện
    if "VIEN" in text.upper():
        fields["Khoa/Viện"] = text

    # Trích xuất Khoá (dòng chứa năm học)
    if re.search(r"\d{4}-\d{4}", text):  # Tìm năm học
        fields["Khoá"] = text

# Hiển thị kết quả trích xuất
for field, value in fields.items():
    print(f"{field}: {value}")
