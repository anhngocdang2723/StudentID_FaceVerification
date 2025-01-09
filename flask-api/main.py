import os
import cv2
import unidecode
from flask import Flask, request, jsonify
import numpy as np
from flask_cors import CORS  # Import CORS
from db_update import update_images  # Ensure this is imported correctly

# Enable CORS for all domains
app = Flask(__name__)
CORS(app)

CARD_FOLDER = r'D:\\Edu\\Python\\StudentID_FaceVerification\\student-id-face-matching\\results\\image\\card'
FACE_FOLDER = r'D:\\Edu\\Python\\StudentID_FaceVerification\\student-id-face-matching\\results\\image\\face'

os.makedirs(CARD_FOLDER, exist_ok=True)
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

@app.route('/upload-photo/', methods=['POST'])
def upload_photo():
    if 'studentPhoto' not in request.files:
        return jsonify({'error': 'No photo provided'}), 400

    full_name = request.form.get('fullName', '').strip()
    student_code = request.form.get('studentCode', '').strip()

    if not full_name or not student_code:
        return jsonify({'error': 'Invalid student name or student code'}), 400

    photo = request.files['studentPhoto']
    image_data = photo.read()

    card_filename = f"{unidecode.unidecode(full_name).replace(' ', '').lower()}_{student_code[-3:]}_card.jpg"
    card_path = os.path.join(CARD_FOLDER, card_filename)

    with open(card_path, 'wb') as f:
        f.write(image_data)

    face_image_path = detect_and_crop_face(image_data, full_name, student_code)

    if face_image_path is None:
        return jsonify({'error': 'No face detected in the image'}), 400

    update_images(student_code, full_name)  # Update images in the database

    return jsonify({
        'message': 'Photo uploaded and face cropped successfully',
        'card_image_path': card_path,
        'face_image_path': face_image_path
    }), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
