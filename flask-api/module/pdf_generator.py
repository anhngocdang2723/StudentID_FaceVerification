from fpdf import FPDF
import io
from datetime import datetime

class PDF(FPDF):
    def header(self):
        # Add Unicode font
        self.add_font('DejaVuSans', '', 'flask-api/font/DejaVuSans.ttf', uni=True)
        self.add_font('DejaVuSans', 'B', 'flask-api/font/DejaVuSans-Bold.ttf', uni=True)

        # Header with logo and title
        self.set_font('DejaVuSans', 'B', 15)
        self.cell(0, 10, 'BÁO CÁO ĐIỂM DANH', ln=True, align='C')
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font('DejaVuSans', '', 8)
        # Add page number
        self.cell(0, 10, f'Trang {self.page_no()}/{{nb}}', align='C')

    def chapter_title(self, title):
        self.set_font('DejaVuSans', 'B', 12)
        self.cell(0, 10, title, ln=True, align='C')
        self.ln(10)

    def chapter_body(self, body):
        self.set_font('DejaVuSans', '', 12)
        self.multi_cell(0, 10, body)
        self.ln()

def generate_pdf(session_code, student_info):
    pdf = PDF()
    pdf.alias_nb_pages()
    pdf.add_page()

    # Session info
    pdf.set_font('DejaVuSans', 'B', 12)
    pdf.cell(0, 10, f"Mã ca thi: {session_code}", ln=True)
    pdf.cell(0, 10, f"Thời gian: {datetime.now().strftime('%d/%m/%Y %H:%M')}", ln=True)
    pdf.cell(0, 10, f"Số lượng sinh viên: {len(student_info)}", ln=True)
    pdf.ln(10)

    # Table header
    pdf.set_fill_color(200, 200, 200)
    pdf.cell(70, 10, "Họ và tên", border=1, fill=True)
    pdf.cell(40, 10, "Mã sinh viên", border=1, fill=True)
    pdf.cell(40, 10, "Trạng thái", border=1, fill=True)
    pdf.cell(40, 10, "Thời gian", border=1, fill=True)
    pdf.ln()

    # Table content
    pdf.set_font('DejaVuSans', '', 11)
    for student in student_info:
        # Set color based on status
        if student["status"] == "Đã điểm danh":
            pdf.set_text_color(0, 100, 0)
        else:
            pdf.set_text_color(200, 0, 0)

        pdf.cell(70, 10, student["name"], border=1)
        pdf.cell(40, 10, student["student_id"], border=1)
        pdf.cell(40, 10, student["status"], border=1)
        pdf.cell(40, 10, student.get("time", ""), border=1)
        pdf.ln()

        # Reset text color
        pdf.set_text_color(0, 0, 0)

    # Summary statistics
    pdf.ln(10)
    total = len(student_info)
    present = sum(1 for s in student_info if s["status"] == "Đã điểm danh")
    absent = total - present

    pdf.set_font('DejaVuSans', 'B', 11)
    pdf.cell(0, 10, f"Thống kê:", ln=True)
    pdf.set_font('DejaVuSans', '', 11)
    pdf.cell(0, 10, f"- Tổng số sinh viên: {total}", ln=True)
    pdf.cell(0, 10, f"- Đã điểm danh: {present}", ln=True)
    pdf.cell(0, 10, f"- Vắng mặt: {absent}", ln=True)

    # Generate PDF in memory
    try:
        # Get PDF as bytes
        pdf_bytes = pdf.output(dest='S').encode('latin-1')

        # Create BytesIO object and write bytes
        pdf_stream = io.BytesIO()
        pdf_stream.write(pdf_bytes)
        pdf_stream.seek(0)

        return pdf_stream

    except Exception as e:
        print(f"PDF Generation Error: {str(e)}")
        raise

    return pdf_stream
