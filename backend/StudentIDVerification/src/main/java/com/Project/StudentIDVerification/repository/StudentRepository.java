package com.Project.StudentIDVerification.repository;

import com.Project.StudentIDVerification.model.Student;
import org.springframework.data.mongodb.repository.MongoRepository;

import java.util.Optional;

public interface StudentRepository extends MongoRepository<Student, String> {
    Optional<Student> findByStdId(String stdId);
    // Bạn có thể thêm các phương thức tùy chỉnh tại đây nếu cần
}
