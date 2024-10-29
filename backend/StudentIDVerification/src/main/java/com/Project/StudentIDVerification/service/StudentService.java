// StudentService.java
package com.Project.StudentIDVerification.service;

import com.Project.StudentIDVerification.model.Student;
import com.Project.StudentIDVerification.repository.StudentRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Optional;

@Service
public class StudentService {

    @Autowired
    private StudentRepository studentRepository;

    public List<Student> getAllStudents(Boolean status) {
        return studentRepository.findByStatus(status);
    }

    public long getTotalStudents() {
        return studentRepository.countByStatus(true);
    }

    public Optional<Student> getStudentById(String id) {
        return studentRepository.findById(id);
    }

    public Student createStudent(Student student) {
        return studentRepository.save(student);
    }

    public Student updateStudent(String id, Student studentDetails) {
        Student student = studentRepository.findById(id).orElseThrow(() -> new RuntimeException("Student not found"));
        student.setStdId(studentDetails.getStdId());
        student.setStdName(studentDetails.getStdName());
        student.setStdDob(studentDetails.getStdDob());
        student.setStdClass(studentDetails.getStdClass());
        student.setStdFaculty(studentDetails.getStdFaculty());
        student.setStdCourse(studentDetails.getStdCourse());
        student.setStdEmail(studentDetails.getStdEmail());
        student.setStdPhone(studentDetails.getStdPhone());
        student.setExamResults(studentDetails.getExamResults());
        student.setStatus(studentDetails.isStatus());
        return studentRepository.save(student);
    }

    public void deleteStudent(String id) {
        studentRepository.deleteById(id);
    }
}
