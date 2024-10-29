package com.Project.StudentIDVerification.repository;

import com.Project.StudentIDVerification.model.Invigilator;
import org.springframework.data.mongodb.repository.MongoRepository;
import org.springframework.stereotype.Repository;

@Repository // Thêm annotation @Repository
public interface InvigilatorRepository extends MongoRepository<Invigilator, String> {
    Invigilator findByInvigilatorId(String invigilatorId); // Tìm giám thị theo ID
}
