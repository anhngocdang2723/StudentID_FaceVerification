package com.personal_project.exam_management_system.service;

import com.personal_project.exam_management_system.entity.Student;
import com.personal_project.exam_management_system.repository.StudentRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.Collections;
import java.util.List;
import java.util.Optional;

@Service
public class StudentService {

    @Autowired
    private StudentRepository studentRepository;

    public List<Student> findAllStudents() {
        return studentRepository.findAll();
    }

    public Student findStudentByStudentCode(String studentCode) {
        return studentRepository.findByStudentCode(studentCode).orElse(null);
    }

    public List<Student> findStudentsByStudentCode(String studentCode) {
        return studentRepository.findByStudentCode(studentCode)
                .map(Collections::singletonList)
                .orElse(Collections.emptyList());
    }

    public List<Student> findByFullName(String fullName) {
        return studentRepository.findByFullNameContainingIgnoreCase(fullName);
    }

    public List<Student> findByClassName(String className) {
        return studentRepository.findByClassName(className);
    }

    public List<Student> findByStatus(Student.Status status) {
        return studentRepository.findByStatus(status);
    }

    public void save(Student student) {
        studentRepository.save(student);
    }

    public void updateStudent(Student student) {
        studentRepository.save(student);
    }
}
