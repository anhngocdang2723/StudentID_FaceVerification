# camera_detection.py

from fastapi import Response
import cv2
from ultralytics import YOLO

model = YOLO(r"D:\Edu\Python\StudentID_FaceVerification\student-id-face-matching\api\models\best.pt")  # Thay bằng đường dẫn đến model YOLO của bạn

async def detect_card_from_camera():
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        results = model.predict(frame)
        for result in results:
            # Lấy toạ độ bounding box và vẽ lên khung hình
            for box in result.boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

        # Encode khung hình và trả về response
        _, buffer = cv2.imencode('.jpg', frame)
        frame_data = buffer.tobytes()
        yield Response(content=frame_data, media_type="image/jpeg")
        
    cap.release()
