import os
import cv2
import unidecode
from flask import Flask, request, jsonify, send_file
import numpy as np
import random
from flask_cors import CORS
from module.db_update import update_images
from db_connect import connect_db
from module.face_detection import detect_and_crop_face
from module.student_info import get_student_list
from module.recognition import verify_faces
from module.generate_ticket import generate_exam_ticket, generate_random_string
from module.pdf_generator import generate_pdf

app = Flask(__name__)
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
        student_id = request.form.get('student_id')
        student_name = request.form.get('student_name')

        if not student_image_path or not personal_image_file or not student_id:
            return jsonify({'error': 'Cần cung cấp đủ cả đường dẫn ảnh sinh viên, ảnh cá nhân và mã sinh viên.'}), 400

        result = verify_faces(personal_image_file, student_image_path)

        if 'error' in result:
            return jsonify({'error': result['error']}), 500

        if result['match']:
            seating_position = random.randint(1, 20)
            exam_account = generate_random_string()
            exam_password = generate_random_string()

            ticket_directory = r"D:\\Edu\\Python\\StudentID_FaceVerification\\student-id-face-matching\\results\\tickets"

            if not os.path.exists(ticket_directory):
                os.makedirs(ticket_directory)

            ticket_path = generate_exam_ticket(student_name, student_id, ticket_directory)

            return jsonify({
                'match': True,
                'exam_ticket_path': ticket_path,
                'student_name': student_name,
                'student_id': student_id,
                'seating_position': seating_position,
                'exam_account': exam_account,
                'exam_password': exam_password
            })
        else:
            return jsonify({'match': False})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/generate-pdf/', methods=['POST'])
def generate_pdf_route():
    try:
        data = request.get_json()
        session_code = data.get('sessionCode')
        student_info = data.get('studentInfo')

        if not session_code or not student_info:
            return jsonify({'error': 'Missing required data'}), 400

        pdf_stream = generate_pdf(session_code, student_info)

        filename = f'bao_cao_ca_thi-{session_code}.pdf'

        return send_file(
            pdf_stream,
            as_attachment=True,
            attachment_filename=filename,
            mimetype='application/pdf'
        )

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000)