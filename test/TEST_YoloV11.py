import cv2
from ultralytics import YOLO

model = YOLO('yolo11n.pt')

cap = cv2.VideoCapture(r"D:\Edu\Python\StudentID_FaceVerification\student-id-face-matching\test\imgTest\video.mp4")

if not cap.isOpened():
    print("Không thể mở video")
    exit()

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("Không thể đọc khung hình, hoặc hết video")
        break

    results = model(frame)

    annotated_frame = results[0].plot()

    cv2.imshow('YOLOv8 Video Detection', annotated_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("Dừng video")
        break

cap.release()
cv2.destroyAllWindows()
