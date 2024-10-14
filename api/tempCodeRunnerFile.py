import cv2
import dlib
import numpy as np

# Load dlib's pre-trained face detector and the face landmark predictor
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(r"D:\Edu\Python\StudentID_FaceVerification\student-id-face-matching\api\models\shape_predictor_68_face_landmarks.dat")
# Load Face Recognition model (ResNet)
facerec = dlib.face_recognition_model_v1(r"D:\Edu\Python\StudentID_FaceVerification\student-id-face-matching\api\models\dlib_face_recognition_resnet_model_v1.dat")

# trích xuất đặc trưng
def get_face_embedding(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = detector(gray)

    if len(faces) == 0:
        return None

    shape = predictor(gray, faces[0])    # lấy vị trí khuôn mặt đầu tiên
    
    # trích xuất vector đặc trưng
    face_embedding = facerec.compute_face_descriptor(image, shape)

    return np.array(face_embedding)

def compare_faces(image1, image2, threshold=0.6): # Ngưỡng threshold tùy chọn, ở đây nếu khoảng cách Euclidean < 0.6 thì cùng 1 người
    embedding1 = get_face_embedding(image1)
    embedding2 = get_face_embedding(image2)

    if embedding1 is None:
        return "Ảnh 1 không tìm thấy khuôn mặt"
    if embedding2 is None:
        return "Ảnh 2 không tìm thấy khuôn mặt"

    # Tính khoảng cách Euclidean giữa hai vector
    distance = np.linalg.norm(embedding1 - embedding2)

    if distance < threshold:
        return f"Cùng 1 người (Khoảng cách Euclidean: {distance:.2f})"
    else:
        return f"2 người khác nhau (Khoảng cách Euclidean: {distance:.2f})"

image1 = cv2.imread(r'D:\Edu\Python\StudentID_FaceVerification\student-id-face-matching\api\results\student_card_faces\ThaiTuanIDCard.jpg_face.jpg')
image2 = cv2.imread(r'D:\Edu\Python\StudentID_FaceVerification\student-id-face-matching\api\img\NgocAnh_face.jpg')

result = compare_faces(image1, image2)
print(result)
