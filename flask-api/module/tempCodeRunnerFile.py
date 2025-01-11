from fpdf import FPDF
import io

class PDF(FPDF):
    def header(self):
        # Thêm font Unicode đã tải xuống
        self.add_font('DejaVuSans', '', r'flask-api\font\dejavu-sans.book.ttf', uni=True)
        self.set_font('DejaVuSans', 'B', 12)

    def footer(self):
        self.set_font('DejaVuSans', 'I', 8)

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
    pdf.add_page()

    # Tiêu đề
    pdf.cell(200, 10, txt=f"Báo cáo Ca thi: {session_code}", ln=True, align='C')
    pdf.ln(10)

    # Header bảng
    pdf.cell(60, 10, txt="Họ tên", border=1)
    pdf.cell(50, 10, txt="Mã sinh viên", border=1)
    pdf.cell(40, 10, txt="Trạng thái", border=1)
    pdf.ln()

    # Dữ liệu sinh viên
    for student in student_info:
        pdf.cell(60, 10, txt=student["name"], border=1)
        pdf.cell(50, 10, txt=student["student_id"], border=1)
        pdf.cell(40, 10, txt=student["status"], border=1)
        pdf.ln()

    # Xuất file PDF vào bộ nhớ
    pdf_stream = io.BytesIO()
    pdf.output(pdf_stream)
    pdf_stream.seek(0)

    return pdf_stream
