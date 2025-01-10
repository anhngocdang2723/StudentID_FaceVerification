CREATE TABLE Users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    account_id TEXT UNIQUE NOT NULL,    -- Tài khoản (MSV, mã giám thị, mã admin)
    password TEXT NOT NULL,             -- Mật khẩu
    role_id INTEGER, 
	FOREIGN KEY (role_id) REFERENCES Role (role_id)  -- Phân quyền
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP  -- Ngày tạo tài khoản
);

CREATE TABLE Students (
    student_id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_code TEXT UNIQUE NOT NULL,  -- Mã sinh viên
    full_name TEXT NOT NULL,            -- Họ và tên
    department TEXT NOT NULL,           -- Đơn vị (Khoa/Viện)
    class_name TEXT NOT NULL,           -- Lớp học
    cohort TEXT NOT NULL,               -- Khoá học (2021-2026)
    gender TEXT CHECK (gender IN ('Male', 'Female')) NOT NULL,  -- Giới tính
    date_of_birth DATE NOT NULL,        -- Ngày sinh
    phone_number TEXT,                  -- Số điện thoại
    email TEXT,                         -- Email
    status TEXT CHECK (status IN ('Active', 'Graduated', 'Inactive')) DEFAULT 'Active', -- Trạng thái sinh viên
    student_photo TEXT,                 -- Ảnh thẻ sinh viên 
    face_photo TEXT                     -- Ảnh khuôn mặt sinh viên 
);

CREATE TABLE Proctors (
    proctor_id INTEGER PRIMARY KEY AUTOINCREMENT,
    proctor_code TEXT UNIQUE NOT NULL,  -- Mã giám thị
    full_name TEXT NOT NULL,            -- Họ và tên
    department TEXT NOT NULL,           -- Đơn vị (Khoa/Bộ môn)
    phone_number TEXT,                  -- Số điện thoại
    email TEXT                          -- Email
);

CREATE TABLE Role (
    role_id INTEGER PRIMARY KEY AUTOINCREMENT,
    role_name TEXT NOT NULL UNIQUE
);

INSERT INTO Role (role_name) VALUES ('Student');
INSERT INTO Role (role_name) VALUES ('Proctor');
INSERT INTO Role (role_name) VALUES ('Admin');


CREATE TABLE Courses (
    course_code TEXT PRIMARY KEY,           -- Mã học phần
    course_name TEXT NOT NULL,              -- Tên học phần
    credit_hours INTEGER NOT NULL,         -- Số tín chỉ
    description TEXT,                       -- Mô tả học phần (optional)
    department TEXT NOT NULL,               -- Khoa/Bộ môn
    semester TEXT,                          -- Học kỳ (optional)
    year INTEGER                             -- Năm học (optional)
);
CREATE TABLE ExamRooms (
    room_code TEXT PRIMARY KEY,             -- Mã phòng
    address TEXT NOT NULL,                  -- Địa chỉ
    max_capacity INTEGER NOT NULL           -- Số lượng tối đa
);
CREATE TABLE ExamSessions (
    session_code TEXT PRIMARY KEY,          -- Mã ca thi
    course_code TEXT NOT NULL,              -- Mã học phần (tham chiếu đến bảng Courses)
    room_code TEXT NOT NULL,                -- Mã phòng thi (tham chiếu đến bảng ExamRooms)
    student_codes TEXT,                     -- Danh sách mã SV (Lưu dưới dạng chuỗi hoặc JSON)
    proctor_code TEXT NOT NULL,             -- Mã Giám thị (tham chiếu đến bảng Proctors)
    exam_date_time TEXT NOT NULL,           -- Thời gian ca thi
    session_status TEXT NOT NULL,           -- Trạng thái ca thi (e.g. "Scheduled", "Completed", etc.)
    report_file_path TEXT                   -- Báo cáo (Đường dẫn đến file PDF hoặc loại tệp khác)
);

ALTER TABLE Courses ADD COLUMN id INTEGER PRIMARY KEY AUTOINCREMENT;
