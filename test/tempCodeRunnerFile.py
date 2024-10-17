import os

def rename_images_in_directory(directory):
    # Lấy danh sách tất cả file trong thư mục
    files = os.listdir(directory)
    
    # Các định dạng ảnh phổ biến
    valid_extensions = ('.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff', '.webp')
    
    # Lọc các file ảnh với đuôi bất kỳ
    image_files = [f for f in files if f.lower().endswith(valid_extensions)]

    # Sắp xếp các file để đảm bảo thứ tự
    image_files.sort()

    # Duyệt qua từng file và đổi tên
    for idx, filename in enumerate(image_files):
        # Tạo số thứ tự với 4 chữ số, thêm 0 vào trước nếu cần
        new_name = f"card_{idx:04d}.jpg"  # Bạn có thể chọn giữ định dạng cũ thay vì chuyển hết về .jpg
        
        # Lấy đường dẫn đầy đủ của file hiện tại và file mới
        old_path = os.path.join(directory, filename)
        new_path = os.path.join(directory, new_name)
        
        # Đổi tên file
        os.rename(old_path, new_path)
        print(f"Đã đổi tên {filename} thành {new_name}")

# Ví dụ sử dụng
directory = r"D:\Edu\Python\StudentID_FaceVerification\student-id-face-matching\test\imgTest copy"  # Thay bằng đường dẫn thư mục chứa ảnh của bạn
rename_images_in_directory(directory)
