import os
import cv2
import unidecode
from flask import Flask, request, jsonify, render_template
import numpy as np
from flask_cors import CORS
from db_update import update_images
from db_connect import connect_db
from face_detection import detect_and_crop_face
from student_info import get_student_list
from recognition import verify_faces

app = Flask(__name__)
# CORS(app)
CORS(app, resources={r"/*": {"origins": "*"}})


CARD_FOLDER = r'D:\\Edu\\Python\\StudentID_FaceVerification\\student-id-face-matching\\results\\images\\card'

os.makedirs(CARD_FOLDER, exist_ok=True)

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

    update_images(student_code, full_name)

    return jsonify({
        'message': 'Photo uploaded and face cropped successfully',
        'card_image_path': card_path,
        'face_image_path': face_image_path
    }), 200

@app.route('/get-student-info/', methods=['POST'])
def get_student_info():
    session_code = request.json.get('sessionCode', '').strip()

    if not session_code:
        return jsonify({'error': 'Invalid session code'}), 400

    student_info_result = get_student_list(session_code)

    if student_info_result.get("student_info_result", {}).get("student_info"):
        return jsonify({
            'message': 'Danh sách sinh viên thành công',
            'student_info': student_info_result['student_info_result']['student_info']
        }), 200
    else:
        return jsonify({'error': student_info_result.get('error', 'Không tìm thấy thông tin sinh viên hoặc ca thi')}), 404
    # curl -X POST http://127.0.0.1:8000/get-student-info/ -H "Content-Type: application/json" -d "{\"sessionCode\": \"EXS001\"}"

@app.route('/verify-face/', methods=['POST'])
def verify_face():
    try:
        student_image_path = request.form.get('student_image_path')
        personal_image_file = request.files['filePersonalImage']

        # print("Ảnh sinh viên trong DB:", student_image_path)
        # print("Ảnh thực tế:", personal_image_file)

        if not student_image_path or not personal_image_file:
            return jsonify({'error': 'Cần cung cấp đủ cả đường dẫn ảnh sinh viên và ảnh cá nhân.'}), 400

        result = verify_faces(personal_image_file, student_image_path)

        if 'error' in result:
            return jsonify({'error': result['error']}), 500

        if result['match']:
            return jsonify({'match': True})
        else:
            return jsonify({'match': False})

    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000)