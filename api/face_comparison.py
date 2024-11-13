import base64
import numpy as np
import cv2
from io import BytesIO
from PIL import Image
import dlib

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(r"D:\Edu\Python\StudentID_FaceVerification\student-id-face-matching\api\models\shape_predictor_68_face_landmarks.dat")
facerec = dlib.face_recognition_model_v1(r"D:\Edu\Python\StudentID_FaceVerification\student-id-face-matching\api\models\dlib_face_recognition_resnet_model_v1.dat")

def decode_base64_image(base64_string): #hàm giải mã ảnh từ base64
    image_data = base64.b64decode(base64_string)
    image = Image.open(BytesIO(image_data)).convert("RGB")
    return np.array(image)

def get_face_embedding(image): #hàm trích xuất vector đặc trưng từ ảnh
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = detector(gray)

    if len(faces) == 0:
        return None

    shape = predictor(gray, faces[0])
    face_embedding = facerec.compute_face_descriptor(image, shape)  #trích xuất vector đặc trưng

    return np.array(face_embedding)

def compare_faces(uploaded_image, face_image_base64, threshold=0.6): #hàm so sánh 2 ảnh bằng vector đặc trưng
    """So sánh hai khuôn mặt và trả về kết quả so sánh."""
    image1 = cv2.cvtColor(uploaded_image, cv2.COLOR_RGB2BGR)
    image2 = decode_base64_image(face_image_base64)
        
    embedding1 = get_face_embedding(image1)
    embedding2 = get_face_embedding(image2)

    if embedding1 is None:
        return "Ảnh tải lên không tìm thấy khuôn mặt"
    if embedding2 is None:
        return "Ảnh khuôn mặt từ thẻ không tìm thấy khuôn mặt"

    distance = np.linalg.norm(embedding1 - embedding2)

    if distance < threshold:
        return f"Cùng 1 người (Khoảng cách Euclidean: {distance:.2f})"
    else:
        return f"2 người khác nhau (Khoảng cách Euclidean: {distance:.2f})"
