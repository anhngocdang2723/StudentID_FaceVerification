package com.Project.StudentIDVerification.repository;

import com.Project.StudentIDVerification.model.Invigilator;
import org.springframework.data.mongodb.repository.MongoRepository;
import org.springframework.stereotype.Repository;

import java.util.Optional;

@Repository
public interface InvigilatorRepository extends MongoRepository<Invigilator, String> {
    Optional<Invigilator> findByInvigilatorId(String invigilatorId);
}
