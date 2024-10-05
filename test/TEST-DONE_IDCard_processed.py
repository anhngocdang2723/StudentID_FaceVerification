import cv2

# Đọc ảnh
#img_path = r"D:\\Edu\\Python\StudentID_FaceVerification\student-id-face-matching\\test\\imgTest\\NgocAnhIDCard.jpg"
img_path = r"D:\\Edu\\Python\StudentID_FaceVerification\student-id-face-matching\\test\\imgTest\\CuuChuongIDCard.jpg"
#img_path = r"D:\\Edu\\Python\StudentID_FaceVerification\student-id-face-matching\\test\\imgTest\\NgocAnhIDCard.jpg"
img = cv2.imread(img_path)

# Chuyển ảnh sang xám
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Tải mô hình phát hiện khuôn mặt
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Giảm kích thước ảnh để tăng tốc độ phát hiện
scale_percent = 50  # Tỉ lệ % để giảm kích thước
width = int(img.shape[1] * scale_percent / 100)
height = int(img.shape[0] * scale_percent / 100)
dim = (width, height)
resized_img = cv2.resize(img, dim)

# Phát hiện khuôn mặt
faces = face_cascade.detectMultiScale(cv2.cvtColor(resized_img, cv2.COLOR_BGR2GRAY), scaleFactor=1.1, minNeighbors=5)

# Kiểm tra xem có khuôn mặt nào được phát hiện không
if len(faces) > 0:
    # Lấy tọa độ của khuôn mặt đầu tiên
    (x, y, w, h) = faces[0]
    
    # Chuyển tọa độ về kích thước ảnh gốc
    x = int(x * (100 / scale_percent))
    y = int(y * (100 / scale_percent))
    w = int(w * (100 / scale_percent))
    h = int(h * (100 / scale_percent))

    # Cắt và lưu ảnh khuôn mặt
    face_img = img[y:y+h, x:x+w]
    #cv2.imwrite(r"D:\\Edu\\Python\StudentID_FaceVerification\student-id-face-matching\\test\\resultTest\\NgocAnhIDCard_face.jpg", face_img)
    cv2.imwrite(r"D:\\Edu\\Python\StudentID_FaceVerification\student-id-face-matching\\test\\resultTest\\CuuChuongIDCard_face.jpg", face_img)
    #cv2.imwrite(r"D:\\Edu\\Python\StudentID_FaceVerification\student-id-face-matching\\test\\resultTest\\NgocAnhIDCard_face.jpg", face_img)

    
    # Hiển thị ảnh đã cắt
    cv2.imshow("Face", face_img)
else:
    print("Không tìm thấy khuôn mặt.")

# Áp dụng ngưỡng hóa để tạo ảnh nhị phân (ảnh chỉ chứa 2 màu đen và trắng)
_, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)

# Lưu ảnh đã xử lý
#cv2.imwrite(r"D:\Edu\\Python\StudentID_FaceVerification\student-id-face-matching\\test\\resultTest\\NgocAnhIDCard_processed.jpg", thresh)
cv2.imwrite(r"D:\\Edu\\Python\StudentID_FaceVerification\student-id-face-matching\\test\\resultTest\\CuuChuongIDCard_processed.jpg", thresh)
#cv2.imwrite(r"D:\\Edu\\Python\StudentID_FaceVerification\student-id-face-matching\\test\\resultTest\\NgocAnhIDCard_processed.jpg", thresh)

# Đợi và đóng cửa sổ hiển thị
cv2.waitKey(0)
cv2.destroyAllWindows()
