package com.Project.StudentIDVerification.repository;

import com.Project.StudentIDVerification.model.Invigilator;

import java.util.List;
import java.util.Optional;

import org.springframework.data.mongodb.repository.MongoRepository;
import org.springframework.stereotype.Repository;



@Repository // Thêm annotation @Repository
public interface InvigilatorRepository extends MongoRepository<Invigilator, String> {
    Invigilator findByInvigilatorEmail(String invigilatorEmail);
    Invigilator findByInvigilatorId(String invigilatorId); // Tìm giám thị theo ID

}
