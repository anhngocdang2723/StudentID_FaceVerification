package com.Project.StudentIDVerification.repository;

import com.Project.StudentIDVerification.model.Invigilator;

import java.util.List;
import java.util.Optional;

import org.springframework.data.mongodb.repository.MongoRepository;
import org.springframework.stereotype.Repository;
@Repository
public interface InvigilatorRepository extends MongoRepository<Invigilator, String> {
    Invigilator findByInvigilatorIdAndInvigilatorEmail(String invigilatorId, String invigilatorEmail); // Gộp ID và Email

    Invigilator findByInvigilatorId(String invigilatorId);
}
