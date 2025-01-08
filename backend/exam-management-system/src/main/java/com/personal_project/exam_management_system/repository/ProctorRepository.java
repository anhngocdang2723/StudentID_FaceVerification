package com.personal_project.exam_management_system.repository;

import com.personal_project.exam_management_system.entity.Proctor;
import org.springframework.data.jpa.repository.JpaRepository;
import java.util.Optional;

public interface ProctorRepository extends JpaRepository<Proctor, Long> {
    Optional<Proctor> findByProctorCode(String proctorCode);
}
