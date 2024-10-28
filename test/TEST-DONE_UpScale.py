import cv2

def upscale_image(image_path, model_path, scale=4):
    sr = cv2.dnn_superres.DnnSuperResImpl_create()
    sr.readModel(model_path)
    sr.setModel("edsr", scale)  # Sử dụng EDSR với tỷ lệ phóng to được truyền vào

    image = cv2.imread(image_path)
    if image is None:
        raise ValueError("Không thể đọc ảnh từ đường dẫn đã cung cấp.")
    
    upscaled_image = sr.upsample(image)
    output_path = image_path.replace(".jpg", f"_upscaled_x{scale}.jpg")
    cv2.imwrite(output_path, upscaled_image)
    return output_path

image_path = r"D:\Edu\Python\StudentID_FaceVerification\student-id-face-matching\test\output\best_detected_object_20241028132406.jpg"
model_path = r"D:\Edu\Python\StudentID_FaceVerification\student-id-face-matching\api\models\EDSR_x4.pb"

upscaled_image_path = upscale_image(image_path, model_path)
print("Đường dẫn ảnh đã upscale:", upscaled_image_path)
