package com.personal_project.exam_management_system.repository;

import com.personal_project.exam_management_system.entity.Student;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;
import java.util.Optional;

public interface StudentRepository extends JpaRepository<Student, Long> {
    // Phương thức tìm kiếm sinh viên theo mã sinh viên
    Optional<Student> findByStudentCode(String studentCode);

    // Phương thức tìm kiếm sinh viên theo tên
    List<Student> findByFullNameContainingIgnoreCase(String fullName);

    // Phương thức tìm kiếm sinh viên theo lớp học
    List<Student> findByClassName(String className);

    // Phương thức tìm kiếm sinh viên theo trạng thái
    List<Student> findByStatus(Student.Status status);
}

