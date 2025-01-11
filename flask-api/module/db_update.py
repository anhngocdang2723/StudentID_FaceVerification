#module.db_update.py

import sqlite3
import os
import unidecode
from db_connect import connect_db

# def enable_wal_mode():
#     conn = connect_db()
#     if conn:
#         try:
#             cursor = conn.cursor()
#             cursor.execute("PRAGMA journal_mode=WAL;")
#             conn.commit()
#             print("Đã kích hoạt chế độ WAL.")
#         except sqlite3.Error as e:
#             print(f"Lỗi khi kích hoạt WAL: {e}")
#         finally:
#             conn.close()

def update_images(student_code, full_name):
    conn = connect_db()
    if not conn:
        print("Không thể kết nối đến cơ sở dữ liệu.")
        return

    try:
        cursor = conn.cursor()

        name_without_accents = unidecode.unidecode(full_name.strip()).replace(" ", "").lower()
        student_code_last_3 = student_code[-3:]

        card_image_filename = f"{name_without_accents}_{student_code_last_3}_card.jpg"
        face_image_filename = f"{name_without_accents}_{student_code_last_3}_face.jpg"

        card_image_path = f"/images/card/{card_image_filename}"
        face_image_path = f"/images/face/{face_image_filename}"

        cursor.execute("""
            UPDATE Students
            SET student_photo = ?, face_photo = ?
            WHERE student_code = ?
        """, (card_image_path, face_image_path, student_code))

        conn.commit()
        print(f"Đã cập nhật ảnh cho sinh viên {student_code}.")

    except sqlite3.Error as e:
        print(f"Lỗi khi cập nhật ảnh: {e}")

    finally:
        conn.close()

# enable_wal_mode()