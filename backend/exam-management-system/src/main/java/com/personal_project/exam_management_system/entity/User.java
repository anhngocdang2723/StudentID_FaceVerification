package com.personal_project.exam_management_system.entity;

import jakarta.persistence.*;
import java.time.LocalDateTime;

@Entity
public class User {

    @Id
    @GeneratedValue(strategy = GenerationType.SEQUENCE)
    private Long userId;  // Mã người dùng (ID tài khoản)

    @Column(nullable = false, unique = true)
    private String accountId;  // Tài khoản (MSV, mã giám thị, mã admin)

    @Column(nullable = false)
    private String password;  // Mật khẩu

    @Enumerated(EnumType.STRING)
    @Column(nullable = false)
    private Role role;  // Phân quyền (student, proctor, admin)

    @Column(nullable = false, updatable = false)
    private LocalDateTime createdAt;  // Ngày tạo tài khoản

    // Constructor mặc định
    public User() {}

    // Constructor có tham số
    public User(String accountId, String password, Role role, LocalDateTime createdAt) {
        this.accountId = accountId;
        this.password = password;
        this.role = role;
        this.createdAt = createdAt;
    }

    // Getters và Setters
    public Long getUserId() {
        return userId;
    }

    public void setUserId(Long userId) {
        this.userId = userId;
    }

    public String getAccountId() {
        return accountId;
    }

    public void setAccountId(String accountId) {
        this.accountId = accountId;
    }

    public String getPassword() {
        return password;
    }

    public void setPassword(String password) {
        this.password = password;
    }

    public Role getRole() {
        return role;
    }

    public void setRole(Role role) {
        this.role = role;
    }

    public LocalDateTime getCreatedAt() {
        return createdAt;
    }

    public void setCreatedAt(LocalDateTime createdAt) {
        this.createdAt = createdAt;
    }

    @Override
    public String toString() {
        return "User{" +
                "userId=" + userId +
                ", accountId='" + accountId + '\'' +
                ", role=" + role +
                ", createdAt=" + createdAt +
                '}';
    }

    // Enum cho các quyền (student, proctor, admin)
    public enum Role {
        STUDENT,
        PROCTOR,
        ADMIN
    }
}
