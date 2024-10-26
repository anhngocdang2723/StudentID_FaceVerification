package com.Project.StudentIDVerification.model;

import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.mapping.Document;
import org.springframework.data.mongodb.core.mapping.Field;

@Document(collection = "Students")
public class Student {

    @Id
    private String id;        // _id trong MongoDB
    @Field("std_id")
    private String stdId;     // Mã sinh viên
    @Field("std_name")
    private String stdName;   // Tên sinh viên
    @Field("std_dob")
    private String stdDob;    // Ngày sinh
    @Field("std_class")
    private String stdClass;  // Lớp học
    @Field("std_faculty")
    private String stdFaculty; // Khoa/Viện/Trường
    @Field("std_course")
    private String stdCourse;  // Khóa học
    @Field("std_email")
    private String stdEmail;   // Email
    @Field("std_phone")
    private String stdPhone;   // Số điện thoại
    @Field("exam_results")
    private ExamResults examResults; // Đối tượng điểm thi

    // Getters và Setters
    public String getId() {
        return id;
    }

    public void setId(String id) {
        this.id = id;
    }

    public String getStdId() {
        return stdId;
    }

    public void setStdId(String stdId) {
        this.stdId = stdId;
    }

    public String getStdName() {
        return stdName;
    }

    public void setStdName(String stdName) {
        this.stdName = stdName;
    }

    public String getStdDob() {
        return stdDob;
    }

    public void setStdDob(String stdDob) {
        this.stdDob = stdDob;
    }

    public String getStdClass() {
        return stdClass;
    }

    public void setStdClass(String stdClass) {
        this.stdClass = stdClass;
    }

    public String getStdFaculty() {
        return stdFaculty;
    }

    public void setStdFaculty(String stdFaculty) {
        this.stdFaculty = stdFaculty;
    }

    public String getStdCourse() {
        return stdCourse;
    }

    public void setStdCourse(String stdCourse) {
        this.stdCourse = stdCourse;
    }

    public String getStdEmail() {
        return stdEmail;
    }

    public void setStdEmail(String stdEmail) {
        this.stdEmail = stdEmail;
    }

    public String getStdPhone() {
        return stdPhone;
    }

    public void setStdPhone(String stdPhone) {
        this.stdPhone = stdPhone;
    }

    public ExamResults getExamResults() {
        return examResults;
    }

    public void setExamResults(ExamResults examResults) {
        this.examResults = examResults;
    }

    // Lớp nội bộ cho examResults (đã bổ sung các trường cần thiết)
    public static class ExamResults {
        @Field("subject") // Tên môn học
        private String subject; // Tên môn học
        @Field("score") // Điểm
        private double score;    // Điểm thi

        // Getters và Setters
        public String getSubject() {
            return subject;
        }

        public void setSubject(String subject) {
            this.subject = subject;
        }

        public double getScore() {
            return score;
        }

        public void setScore(double score) {
            this.score = score;
        }
    }
}
