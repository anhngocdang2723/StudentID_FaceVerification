package com.personal_project.exam_management_system.entity;

import com.personal_project.exam_management_system.converter.LocalDateConverter;
import jakarta.persistence.*;
import java.time.LocalDate;

@Entity
@Table(name = "Students")
public class Student {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long studentId;

    @Column(nullable = false, unique = true)
    private String studentCode;

    @Column(nullable = false)
    private String fullName;

    @Column(nullable = false)
    private String department;

    @Column(nullable = false)
    private String className;

    @Column(nullable = false)
    private String cohort;

    @Enumerated(EnumType.STRING)
    @Column(nullable = false)
    private Gender gender;

    @Convert(converter = LocalDateConverter.class)
    @Column(nullable = false)
    private LocalDate dateOfBirth;

    @Column(nullable = true)
    private String phoneNumber;

    @Column(nullable = true)
    private String email;

    @Enumerated(EnumType.STRING)
    @Column(nullable = false)
    private Status status;

    @Column(nullable = true)
    private String studentPhoto;

    @Column(nullable = true)
    private String facePhoto;

    public Student() {}

    public Student(String studentCode, String fullName, String department, String className, String cohort, Gender gender, LocalDate dateOfBirth, String phoneNumber, String email, Status status, String studentPhoto, String facePhoto) {
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

    public String getStudentPhoto() {
        return studentPhoto;
    }

    public void setStudentPhoto(String studentPhoto) {
        this.studentPhoto = studentPhoto;
    }

    public String getFacePhoto() {
        return facePhoto;
    }

    public void setFacePhoto(String facePhoto) {
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
                ", studentPhoto='" + studentPhoto + '\'' +
                ", facePhoto='" + facePhoto + '\'' +
                '}';
    }

    public enum Gender {
        MALE,
        FEMALE;
    }

    public enum Status {
        ACTIVE,
        GRADUATED,
        INACTIVE;
    }
}
