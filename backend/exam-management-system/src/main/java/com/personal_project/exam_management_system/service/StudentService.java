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
        // Debugging: Kiểm tra mã sinh viên đang được tìm kiếm
        System.out.println("Searching for student with code: " + studentCode);

        // Sử dụng Optional để tránh lỗi NullPointerException
        Student student = studentRepository.findByStudentCode(studentCode).orElse(null);

        // Debugging: Kiểm tra xem có sinh viên không
        System.out.println("Student found: " + student);

        return student;
    }
}
