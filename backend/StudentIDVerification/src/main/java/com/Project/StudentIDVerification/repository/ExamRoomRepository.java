package com.Project.StudentIDVerification.repository;

import com.Project.StudentIDVerification.model.ExamRoom;
import org.springframework.data.mongodb.repository.MongoRepository;

import java.util.Optional;

public interface ExamRoomRepository extends MongoRepository<ExamRoom, String> {
    Optional<ExamRoom> findByRoomId(String roomId);
}