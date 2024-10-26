from ultralytics import YOLO
import cv2

# Load mô hình YOLO
model = YOLO(r"D:\Edu\Python\StudentID_FaceVerification\student-id-face-matching\api\models\best.pt")  # Thay bằng đường dẫn đến file .pt của bạn

# Khởi tạo webcam với độ phân giải cao
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

# Kiểm tra xem webcam có mở thành công không
if not cap.isOpened():
    print("Không thể mở webcam.")
    exit()

# Tọa độ của khung ảo cố định ở giữa màn hình
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
virtual_box_x1, virtual_box_y1 = int(frame_width * 0.3), int(frame_height * 0.3)
virtual_box_x2, virtual_box_y2 = int(frame_width * 0.7), int(frame_height * 0.7)

while True:
    # Đọc từng khung hình từ webcam
    ret, frame = cap.read()
    if not ret:
        print("Không thể đọc khung hình từ webcam.")
        break

    # Vẽ khung ảo cố định lên khung hình
    cv2.rectangle(frame, (virtual_box_x1, virtual_box_y1), (virtual_box_x2, virtual_box_y2), (0, 255, 0), 2)

    # Dự đoán đối tượng trên khung hình
    results = model.predict(source=frame, show=False, conf=0.25)

    # Xử lý từng bounding box
    for box in results[0].boxes:
        # Tọa độ của bounding box từ YOLO
        x1, y1, x2, y2 = map(int, box.xyxy[0])

        # Kiểm tra nếu bounding box nằm hoàn toàn trong khung ảo
        if x1 >= virtual_box_x1 and y1 >= virtual_box_y1 and x2 <= virtual_box_x2 and y2 <= virtual_box_y2:
            # Cắt ảnh trong vùng bounding box
            card_image = frame[y1:y2, x1:x2]

            # Hiển thị ảnh thẻ đã cắt và lưu ảnh
            cv2.imshow("High Quality Student ID Card", card_image)
            cv2.imwrite(r"D:\Edu\Python\StudentID_FaceVerification\student-id-face-matching\test\output\student_id_card.jpg", card_image)

    # Hiển thị khung hình có kết quả nhận diện
    annotated_frame = results[0].plot()
    cv2.imshow("YOLOv11 Live Detection", annotated_frame)

    # Nhấn phím 'q' để thoát
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Giải phóng tài nguyên
cap.release()
cv2.destroyAllWindows()
