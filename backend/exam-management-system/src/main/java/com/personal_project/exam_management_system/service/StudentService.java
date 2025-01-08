package com.personal_project.exam_management_system.service;

import com.personal_project.exam_management_system.entity.Student;
import com.personal_project.exam_management_system.repository.StudentRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

@Service
public class StudentService {

    @Autowired
    private StudentRepository studentRepository;

    // Phương thức tìm kiếm thông tin sinh viên theo mã sinh viên
    public Student findByStudentCode(String studentCode) {
        return studentRepository.findByStudentCode(studentCode)
                .orElseThrow(() -> new RuntimeException("Student not found with code: " + studentCode));
    }
}
