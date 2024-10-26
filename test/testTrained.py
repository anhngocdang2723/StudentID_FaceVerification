from ultralytics import YOLO
import cv2

# Load mô hình YOLO
model = YOLO(r"D:\Edu\Python\StudentID_FaceVerification\student-id-face-matching\api\models\best.pt")  # Thay bằng đường dẫn đến file .pt của bạn

# Khởi tạo webcam (device ID 0 là camera mặc định)
cap = cv2.VideoCapture(1)

# Kiểm tra xem webcam có mở thành công không
if not cap.isOpened():
    print("Không thể mở webcam.")
    exit()

while True:
    # Đọc từng khung hình từ webcam
    ret, frame = cap.read()
    if not ret:
        print("Không thể đọc khung hình từ webcam.")
        break

    # Dự đoán đối tượng trên khung hình
    results = model.predict(source=frame, show=False, conf=0.25)

    # Lấy kết quả đầu tiên (nếu có nhiều đối tượng thì lấy đối tượng đầu tiên)
    for box in results[0].boxes:
        # Tọa độ của bounding box
        x1, y1, x2, y2 = map(int, box.xyxy[0])  # Chuyển tọa độ về kiểu int

        # Cắt ảnh trong vùng bounding box
        card_image = frame[y1:y2, x1:x2]

        # Hiển thị ảnh thẻ trong cửa sổ riêng
        cv2.imshow("Student ID Card", card_image)
        
        #lưu ảnh thẻ
        cv2.imwrite(r"D:\Edu\Python\StudentID_FaceVerification\student-id-face-matching\test\output\card_image.jpg", card_image)

    # Hiển thị khung hình có kết quả nhận diện
    annotated_frame = results[0].plot()  # Khung hình với kết quả được vẽ
    cv2.imshow("YOLOv11 Live Detection", annotated_frame)

    # Nhấn phím 'q' để thoát
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Giải phóng tài nguyên
cap.release()
cv2.destroyAllWindows()
