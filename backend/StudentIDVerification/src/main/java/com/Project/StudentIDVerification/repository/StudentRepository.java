// StudentRepository.java
package com.Project.StudentIDVerification.repository;

import com.Project.StudentIDVerification.model.Student;
import org.springframework.data.mongodb.repository.MongoRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface StudentRepository extends MongoRepository<Student, String> {
    // Các query bổ sung nếu cần
    long countByStatus(boolean status);
}
