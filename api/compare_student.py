def compare_with_student_list(extracted_info, students_list):  
    """
    So sánh mã sinh viên từ thông tin OCR với danh sách sinh viên.

    :param extracted_info: Thông tin trích xuất từ OCR (dict).
    :param students_list: Danh sách sinh viên (danh sách chuỗi có định dạng "Tên - MSV").
    :return: True nếu tìm thấy sinh viên, False nếu không.
    """
    if 'MSV' in extracted_info:  # Kiểm tra nếu 'MSV' có trong extracted_info
        msv_from_ocr = extracted_info['MSV']
        # print("Mã sinh viên từ OCR:", msv_from_ocr) # Log giá trị MSV từ OCR

        # Tách danh sách sinh viên thành các phần tử có dạng (tên, msv)
        students_data = [student.split(' - ') for student in students_list]
        
        for student in students_data:  # Duyệt từng sinh viên, so sánh MSV
            student_name, student_msv = student[0], student[1]
            if msv_from_ocr == student_msv:
                print(f"Thông tin sinh viên khớp: {student_name} - {student_msv}") # Log thông tin sinh viên khớp
                return True
        print("Không tìm thấy mã sinh viên trong danh sách.")
        return False
    else:
        print("Không có mã sinh viên trong dữ liệu OCR.")
        return False
