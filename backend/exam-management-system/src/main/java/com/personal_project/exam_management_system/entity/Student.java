package com.personal_project.exam_management_system.entity;

import jakarta.persistence.*;
import java.time.LocalDate;

@Entity
public class Student {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY) // Sử dụng IDENTITY cho SQLite
    private Long studentId;  // Mã sinh viên

    @Column(nullable = false, unique = true)
    private String studentCode;  // Mã sinh viên

    @Column(nullable = false)
    private String fullName;  // Họ và tên

    @Column(nullable = false)
    private String department;  // Đơn vị (Khoa/Viện)

    @Column(nullable = false)
    private String className;  // Lớp học

    @Column(nullable = false)
    private String cohort;  // Khoá học (Ví dụ: 62, 63, v.v.)

    @Enumerated(EnumType.STRING)
    @Column(nullable = false)
    private Gender gender;  // Giới tính (Male/Female)

    @Column(nullable = false)
    private LocalDate dateOfBirth;  // Ngày sinh

    @Column(nullable = true)
    private String phoneNumber;  // Số điện thoại

    @Column(nullable = true)
    private String email;  // Email

    @Enumerated(EnumType.STRING)
    @Column(nullable = false)
    private Status status;  // Trạng thái sinh viên (Active/Graduated/Inactive)

    @Lob
    private byte[] studentPhoto;  // Ảnh thẻ sinh viên (Lưu dưới dạng BLOB)

    @Lob
    private byte[] facePhoto;  // Ảnh khuôn mặt sinh viên (Lưu dưới dạng BLOB)

    // Constructor mặc định
    public Student() {}

    // Constructor có tham số
    public Student(String studentCode, String fullName, String department, String className, String cohort, Gender gender, LocalDate dateOfBirth, String phoneNumber, String email, Status status, byte[] studentPhoto, byte[] facePhoto) {
        this.studentCode = studentCode;
        this.fullName = fullName;
        this.department = department;
        this.className = className;
        this.cohort = cohort;
        this.gender = gender;
        this.dateOfBirth = dateOfBirth;
        this.phoneNumber = phoneNumber;
        this.email = email;
        this.status = status;
        this.studentPhoto = studentPhoto;
        this.facePhoto = facePhoto;
    }

    // Getters và Setters
    public Long getStudentId() {
        return studentId;
    }

    public void setStudentId(Long studentId) {
        this.studentId = studentId;
    }

    public String getStudentCode() {
        return studentCode;
    }

    public void setStudentCode(String studentCode) {
        this.studentCode = studentCode;
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

    public String getClassName() {
        return className;
    }

    public void setClassName(String className) {
        this.className = className;
    }

    public String getCohort() {
        return cohort;
    }

    public void setCohort(String cohort) {
        this.cohort = cohort;
    }

    public Gender getGender() {
        return gender;
    }

    public void setGender(Gender gender) {
        this.gender = gender;
    }

    public LocalDate getDateOfBirth() {
        return dateOfBirth;
    }

    public void setDateOfBirth(LocalDate dateOfBirth) {
        this.dateOfBirth = dateOfBirth;
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

    public Status getStatus() {
        return status;
    }

    public void setStatus(Status status) {
        this.status = status;
    }

    public byte[] getStudentPhoto() {
        return studentPhoto;
    }

    public void setStudentPhoto(byte[] studentPhoto) {
        this.studentPhoto = studentPhoto;
    }

    public byte[] getFacePhoto() {
        return facePhoto;
    }

    public void setFacePhoto(byte[] facePhoto) {
        this.facePhoto = facePhoto;
    }

    @Override
    public String toString() {
        return "Student{" +
                "studentId=" + studentId +
                ", studentCode='" + studentCode + '\'' +
                ", fullName='" + fullName + '\'' +
                ", department='" + department + '\'' +
                ", className='" + className + '\'' +
                ", cohort='" + cohort + '\'' +
                ", gender=" + gender +
                ", dateOfBirth=" + dateOfBirth +
                ", phoneNumber='" + phoneNumber + '\'' +
                ", email='" + email + '\'' +
                ", status=" + status +
                '}';
    }

    // Enum cho Giới tính
    public enum Gender {
        MALE,
        FEMALE;
    }

    // Enum cho Trạng thái sinh viên
    public enum Status {
        ACTIVE,
        GRADUATED,
        INACTIVE;
    }
}
