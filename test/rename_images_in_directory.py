import os

def rename_images_in_directory(directory):
    files = os.listdir(directory)

    valid_extensions = ('.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff', '.webp')
    
    image_files = [f for f in files if f.lower().endswith(valid_extensions)]

    image_files.sort()

    for idx, filename in enumerate(image_files):
        new_name = f"card_{idx:04d}.jpg"
        
        old_path = os.path.join(directory, filename)
        new_path = os.path.join(directory, new_name)
        
        os.rename(old_path, new_path)
        print(f"Đã đổi tên {filename} thành {new_name}")

# thay phần này bằng đường dẫn chứa folder chứa ảnh cần đổi tên
directory = r"D:\Edu\Python\StudentID_FaceVerification\student-id-face-matching\test\output"
rename_images_in_directory(directory)
