package com.personal_project.exam_management_system.repository;

import com.personal_project.exam_management_system.entity.Student;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;
import java.util.Optional;

public interface StudentRepository extends JpaRepository<Student, Long> {
    Optional<Student> findByStudentCode(String studentCode);

    List<Student> findByFullNameContainingIgnoreCase(String fullName);

    List<Student> findByClassName(String className);

    List<Student> findByStatus(Student.Status status);
}

