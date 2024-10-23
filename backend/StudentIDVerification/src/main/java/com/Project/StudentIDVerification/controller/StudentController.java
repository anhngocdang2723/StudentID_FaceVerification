package com.Project.StudentIDVerification.controller;

import com.Project.StudentIDVerification.model.Student;
import com.Project.StudentIDVerification.service.StudentService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

@RestController
public class StudentController {

    @Autowired
    private StudentService studentService;

    // Endpoint để lấy danh sách sinh viên
    @GetMapping("/students")
    public List<Student> getAllStudents() {
        return studentService.getAllStudents();
    }
}