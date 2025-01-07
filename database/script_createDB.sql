CREATE TABLE Users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    account_id TEXT UNIQUE NOT NULL,    -- Tài khoản (MSV, mã giám thị, mã admin)
    password TEXT NOT NULL,             -- Mật khẩu
    role TEXT CHECK (role IN ('student', 'proctor', 'admin')) NOT NULL,  -- Phân quyền
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
    student_photo BLOB,                 -- Ảnh thẻ sinh viên (dạng BLOB để lưu ảnh)
    face_photo BLOB                     -- Ảnh khuôn mặt sinh viên (dạng BLOB để lưu ảnh)
);

CREATE TABLE Proctors (
    proctor_id INTEGER PRIMARY KEY AUTOINCREMENT,
    proctor_code TEXT UNIQUE NOT NULL,  -- Mã giám thị
    full_name TEXT NOT NULL,            -- Họ và tên
    department TEXT NOT NULL,           -- Đơn vị (Khoa/Bộ môn)
    phone_number TEXT,                  -- Số điện thoại
    email TEXT                          -- Email
);
