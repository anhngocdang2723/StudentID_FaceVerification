import pandas as pd
from unidecode import unidecode

def read_from_excel(excel_path):
    try:
        df = pd.read_excel(excel_path)
        name_col = None
        msv_col = None
        for col in df.columns:
            if "họ tên" in col.lower():
                name_col = col
            elif "mã sinh viên" in col.lower():
                msv_col = col
        if name_col and msv_col:
            excel_data = []
            for index, row in df.iterrows():
                name = row[name_col]
                msv = row[msv_col]
                if pd.notna(name) and pd.notna(msv):
                    name = unidecode(str(name)).upper()
                    excel_data.append(f"{name} - {msv}")
            return excel_data
        else:
            print("Không tìm thấy cột 'Họ tên' và 'Mã sinh viên'.")
            return []
    except Exception as e:
        print(f"Lỗi khi đọc file Excel: {e}")
        return []

# # Ví dụ sử dụng
# excel_file_path = r"D:\Edu\Python\StudentID_FaceVerification\student-id-face-matching\api\List of candidates\students.xlsx"
# students = read_from_excel(excel_file_path)
# print(students)
