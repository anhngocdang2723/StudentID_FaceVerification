from ultralytics import YOLO
import cv2

model = YOLO(r"D:\Edu\Python\StudentID_FaceVerification\student-id-face-matching\api\models\best.pt") 

cap = cv2.VideoCapture(1)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

if not cap.isOpened():
    print("Không thể mở webcam.")
    exit()

frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
virtual_box_x1, virtual_box_y1 = int(frame_width * 0.3), int(frame_height * 0.3)
virtual_box_x2, virtual_box_y2 = int(frame_width * 0.7), int(frame_height * 0.7)

# Biến đếm để chỉ xử lý một số khung hình
frame_count = 0
process_interval = 5  # Cài đặt xử lý mỗi 5 khung hình

while True:
    ret, frame = cap.read()
    if not ret:
        print("Không thể đọc khung hình từ webcam.")
        break

    # Tăng biến đếm
    frame_count += 1
    
    # Chỉ xử lý khi đạt tới interval
    if frame_count % process_interval == 0:
        # Vẽ khung ảo cố định lên khung hình
        cv2.rectangle(frame, (virtual_box_x1, virtual_box_y1), (virtual_box_x2, virtual_box_y2), (0, 255, 0), 2)

        results = model.predict(source=frame, show=False, conf=0.25)

        # Xử lý từng bounding box
        for box in results[0].boxes:
            # Tọa độ của bounding box từ YOLO
            x1, y1, x2, y2 = map(int, box.xyxy[0])

            # Kiểm tra nếu bounding box nằm hoàn toàn trong khung ảo
            if x1 >= virtual_box_x1 and y1 >= virtual_box_y1 and x2 <= virtual_box_x2 and y2 <= virtual_box_y2:
                
                card_image = frame[y1:y2, x1:x2]

                cv2.imshow("High Quality Student ID Card", card_image)
                cv2.imwrite(r"D:\Edu\Python\StudentID_FaceVerification\student-id-face-matching\test\output\student_id_card.jpg", card_image)

        annotated_frame = results[0].plot()
        cv2.imshow("YOLOv11 Live Detection", annotated_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()