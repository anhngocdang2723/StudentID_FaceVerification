import random
import string
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os

def generate_random_string(length=8):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for i in range(length))

def generate_exam_ticket(student_name, student_id, output_path):
    seating_position = random.randint(1, 20)
    exam_account = generate_random_string()
    exam_password = generate_random_string()

    ticket_filename = f"{student_id}_exam_ticket.pdf"
    ticket_path = os.path.join(output_path, ticket_filename)

    c = canvas.Canvas(ticket_path, pagesize=letter)
    width, height = letter

    c.setFont("Helvetica-Bold", 18)
    c.drawString(200, height - 40, "Phiếu Thi Sinh Viên")

    c.setFont("Helvetica", 12)
    c.drawString(50, height - 80, f"Tên Sinh Viên: {student_name}")
    c.drawString(50, height - 100, f"Mã Sinh Viên: {student_id}")
    c.drawString(50, height - 120, f"Vị trí ngồi: {seating_position}")
    c.drawString(50, height - 140, f"Tài khoản thi: {exam_account}")
    c.drawString(50, height - 160, f"Mật khẩu thi: {exam_password}")

    c.save()

    return ticket_path

# def handle_exam_ticket(student_name, student_id):
#     ticket_directory = r"D:\Edu\Python\StudentID_FaceVerification\student-id-face-matching\results\tickets"

#     if not os.path.exists(ticket_directory):
#         os.makedirs(ticket_directory)

#     ticket_path = generate_exam_ticket(student_name, student_id, ticket_directory)

#     return ticket_path

# student_name = "Ngoc Anh"
# student_id = "215748020110333"

# ticket_path = handle_exam_ticket(student_name, student_id)
# print(f"Phiếu thi đã được tạo và lưu tại: {ticket_path}")
