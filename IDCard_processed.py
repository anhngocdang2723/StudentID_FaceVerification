import cv2

# Đọc ảnh từ file
img_path = r"D:\Edu\Python\StudentID_FaceVerification\student-id-face-matching\img\ThaiTuanIDCard.jpg"
img = cv2.imread(img_path)

#chuyển ảnh xám
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

#áp dụng ngưỡng hoá để tạo ảnh nhị phân (ảnh chỉ chứa 2 màu đen và trắng) 
_, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)

#lưu ảnh đã xử lý
cv2.imwrite(r"D:\Edu\Python\StudentID_FaceVerification\student-id-face-matching\img\ThaiTuanIDCard_processed.jpg", thresh)
