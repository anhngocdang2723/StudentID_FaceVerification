import cv2

# Đọc ảnh từ file
img_path = r"D:\Edu\Python\StudentID_FaceVerification\student-id-face-matching\img\ThaiTuanIDCard.jpg"
img = cv2.imread(img_path)

# Chuyển ảnh sang dạng grayscale (màu xám)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Áp dụng ngưỡng hóa để loại bỏ nhiễu
_, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)

# Lưu ảnh đã xử lý lại để kiểm tra
cv2.imwrite(r"D:\Edu\Python\StudentID_FaceVerification\student-id-face-matching\img\ThaiTuanIDCard_processed.jpg", thresh)
