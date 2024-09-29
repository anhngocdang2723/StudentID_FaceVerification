from paddleocr import PaddleOCR

ocr = PaddleOCR(use_angle_cls=True, lang='vi')

# Đọc danh sách thí sinh từ ảnh
img_path = r"D:\Edu\Python\StudentID_FaceVerification\student-id-face-matching\List of candidates\list1.pdf"
result = ocr.ocr(img_path, cls=True)

# Chuyển danh sách từ ảnh sang text
extracted_names = []
for line in result[0]:
    text = line[1][0].strip()
    extracted_names.append(text)

def compare_with_image(student_info, extracted_names):
    for name in extracted_names:
        if student_info['Tên'].lower() in name.lower():
            return f"Sinh viên {student_info['Tên']} có mặt trong danh sách phòng thi."
    return f"Sinh viên {student_info['Tên']} không có mặt trong danh sách phòng thi."

# Ví dụ sau khi đã nhận diện thông tin từ thẻ
student_info = {
    "Tên": "Đặng Ngọc Anh",
    "MSV": "215748020110333"
}

result = compare_with_image(student_info, extracted_names)
print(result)
