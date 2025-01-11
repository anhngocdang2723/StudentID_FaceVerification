import sqlite3

DB_PATH = r'D:\\Edu\\Python\\StudentID_FaceVerification\\student-id-face-matching\\database\\exam_system.db'

def connect_db(db_path=DB_PATH):
    try:
        conn = sqlite3.connect(db_path)
        return conn
    except sqlite3.Error as e:
        print(f"Lỗi kết nối cơ sở dữ liệu: {e}")
        return None
