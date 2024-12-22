import cv2
import face_recognition

# Đường dẫn tới ảnh chuẩn (ảnh của người cần so sánh)
reference_image_path = r"D:\Edu\Python\StudentID_FaceVerification\student-id-face-matching\api\(delete)img\NgocAnh_face.jpg"  # Thay bằng đường dẫn ảnh của bạn
reference_image = face_recognition.load_image_file(reference_image_path)
reference_encoding = face_recognition.face_encodings(reference_image)[0]  # Mã hóa khuôn mặt chuẩn

# Mở webcam
cap = cv2.VideoCapture(1)

if not cap.isOpened():
    print("Error: Could not open the camera.")
    exit()

while True:
    # Đọc từng khung hình từ webcam
    ret, frame = cap.read()
    if not ret:
        print("Error: Could not read frame.")
        break

    # Chuyển đổi khung hình sang định dạng RGB (yêu cầu bởi face_recognition)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Phát hiện khuôn mặt và mã hóa khuôn mặt từ webcam
    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        # So sánh khuôn mặt với khuôn mặt chuẩn
        matches = face_recognition.compare_faces([reference_encoding], face_encoding, tolerance=0.6)
        label = "Match" if matches[0] else "Not Match"

        # Vẽ khung và hiển thị kết quả
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0) if matches[0] else (0, 0, 255), 2)
        cv2.putText(frame, label, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0) if matches[0] else (0, 0, 255), 2)

    # Hiển thị khung hình
    cv2.imshow('Face Comparison', frame)

    # Nhấn 'q' để thoát
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Giải phóng tài nguyên
cap.release()
cv2.destroyAllWindows()
