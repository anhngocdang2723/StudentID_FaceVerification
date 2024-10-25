import cv2
import numpy as np
import albumentations as A
import os

# Đường dẫn tới thư mục chứa ảnh gốc và thư mục lưu ảnh augmented
input_folder = r'D:\Edu\Python\StudentID_FaceVerification\student-id-face-matching\test\input'
output_folder = r'D:\Edu\Python\StudentID_FaceVerification\student-id-face-matching\test\output'
os.makedirs(output_folder, exist_ok=True)

# Hàm thêm nhiễu Salt-and-Pepper
def add_salt_pepper_noise(image, prob=0.02):
    noisy_image = image.copy()
    num_salt = int(prob * image.size * 0.5)
    num_pepper = int(prob * image.size * 0.5)

    # Tạo điểm nhiễu trắng (salt)
    coords = [np.random.randint(0, i - 1, num_salt) for i in image.shape]
    noisy_image[coords[0], coords[1], :] = 255

    # Tạo điểm nhiễu đen (pepper)
    coords = [np.random.randint(0, i - 1, num_pepper) for i in image.shape]
    noisy_image[coords[0], coords[1], :] = 0
    return noisy_image

# Định nghĩa các phép biến đổi sử dụng Albumentations
augmentations = [
    A.HorizontalFlip(p=1.0),
    A.VerticalFlip(p=1.0),
    A.Rotate(limit=10, p=1.0),  # Xoay ngẫu nhiên trong khoảng -10 đến 10 độ
    A.RandomScale(scale_limit=0.2, p=1.0),  # Phóng to hoặc thu nhỏ ngẫu nhiên
    A.ShiftScaleRotate(shift_limit=0.1, scale_limit=0, rotate_limit=0, p=1.0),  # Dịch chuyển ngẫu nhiên
    A.GaussianBlur(blur_limit=(3, 5), p=1.0),  # Làm mờ Gaussian
    A.RandomBrightnessContrast(p=1.0),  # Thay đổi độ sáng, độ tương phản
    A.RGBShift(r_shift_limit=20, g_shift_limit=20, b_shift_limit=20, p=1.0),  # Biến đổi màu sắc
]

# Hàm thực hiện các biến đổi và lưu ảnh
def augment_image(image_path, output_folder, num_augmented=10):
    image = cv2.imread(image_path)
    base_filename = os.path.splitext(os.path.basename(image_path))[0]

    for i in range(num_augmented):
        if i < len(augmentations):
            # Áp dụng phép biến đổi trong danh sách
            transform = augmentations[i]
            augmented = transform(image=image)["image"]
        else:
            # Thêm nhiễu salt-and-pepper
            augmented = add_salt_pepper_noise(image)

        # Lưu ảnh sau biến đổi
        output_path = os.path.join(output_folder, f"{base_filename}_aug_{i}.jpg")
        cv2.imwrite(output_path, augmented)

# Thực hiện biến đổi trên tất cả ảnh trong thư mục đầu vào
for image_file in os.listdir(input_folder):
    image_path = os.path.join(input_folder, image_file)
    augment_image(image_path, output_folder)

# Hàm đổi tên ảnh trong thư mục thành dạng card_XXXX.jpg
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

# Đường dẫn tới thư mục chứa ảnh đã augment để đổi tên
rename_images_in_directory(output_folder)
