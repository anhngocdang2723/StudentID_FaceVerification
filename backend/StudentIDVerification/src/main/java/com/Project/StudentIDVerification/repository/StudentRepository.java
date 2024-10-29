// StudentRepository.java
package com.Project.StudentIDVerification.repository;

import com.Project.StudentIDVerification.model.Student;
import org.springframework.data.mongodb.repository.MongoRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface StudentRepository extends MongoRepository<Student, String> {
    Student findByStdId(String stdId);

    long countByStatus(boolean status);

    List<Student> findByStatus(Boolean status);
}

