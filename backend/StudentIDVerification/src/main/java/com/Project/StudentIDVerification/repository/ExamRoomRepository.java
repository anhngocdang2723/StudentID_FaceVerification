package com.Project.StudentIDVerification.repository;

import com.Project.StudentIDVerification.model.ExamRoom;
import org.springframework.data.mongodb.repository.MongoRepository;

import java.util.Optional;

public interface ExamRoomRepository extends MongoRepository<ExamRoom, String> {
    // Custom query nếu cần (VD: tìm theo roomId)
    ExamRoom findByRoomId(String roomId);
}