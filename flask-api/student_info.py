import sqlite3
from db_connect import connect_db

def get_student_list(session_code):
    conn = connect_db()
    if not conn:
        print("Không thể kết nối đến cơ sở dữ liệu.")
        return {"error": "Không thể kết nối đến cơ sở dữ liệu."}

    try:
        cursor = conn.cursor()

        # Truy vấn mã sinh viên từ bảng ExamSessions
        query = "SELECT student_codes FROM ExamSessions WHERE session_code = ?"
        cursor.execute(query, (session_code,))
        result = cursor.fetchone()

        if result:
            student_codes = result[0]
            student_list = student_codes.split(",") if student_codes else []

            if not student_list:
                return {"error": f"Ca thi {session_code} không có sinh viên nào."}

            # Truy vấn thông tin sinh viên từ bảng Students
            placeholders = ','.join('?' for _ in student_list)
            query_students = f"""
                SELECT student_code, full_name, phone_number, face_photo
                FROM Students
                WHERE student_code IN ({placeholders})
            """
            cursor.execute(query_students, student_list)
            student_info_list = cursor.fetchall()

            if student_info_list:
                student_data = []
                for student_code, full_name, phone_number, face_photo in student_info_list:
                    student_data.append({
                        "name": full_name,
                        "student_id": student_code,
                        "phone": phone_number if phone_number else "Chưa cập nhật",
                        "image_url": face_photo if face_photo else "/static/default_avatar.png",
                        "status": "Đang chờ xác thực"
                    })
                return {"student_info_result": {"student_info": student_data}}
            else:
                return {"error": "Không tìm thấy thông tin sinh viên trong danh sách."}
        else:
            return {"error": f"Không tìm thấy ca thi với mã {session_code}."}

    except sqlite3.Error as e:
        return {"error": f"Lỗi truy vấn cơ sở dữ liệu: {e}"}

    finally:
        conn.close()

# Ví dụ sử dụng
# result = get_student_list('EXS001')
# print(result)
