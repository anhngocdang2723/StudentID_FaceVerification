import sqlite3
import os
import unidecode

# Đường dẫn đến cơ sở dữ liệu SQLite
DB_PATH = r'D:\Edu\Python\StudentID_FaceVerification\student-id-face-matching\database\exam_system.db'

# Hàm kích hoạt chế độ WAL (Write-Ahead Logging)
def enable_wal_mode():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("PRAGMA journal_mode=WAL;")
    conn.commit()
    conn.close()

# Hàm cập nhật đường dẫn ảnh vào cơ sở dữ liệu
def update_images(student_code, full_name):
    conn = sqlite3.connect(DB_PATH, timeout=10.0)  # Tăng thời gian timeout lên 10 giây
    cursor = conn.cursor()

    # Chuẩn hóa tên sinh viên
    name_without_accents = unidecode.unidecode(full_name.strip()).replace(" ", "").lower()
    student_code_last_3 = student_code[-3:]

    # Tạo tên file ảnh
    card_image_filename = f"{name_without_accents}_{student_code_last_3}_card.jpg"
    face_image_filename = f"{name_without_accents}_{student_code_last_3}_face.jpg"

    # Sử dụng đường dẫn tương đối cho ảnh
    card_image_path = f"\\images\\card\\{card_image_filename}"  # Dùng dấu \ để lưu đường dẫn
    face_image_path = f"\\images\\face\\{face_image_filename}"  # Dùng dấu \ để lưu đường dẫn

    # Nếu bạn muốn sử dụng dấu "/" thay vì "\", chỉ cần thay đổi thành "/"
    # card_image_path = f"/card/{card_image_filename}"
    # face_image_path = f"/face/{face_image_filename}"

    # Cập nhật đường dẫn ảnh vào cơ sở dữ liệu
    cursor.execute("""
        UPDATE Students
        SET student_photo = ?, face_photo = ?
        WHERE student_code = ?
    """, (card_image_path, face_image_path, student_code))

    conn.commit()
    conn.close()

# Kích hoạt chế độ WAL một lần khi khởi động ứng dụng
enable_wal_mode()
