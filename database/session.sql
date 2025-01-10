SELECT 
    es.session_code,
    c.course_name,
    er.address,
    GROUP_CONCAT(s.full_name) AS list_student_names,
    p.full_name AS proctor_name,
    es.exam_date_time,
    es.session_status,
    es.report_file_path
FROM 
    ExamSessions es
JOIN Courses c ON es.course_code = c.course_code
JOIN ExamRooms er ON es.room_code = er.room_code
JOIN Proctors p ON es.proctor_code = p.proctor_code
JOIN Students s ON es.student_codes LIKE '%' || s.student_code || '%'
WHERE es.session_code = 'EXAM001'
GROUP BY es.session_code, c.course_name, er.address, p.full_name, es.exam_date_time, es.session_status, es.report_file_path;
