package com.Project.StudentIDVerification.repository;

import com.Project.StudentIDVerification.model.Exam;
import org.springframework.data.mongodb.repository.MongoRepository;

import java.util.Optional;

public interface ExamRepository extends MongoRepository<Exam, String> {
    Optional<Exam> findByExamId(String examId);  // Tìm kiếm theo examId thay vì _id
}
