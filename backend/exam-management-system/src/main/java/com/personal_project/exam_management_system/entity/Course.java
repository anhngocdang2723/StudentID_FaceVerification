package com.personal_project.exam_management_system.entity;

import jakarta.persistence.*;

@Entity
@Table(name = "Courses")
public class Course {

    @Id
    @Column(name = "course_code")
    private String courseCode;  // Mã học phần

    @Column(nullable = false)
    private String courseName;  // Tên học phần

    @Column(nullable = false)
    private int creditHours;  // Số tín chỉ

    @Column(nullable = true)
    private String description;  // Mô tả

    @Column(nullable = false)
    private String department;  // Đơn vị

    @Column(nullable = false)
    private String semester;  // Học kỳ

    @Column(nullable = false)
    private int year;  // Năm học

    public Course() {}

    public Course(String courseCode, String courseName, int creditHours, String description, String department, String semester, int year) {
        this.courseCode = courseCode;
        this.courseName = courseName;
        this.creditHours = creditHours;
        this.description = description;
        this.department = department;
        this.semester = semester;
        this.year = year;
    }

    public String getCourseCode() {
        return courseCode;
    }

    public void setCourseCode(String courseCode) {
        this.courseCode = courseCode;
    }

    public String getCourseName() {
        return courseName;
    }

    public void setCourseName(String courseName) {
        this.courseName = courseName;
    }

    public int getCreditHours() {
        return creditHours;
    }

    public void setCreditHours(int creditHours) {
        this.creditHours = creditHours;
    }

    public String getDescription() {
        return description;
    }

    public void setDescription(String description) {
        this.description = description;
    }

    public String getDepartment() {
        return department;
    }

    public void setDepartment(String department) {
        this.department = department;
    }

    public String getSemester() {
        return semester;
    }

    public void setSemester(String semester) {
        this.semester = semester;
    }

    public int getYear() {
        return year;
    }

    public void setYear(int year) {
        this.year = year;
    }

    @Override
    public String toString() {
        return "Course{" +
                "courseCode='" + courseCode + '\'' +
                ", courseName='" + courseName + '\'' +
                ", creditHours=" + creditHours +
                ", description='" + description + '\'' +
                ", department='" + department + '\'' +
                ", semester='" + semester + '\'' +
                ", year=" + year +
                '}';
    }
}
