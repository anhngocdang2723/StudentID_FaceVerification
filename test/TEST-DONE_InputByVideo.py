from ultralytics import YOLO
import cv2
import time

model = YOLO(r"D:\Edu\Python\StudentID_FaceVerification\student-id-face-matching\api\models\best.pt")

video_path = r"D:\Edu\Python\StudentID_FaceVerification\student-id-face-matching\test\imgTest\5974983164661.mp4"
cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    print("Không thể mở video.")
    exit()

# Ngưỡng confidence tối thiểu để lưu ảnh
confidence_threshold = 0.94  # Chỉ lưu ảnh khi confidence cao hơn ngưỡng này
padding = 10  # Ngưỡng pixel để mở rộng bounding box

while True:
    ret, frame = cap.read()
    if not ret:
        print("Đã đến cuối video hoặc không thể đọc khung hình.")
        break

    results = model.predict(source=frame, show=False, conf=0.25)

    # Khởi tạo biến để lưu đối tượng có độ tương đồng cao nhất
    max_confidence = 0
    best_box = None

    # Tìm bounding box có độ confidence cao nhất
    for box in results[0].boxes:
        confidence = box.conf[0]
        if confidence > max_confidence and confidence > confidence_threshold:
            max_confidence = confidence
            best_box = box

    # Nếu có box với confidence cao nhất, lưu ảnh đối tượng
    if best_box is not None:
        x1, y1, x2, y2 = map(int, best_box.xyxy[0])

        # Mở rộng bounding box
        x1 = max(x1 - padding, 0)  # Đảm bảo không ra ngoài biên
        y1 = max(y1 - padding, 0)
        x2 = min(x2 + padding, frame.shape[1])  # Đảm bảo không ra ngoài biên
        y2 = min(y2 + padding, frame.shape[0])

        detected_object = frame[y1:y2, x1:x2]

        # Tạo tên file với thời gian hiện tại để tránh trùng lặp
        filename = time.strftime(r"D:\Edu\Python\StudentID_FaceVerification\student-id-face-matching\test\output\best_detected_object_%Y%m%d%H%M%S.jpg")
        cv2.imwrite(filename, detected_object)
        print(f"Ảnh đã được lưu tại: {filename} với độ tương đồng {max_confidence:.2f}")

    annotated_frame = results[0].plot()
    cv2.imshow("YOLO Video Detection", annotated_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
