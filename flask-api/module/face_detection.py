# module.face_detection.py

import cv2
import os
import unidecode
import numpy as np

FACE_FOLDER = r'D:\\Edu\\Python\\StudentID_FaceVerification\\student-id-face-matching\\results\\images\\face'
os.makedirs(FACE_FOLDER, exist_ok=True)

def detect_and_crop_face(image_data, full_name, student_code):
    np_arr = np.frombuffer(image_data, np.uint8)
    img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)

    if len(faces) == 0:
        return None

    x, y, w, h = faces[0]
    face_img = img[y:y+h, x:x+w]

    name_without_accents = unidecode.unidecode(full_name.strip()).replace(" ", "").lower()
    student_code_last_3 = student_code[-3:]
    face_filename = f"{name_without_accents}_{student_code_last_3}_face.jpg"
    face_path = os.path.join(FACE_FOLDER, face_filename)
    cv2.imwrite(face_path, face_img)

    return face_path
