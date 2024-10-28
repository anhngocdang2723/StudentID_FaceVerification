import cv2

def upscale_image(image_path, model_path, scale=2):
    sr = cv2.dnn_superres.DnnSuperResImpl_create()
    sr.readModel(model_path)
    sr.setModel("fsrcnn", scale)  # Sử dụng FSRCNN với tỷ lệ phóng to (scale)
    
    image = cv2.imread(image_path)
    upscaled_image = sr.upsample(image)
    output_path = image_path.replace(".jpg", f"_upscaled_x{scale}.jpg")
    cv2.imwrite(output_path, upscaled_image)
    return output_path

# Thông tin đường dẫn
image_path = r"D:\Edu\Python\StudentID_FaceVerification\student-id-face-matching\test\output\student_id_card.jpg"
model_path = r"import cv2

def upscale_image(image_path, model_path, scale=2):
    sr = cv2.dnn_superres.DnnSuperResImpl_create()
    sr.readModel(model_path)
    sr.setModel("fsrcnn", scale)  # Sử dụng FSRCNN với tỷ lệ phóng to (scale)
    
    image = cv2.imread(image_path)
    upscaled_image = sr.upsample(image)
    output_path = image_path.replace(".jpg", f"_upscaled_x{scale}.jpg")
    cv2.imwrite(output_path, upscaled_image)
    return output_path

# Thông tin đường dẫn
image_path = r"D:\Edu\Python\StudentID_FaceVerification\student-id-face-matching\test\output\student_id_card.jpg"
model_path = r"D:\Edu\Python\StudentID_FaceVerification\student-id-face-matching\api\models\FSRCNN_x2.pb"

# Gọi hàm để upscale ảnh
upscaled_image_path = upscale_image(image_path, model_path)
print("Đường dẫn ảnh đã upscale:", upscaled_image_path)

# Gọi hàm để upscale ảnh
upscaled_image_path = upscale_image(image_path, model_path)
print("Đường dẫn ảnh đã upscale:", upscaled_image_path)
