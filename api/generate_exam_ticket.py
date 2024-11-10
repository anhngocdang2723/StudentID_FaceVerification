# generate_exam_ticket.py
import os

def generate_exam_ticket(student_name, student_msv, exam_name, exam_code, seat_position, output_dir="tickets"):
    """
    Hàm để tạo phiếu thi cho sinh viên.
    
    :param student_name: Họ tên sinh viên.
    :param student_msv: Mã sinh viên.
    :param exam_name: Tên môn thi.
    :param exam_code: Mã khóa thi.
    :param seat_position: Vị trí ngồi thi (1-20).
    :param output_dir: Thư mục lưu phiếu thi, mặc định là "tickets".
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    ticket_info = f"""
    ---------------------------------
           PHIẾU DỰ THI
    ---------------------------------
    Tên sinh viên: {student_name}
    Mã sinh viên: {student_msv}
    Tên môn thi: {exam_name}
    Mã khóa: {exam_code}
    Vị trí ngồi: {seat_position} (1-20)
    ---------------------------------
    """
    
    # Lưu phiếu thi vào file txt với mã hóa utf-8
    ticket_filename = f"{student_msv}_exam_ticket.txt"
    ticket_path = os.path.join(output_dir, ticket_filename)
    
    with open(ticket_path, "w", encoding="utf-8") as f:  # Thêm encoding="utf-8"
        f.write(ticket_info)
    
    print(f"Phiếu thi đã được tạo và lưu tại: {ticket_path}")
    return ticket_path
