# Giả sử bạn đã có kết quả từ việc đọc thẻ sinh viên
# student_info chứa tên và mã số sinh viên được đọc từ thẻ
student_info = {
    # "Tên": "Dang Ngoc Anh",  # Thay thế bằng tên thực tế đọc từ thẻ
    # "MSV": "215748020110333"  # Thay thế bằng mã số sinh viên thực tế đọc từ thẻ
}

# Hàm so sánh với danh sách đã trích xuất
def compare_with_list(student_info, extracted_list):
    for entry in extracted_list:
        name, msv = entry.split(" - ")
        if student_info['Tên'].strip().lower() == name.strip().lower() and student_info['MSV'] == msv.strip():
            return f"Sinh viên {student_info['Tên']} có mặt trong danh sách phòng thi."
    return f"Sinh viên {student_info['Tên']} không có mặt trong danh sách phòng thi."

# Đọc danh sách từ file đã lưu
with open(r'D:\Edu\Python\StudentID_FaceVerification\student-id-face-matching\List of candidates\extracted_list\extracted_list.txt', 'r', encoding='utf-8') as f:
    extracted_list = f.readlines()

# Xóa ký tự newline và khoảng trắng thừa
extracted_list = [entry.strip() for entry in extracted_list]

# So sánh và in kết quả
result = compare_with_list(student_info, extracted_list)
print(result)
