package com.personal_project.exam_management_system.repository;

import com.personal_project.exam_management_system.entity.User;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.Optional;

public interface UserRepository extends JpaRepository<User, Long> {

    Optional<User> findByAccountId(String accountId); // Tìm kiếm người dùng theo accountId
}
