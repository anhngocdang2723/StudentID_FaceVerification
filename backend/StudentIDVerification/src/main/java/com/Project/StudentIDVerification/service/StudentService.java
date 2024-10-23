package com.Project.StudentIDVerification.service;

import com.Project.StudentIDVerification.model.Student;
import com.Project.StudentIDVerification.repository.StudentRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class StudentService {

    @Autowired
    private StudentRepository studentRepository;

    // Phương thức để lấy tất cả sinh viên
    public List<Student> getAllStudents() {
        return studentRepository.findAll();
    }
}