package com.personal_project.exam_management_system.entity;

import jakarta.persistence.*;

@Entity
@Table(name = "Proctors")
public class Proctor {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)  // Sử dụng IDENTITY cho SQLite
    private Long proctorId;  // Mã giám thị (ID giám thị)

    @Column(nullable = false, unique = true)
    private String proctorCode;  // Mã giám thị

    @Column(nullable = false)
    private String fullName;  // Họ và tên

    @Column(nullable = false)
    private String department;  // Đơn vị (Khoa/Bộ môn)

    @Column(nullable = true)
    private String phoneNumber;  // Số điện thoại

    @Column(nullable = true)
    private String email;  // Email

    // Constructor mặc định
    public Proctor() {}

    // Constructor có tham số
    public Proctor(String proctorCode, String fullName, String department, String phoneNumber, String email) {
        this.proctorCode = proctorCode;
        this.fullName = fullName;
        this.department = department;
        this.phoneNumber = phoneNumber;
        this.email = email;
    }

    // Getters và Setters
    public Long getProctorId() {
        return proctorId;
    }

    public void setProctorId(Long proctorId) {
        this.proctorId = proctorId;
    }

    public String getProctorCode() {
        return proctorCode;
    }

    public void setProctorCode(String proctorCode) {
        this.proctorCode = proctorCode;
    }

    public String getFullName() {
        return fullName;
    }

    public void setFullName(String fullName) {
        this.fullName = fullName;
    }

    public String getDepartment() {
        return department;
    }

    public void setDepartment(String department) {
        this.department = department;
    }

    public String getPhoneNumber() {
        return phoneNumber;
    }

    public void setPhoneNumber(String phoneNumber) {
        this.phoneNumber = phoneNumber;
    }

    public String getEmail() {
        return email;
    }

    public void setEmail(String email) {
        this.email = email;
    }

    @Override
    public String toString() {
        return "Proctor{" +
                "proctorId=" + proctorId +
                ", proctorCode='" + proctorCode + '\'' +
                ", fullName='" + fullName + '\'' +
                ", department='" + department + '\'' +
                ", phoneNumber='" + phoneNumber + '\'' +
                ", email='" + email + '\'' +
                '}';
    }
}
