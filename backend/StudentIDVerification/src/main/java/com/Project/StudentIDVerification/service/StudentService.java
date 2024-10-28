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

    // Lấy tất cả sinh viên
    public List<Student> getAllStudents() {
        List<Student> students = studentRepository.findAll();
        System.out.println("Danh sách sinh viên: " + students); // In ra danh sách để kiểm tra
        return students;
    }


    // Lấy thông tin sinh viên theo ID
    public Optional<Student> getStudentById(String id) {
        return studentRepository.findById(id);
    }

    // Tạo mới sinh viên
    public Student createStudent(Student student) {
        return studentRepository.save(student);
    }

    // Cập nhật thông tin sinh viên
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

    // Xóa sinh viên theo ID
    public void deleteStudent(String id) {
        studentRepository.deleteById(id);
    }
}
