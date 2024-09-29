from paddleocr import PaddleOCR
import os

# Khởi tạo PaddleOCR với ngôn ngữ Tiếng Việt
ocr = PaddleOCR(use_angle_cls=True, lang='vi')  # Đặt ngôn ngữ là tiếng Việt

# Đường dẫn đến file danh sách thí sinh (có thể là file PDF hoặc ảnh)
img_path = r"D:\Edu\Python\StudentID_FaceVerification\student-id-face-matching\List of candidates\DemoDanhSach.pdf"

# Kiểm tra file có tồn tại không
if not os.path.exists(img_path):
    print(f"File {img_path} không tồn tại.")
else:
    # Nhận diện văn bản từ file danh sách
    result = ocr.ocr(img_path, cls=True)

    # Trích xuất văn bản từ kết quả OCR
    extracted_names = []
    
    # Giữ tên và MSV tạm thời
    names_and_ids = []

    for line in result[0]:  # Xử lý từng dòng được OCR nhận diện
        text = line[1][0].strip()
        names_and_ids.append(text)

    # Xử lý để lấy tên và mã sinh viên
    for i in range(1, len(names_and_ids)):  # Bắt đầu từ dòng thứ 2
        current_line = names_and_ids[i]
        if len(current_line) == 15 and current_line.isdigit():  # Nếu dòng hiện tại là mã sinh viên
            student_id = current_line
            student_name = names_and_ids[i - 1]  # Lấy tên từ dòng trên
            extracted_names.append(f"{student_name} - {student_id}")  # Thêm vào danh sách kết quả

    # In kết quả sau khi đọc danh sách
    print("Kết quả trích xuất từ danh sách thí sinh:")
    for student in extracted_names:
        print(student)

    # Lưu kết quả vào file TXT
    with open(r'D:\Edu\Python\StudentID_FaceVerification\student-id-face-matching\List of candidates\extracted_list\extracted_list.txt', 'w', encoding='utf-8') as f:
        for student in extracted_names:
            f.write(student + '\n')
        print("Kết quả đã được lưu vào file 'extracted_list.txt'.")
