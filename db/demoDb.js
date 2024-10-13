//////////Sinh viên
Students = {
    "_id": "tự tạo",
    "std_id": "msv",
    "std_name": "tên sv",
    "std_dob": "ngày sinh",
    "std_class": "lớp",
    "std_faculty": "khoa/viện/trường",
    "std_course": "khoá học",
    "std_email": "email",
    "std_phone": "sdt",
    "exam_results": {
        "exam_id": "mã môn",
        "exam_results": "điểm"
    }
}

//////////Giám thị
Invigilators = {
    "_id": "tự tạo",
    "invigilator_id": "mã giám thị",
    "invigilator_name": "tên giám thị",
    "invigilator_phone": "sdt",
    "invigilator_email": "email"
}

/////////Kỳ thi
Exams = {
    "_id": "tự tạo",
    "exam_id": "mã kỳ thi",
    "exam_name": "tên môn",
    "exam_date": "ngày thi",
    "exam_room": "phòng thi",
    "invigilator_id": "mã giám thị",
    //"invigilator_name": "tên giám thị",
}

//////////Phòng thi
ExamRooms = {
    "_id": "tự tạo",
    "room_id": "mã phòng",
    "capacity": xx, //số lượng sinh viên tối đa
    "exam_id": "mã kỳ thi lấy ở trên",
    "invigilator_id": "mã giám thị",
    "students": [ //danh sách sinh viên thực tế trong phòng thi
        {
            "std_id": "msv",
        },
        {
            "std_id": "msv",
        }
    ],
    "cameras": [ //danh sách các camera giám sát trong phòng
        {
            "camera_id": "mã cam",
            "location": "vị trí cam"
        },
        {
            "camera_id": "mã cam",
            "location": "vị trí cam"
        }
    ],
    "computers": [ // danh sách máy tính trong phòng thi
        {
            "computer_id": "mã máy tính",
            "status": "đang sử dụng" // có thể là 'đang sử dụng', 'trống', hoặc 'bị hỏng'
        },
        {
            "computer_id": "mã máy tính",
            "status": "trống" // máy tính này chưa được sử dụng
        }
    ]
}

//////////Sinh viên tham gia thi
//////////////Danh sách này sẽ được xuất ra thành excel để đối chiếu với thông tin trên thẻ sinh viên
ExamParticipants = {
    "_id": "tự tạo",
    "exam_id": "mã kỳ thi",
    "std_id": "msv",
    //"std_name": "tên sv",
    "exam_room": "mã phòng",
    "invigilator_id": "mã giám thị"
}

//////////Đối chiếu khuôn mặt
FaceVerification = {
    "_id": "tự tạo",
    "std_id": "msv",
    "room_id": "mã phòng",
    "card_image": "ảnh thẻ",
    "face_image": "ảnh khuôn mặt từ thẻ",
    "face_camera": "ảnh khuôn mặt từ camera",
    "face_result": "kết quả đối chiếu", //true/false
    "verification_time": "thời gian đối chiếu",
    ///nếu true thì in phiếu thi
    "exam_ticket": {
        "std_id": "msv",
        "exam_id": "mã môn",
        "username": "tài khoản thi",
        "password": "mật khẩu thi",
        "computers_id": "vị trí ngồi",
        "issued_at": "thời gian cấp phiếu thi"
    }
}
/////Ngân hàng câu hỏi /// Bổ sung sau
Questions = {
    "_id": "tự tạo",
    "question_id": "mã câu hỏi",
    "question_text": "nội dung câu hỏi",
    "options": [
        {
            "option_id": "mã đáp án",
            "option_text": "nội dung đáp án",
            "is_correct": true/false
        }
    ],
    "marks": "số điểm của câu hỏi",
    "difficulty": "độ khó của câu hỏi",  // Đánh giá độ khó (dễ, trung bình, khó)
    "created_at": "thời gian tạo",
    "updated_at": "thời gian cập nhật" 
}

/////Đề thi cho sinh viên, lấy từ ngân hàng câu hỏi
ExamQuestions = {
    "_id": "tự tạo",
    "exam_id": "mã kỳ thi",
    "question_id": "mã câu hỏi"
}


/////Kết quả thi 
ExamResults = {
    "_id": "tự tạo",
    "std_id": "msv",
    "exam_id": "mã kỳ thi",
    "room_id": "mã phòng",
    "exam_result": "điểm",
    "exam_time": "thời gian làm bài thi",
    "exam_status": "đạt/không đạt",
    "exam_remaks": "ghi chú"
}

/////Log
Logs = {
    "_id": "tự tạo",
    "exam_id": "mã kỳ thi",
    "student_id": "msv",
    "start_time": "thời gian bắt đầu xác thực",
    "end_time": "thời gian sv rời phòng",
    "video_clips": [ 
        {
            "clip_id": "mã video",
            "clip_path": "đường dẫn đến video",
            "timestamp": "thời gian ghi lại"
        }
    ],
    "images": [
        {
            "image_id": "mã ảnh",
            "image_path": "đường dẫn đến ảnh",
            "timestamp": "thời gian ghi lại"
        }
    ],
    "metadata": { // Thông tin bổ sung
        "recorded_by": "người ghi chú (giám thị, admin)",
        "comments": "ghi chú thêm nếu cần"
    }
}

