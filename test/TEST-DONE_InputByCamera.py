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

while True:
    ret, frame = cap.read()
    if not ret:
        print("Không thể đọc khung hình từ webcam.")
        break

    cv2.rectangle(frame, (virtual_box_x1, virtual_box_y1), (virtual_box_x2, virtual_box_y2), (0, 255, 0), 2)

    results = model.predict(source=frame, show=False, conf=0.90)

    for box in results[0].boxes:
        x1, y1, x2, y2 = map(int, box.xyxy[0])

        if x1 >= virtual_box_x1 and y1 >= virtual_box_y1 and x2 <= virtual_box_x2 and y2 <= virtual_box_y2:
            card_image = frame[y1:y2, x1:x2]
            cv2.imshow("High Quality Student ID Card", card_image)
            cv2.imwrite(r"D:\Edu\Python\StudentID_FaceVerification\student-id-face-matching\test\output\student_id_card.jpg", card_image)

    annotated_frame = results[0].plot()
    cv2.imshow("YOLOv8 Live Detection", annotated_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
