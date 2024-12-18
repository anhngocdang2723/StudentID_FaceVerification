import os
from fpdf import FPDF

def generate_exam_ticket_pdf(student_name, student_msv, exam_name, exam_code, seat_position, output_dir="tickets"):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    FONT_DIR = os.path.join(BASE_DIR, "tickets")
    font_path_regular = os.path.join(FONT_DIR, "Roboto-Regular.ttf")
    font_path_bold = os.path.join(FONT_DIR, "Roboto-Bold.ttf")

    if not os.path.exists(font_path_regular) or not os.path.exists(font_path_bold):
        return {"status": "error", "message": "Font files not found"}

    TICKET_DIR = os.path.join(BASE_DIR, output_dir)
    os.makedirs(TICKET_DIR, exist_ok=True)

    ticket_filename = f"{student_msv}_exam_ticket.pdf"
    ticket_path = os.path.join(TICKET_DIR, ticket_filename)

    pdf = FPDF()
    pdf.add_page()

    try:
        pdf.add_font("Roboto", "", font_path_regular, uni=True)
        pdf.add_font("Roboto", "B", font_path_bold, uni=True)
    except Exception as e:
        print(f"Không thể tải font: {e}")
        pdf.set_font("Arial", "", 12)

    pdf.set_font("Roboto", "B", 16)
    pdf.cell(0, 10, "PHIẾU DỰ THI", ln=True, align="C")
    pdf.ln(10)

    pdf.set_font("Roboto", "", 12)
    pdf.cell(0, 10, f"Tên sinh viên   : {student_name}", ln=True)
    pdf.cell(0, 10, f"Mã sinh viên    : {student_msv}", ln=True)
    pdf.cell(0, 10, f"Tên môn thi     : {exam_name}", ln=True)
    pdf.cell(0, 10, f"Mã khóa         : {exam_code}", ln=True)
    pdf.cell(0, 10, f"Vị trí ngồi     : {seat_position}", ln=True)
    pdf.ln(10)

    pdf.output(ticket_path)

    return {
        "status": "success",
        "message": "Phiếu thi đã được tạo thành công dưới dạng PDF",
        "ticket_file": ticket_path,
        "ticket_info": {
            "Tên sinh viên": student_name,
            "Mã sinh viên": student_msv,
            "Tên môn thi": exam_name,
            "Mã khóa": exam_code,
            "Vị trí ngồi": seat_position
        }
    }

# Ví dụ chạy
# result = generate_exam_ticket_pdf("Nguyễn Văn Ẻ", "215748020110021", "Lập trình Python", "PY123", 5)
# print(result)
