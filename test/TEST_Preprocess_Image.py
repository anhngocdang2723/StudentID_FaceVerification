import cv2

# Đọc ảnh
img = cv2.imread(r'D:\Edu\Python\StudentID_FaceVerification\student-id-face-matching\test\imgTest\NgocPhuongIDCard.jpg')

# Giảm kích thước ảnh
img = cv2.resize(img, (0, 0), fx=0.5, fy=0.3)

# Chuyển ảnh sang xám
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

cv2.namedWindow("TrackbarWindow")

def get_threshold_value(pos_thresh):
    global threshold_value
    threshold_value = pos_thresh

# Khởi tạo giá trị ngưỡng
threshold_value = 150  # Giá trị ngưỡng ban đầu
cv2.createTrackbar("Threshold", "TrackbarWindow", threshold_value, 255, get_threshold_value)

while True:
    # Áp dụng ngưỡng hóa để tạo ảnh nhị phân
    _, thresh = cv2.threshold(gray, threshold_value, 255, cv2.THRESH_BINARY)

    # Hiển thị giá trị ngưỡng
    text = f'Threshold: {threshold_value}'
    cv2.putText(thresh, text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

    cv2.imshow("TrackbarWindow", thresh)
    
    # Kiểm tra nếu nhấn phím 's' để lưu ảnh
    if cv2.waitKey(20) == ord('s'):
        cv2.imwrite(r'D:\Edu\Python\StudentID_FaceVerification\student-id-face-matching\api\processed\processed_NgocPhuongIDCard.jpg', thresh)
        print("Ảnh đã được lưu.")

    # Nhấn 'q' để thoát
    if cv2.waitKey(20) == ord('q'):
        break

cv2.destroyAllWindows()
