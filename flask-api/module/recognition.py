import face_recognition
from PIL import Image, ImageEnhance
import numpy as np
import cv2
import io
import os

def crop_face(image_array, margin=0.2):
    """Detect and crop face from image"""
    face_locations = face_recognition.face_locations(image_array)
    if not face_locations:
        raise ValueError("No face detected")

    top, right, bottom, left = face_locations[0]
    height = bottom - top
    width = right - left

    margin_y = int(height * margin)
    margin_x = int(width * margin)

    crop_top = max(top - margin_y, 0)
    crop_bottom = min(bottom + margin_y, image_array.shape[0])
    crop_left = max(left - margin_x, 0)
    crop_right = min(right + margin_x, image_array.shape[1])

    return image_array[crop_top:crop_bottom, crop_left:crop_right]

def standardize_image(image_array, target_size=(512, 512)):
    """Standardize image size and format"""
    image = Image.fromarray(image_array)
    image = image.resize(target_size, Image.Resampling.LANCZOS)
    return np.array(image)

def enhance_image(image_array):
    """Enhance image quality"""
    image = Image.fromarray(image_array)

    # Enhance contrast
    contrast = ImageEnhance.Contrast(image)
    image = contrast.enhance(1.2)

    # Enhance sharpness
    sharpness = ImageEnhance.Sharpness(image)
    image = sharpness.enhance(1.5)

    # Convert to CV2 format for denoising
    cv_image = np.array(image)
    denoised = cv2.fastNlMeansDenoisingColored(cv_image)

    return denoised

def verify_faces(filePersonalImage, studentImagePathInDB, threshold=0.50006):
    try:
        # Process personal image
        filePersonalImage.seek(0)
        personal_image = face_recognition.load_image_file(io.BytesIO(filePersonalImage.read()))
        personal_face = crop_face(personal_image)
        personal_face = standardize_image(personal_face)
        personal_face = enhance_image(personal_face)

        # Process student ID image
        base_path = r"D:\\Edu\\Python\\StudentID_FaceVerification\\student-id-face-matching\\results"
        student_path = os.path.join(base_path, studentImagePathInDB.lstrip('/'))
        student_image = face_recognition.load_image_file(student_path)
        student_face = crop_face(student_image)
        student_face = standardize_image(student_face)
        student_face = enhance_image(student_face)

        # Compare faces
        personal_encoding = face_recognition.face_encodings(personal_face)[0]
        student_encoding = face_recognition.face_encodings(student_face)[0]

        face_distances = face_recognition.face_distance([student_encoding], personal_encoding)
        face_distance = face_distances[0]
        confidence = round((1 - face_distance) * 100, 2)
        matches = face_recognition.compare_faces([student_encoding], personal_encoding, tolerance=threshold)

        return {
            'match': bool(matches[0]),
            'confidence': confidence,
            'face_distance': float(face_distance),
            'threshold': threshold
        }

    except Exception as e:
        return {'error': str(e)}

# Test
# filePersonalImage = open(r"api/(delete)img/NgocAnh_face.jpg", "rb")
# filePersonalImage = open(r"api/(delete)img/ThaiTuan_face.jpg", "rb")
# studentImagePathInDB = "/images/face/dangngocanh_333_face.jpg"

# result = verify_faces(filePersonalImage, studentImagePathInDB)
# print(result)

# filePersonalImage.close()
