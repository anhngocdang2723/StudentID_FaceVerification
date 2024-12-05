import os
from fpdf import FPDF

def generate_exam_ticket_pdf(student_name, student_msv, exam_name, exam_code, seat_position, output_dir="tickets"):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    # Thư mục chứa font trong 'tickets'
    FONT_DIR = os.path.join(BASE_DIR, "tickets")  # Đảm bảo thư mục fonts đúng
    print(f"FONT_DIR: {FONT_DIR}")

    font_path_regular = os.path.join(FONT_DIR, "Roboto-Regular.ttf")
    font_path_bold = os.path.join(FONT_DIR, "Roboto-Bold.ttf")

    # Kiểm tra xem font có tồn tại không
    if not os.path.exists(font_path_regular) or not os.path.exists(font_path_bold):
        print("Font file(s) not found. Please ensure the fonts are located in the 'tickets/' folder.")
        return {"status": "error", "message": "Font files not found"}

    TICKET_DIR = os.path.join(BASE_DIR, "tickets")
    os.makedirs(TICKET_DIR, exist_ok=True)
    print(f"TICKET_DIR: {TICKET_DIR}")

    ticket_filename = f"{student_msv}_exam_ticket.pdf"
    ticket_path = os.path.join(TICKET_DIR, ticket_filename)
    print(f"Ticket Path: {ticket_path}")

    pdf = FPDF()
    pdf.add_page()

    # Thêm font tùy chỉnh mà không nhúng vào PDF
    try:
        pdf.add_font("Roboto", "", font_path_regular, uni=True)
        pdf.add_font("Roboto", "B", font_path_bold, uni=True)
    except Exception as e:
        print(f"Không thể tải font: {e}")
        pdf.set_font("Arial", "", 12)

    # Tiêu đề với font Bold
    pdf.set_font("Roboto", "B", 16)
    pdf.cell(0, 10, "PHIẾU DỰ THI", ln=True, align="C")
    pdf.ln(10)

    # Nội dung phiếu thi với font Regular
    pdf.set_font("Roboto", "", 12)
    pdf.cell(0, 10, f"Tên sinh viên   : {student_name}", ln=True)
    pdf.cell(0, 10, f"Mã sinh viên    : {student_msv}", ln=True)
    pdf.cell(0, 10, f"Tên môn thi     : {exam_name}", ln=True)
    pdf.cell(0, 10, f"Mã khóa         : {exam_code}", ln=True)
    pdf.cell(0, 10, f"Vị trí ngồi     : {seat_position} (1-20)", ln=True)
    pdf.ln(10)

    # Lưu phiếu thi vào file
    pdf.output(ticket_path)

    return {
        "status": "success",
        "message": "Phiếu thi đã được tạo thành công dưới dạng PDF",
        "ticket_file": ticket_path
    }

# Ví dụ chạy:
result = generate_exam_ticket_pdf("Nguyễn Văn Ẻ", "215748020110022", "Lập trình Python", "PY123", 5)
print(result)
