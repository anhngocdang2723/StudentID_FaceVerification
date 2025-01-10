package com.personal_project.exam_management_system.entity;

import jakarta.persistence.*;

@Entity
@Table(name = "Proctors")
public class Proctor {

    @Id
    @Column(name = "proctor_code", nullable = false, unique = true)
    private String proctorCode;  // Mã giám thị (làm khóa chính)

    @Column(nullable = false)
    private String fullName;  // Họ và tên

    @Column(nullable = false)
    private String department;  // Đơn vị (Khoa/Bộ môn)

    @Column(nullable = true)
    private String phoneNumber;  // Số điện thoại

    @Column(nullable = true)
    private String email;  // Email

    public Proctor() {}

    public Proctor(String proctorCode, String fullName, String department, String phoneNumber, String email) {
        this.proctorCode = proctorCode;
        this.fullName = fullName;
        this.department = department;
        this.phoneNumber = phoneNumber;
        this.email = email;
    }

    // Getters và Setters
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
                "proctorCode='" + proctorCode + '\'' +
                ", fullName='" + fullName + '\'' +
                ", department='" + department + '\'' +
                ", phoneNumber='" + phoneNumber + '\'' +
                ", email='" + email + '\'' +
                '}';
    }
}
