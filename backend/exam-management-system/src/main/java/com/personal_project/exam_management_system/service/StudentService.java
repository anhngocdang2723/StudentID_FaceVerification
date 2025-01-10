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

    // Phương thức lấy tất cả sinh viên
    public List<Student> findAllStudents() {
        return studentRepository.findAll();  // Lấy tất cả sinh viên
    }

    // Phương thức trả về một sinh viên duy nhất theo mã sinh viên
    public Student findStudentByStudentCode(String studentCode) {
        return studentRepository.findByStudentCode(studentCode).orElse(null);  // Trả về sinh viên duy nhất hoặc null
    }

    // Phương thức trả về danh sách sinh viên theo mã sinh viên
    public List<Student> findStudentsByStudentCode(String studentCode) {
        return studentRepository.findByStudentCode(studentCode)
                .map(Collections::singletonList)  // Nếu tìm thấy, trả về danh sách 1 sinh viên
                .orElse(Collections.emptyList()); // Nếu không tìm thấy, trả về danh sách rỗng
    }

    // Phương thức tìm kiếm thông tin sinh viên theo tên
    public List<Student> findByFullName(String fullName) {
        return studentRepository.findByFullNameContainingIgnoreCase(fullName);
    }

    // Phương thức tìm kiếm thông tin sinh viên theo lớp học
    public List<Student> findByClassName(String className) {
        return studentRepository.findByClassName(className);
    }

    // Phương thức tìm kiếm sinh viên theo trạng thái
    public List<Student> findByStatus(Student.Status status) {
        return studentRepository.findByStatus(status);
    }

    public void save(Student student) {
        studentRepository.save(student);
    }

    // Cập nhật thông tin sinh viên
    public void updateStudent(Student student) {
        studentRepository.save(student); // Lưu lại thông tin đã chỉnh sửa
    }
}
