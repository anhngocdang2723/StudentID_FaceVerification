package com.personal_project.exam_management_system.repository;

import com.personal_project.exam_management_system.entity.ExamRoom;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface ExamRoomRepository extends JpaRepository<ExamRoom, String> {
}
