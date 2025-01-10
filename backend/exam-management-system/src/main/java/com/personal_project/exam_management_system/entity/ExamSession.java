package com.personal_project.exam_management_system.entity;

import jakarta.persistence.*;

import java.util.List;

@Entity
@Table(name = "examsessions")
public class ExamSession {

    @Id
    @Column(name = "session_code")
    private String sessionCode;

    @Column(name = "course_code", nullable = false)
    private String courseCode;

    @Column(name = "room_code", nullable = false)
    private String roomCode;

    @Column(name = "student_codes")
    private String studentCodes;

    @Column(name = "proctor_code", nullable = false)
    private String proctorCode;

    @Column(name = "exam_date_time", nullable = false)
    private String examDateTime;

    @Column(name = "session_status", nullable = false)
    private String sessionStatus;

    @Column(name = "report_file_path")
    private String reportFilePath;

    public ExamSession() {}

    public ExamSession(String sessionCode, String courseCode, String roomCode, String studentCodes,
                       String proctorCode, String examDateTime, String sessionStatus, String reportFilePath) {
        this.sessionCode = sessionCode;
        this.courseCode = courseCode;
        this.roomCode = roomCode;
        this.studentCodes = studentCodes;
        this.proctorCode = proctorCode;
        this.examDateTime = examDateTime;
        this.sessionStatus = sessionStatus;
        this.reportFilePath = reportFilePath;
    }

    public String getSessionCode() {
        return sessionCode;
    }

    public void setSessionCode(String sessionCode) {
        this.sessionCode = sessionCode;
    }

    public String getCourseCode() {
        return courseCode;
    }

    public void setCourseCode(String courseCode) {
        this.courseCode = courseCode;
    }

    public String getRoomCode() {
        return roomCode;
    }

    public void setRoomCode(String roomCode) {
        this.roomCode = roomCode;
    }

    public String getStudentCodes() {
        return studentCodes;
    }

    public void setStudentCodes(String studentCodes) {
        this.studentCodes = studentCodes;
    }

    public String getProctorCode() {
        return proctorCode;
    }

    public void setProctorCode(String proctorCode) {
        this.proctorCode = proctorCode;
    }

    public String getExamDateTime() {
        return examDateTime;
    }

    public void setExamDateTime(String examDateTime) {
        this.examDateTime = examDateTime;
    }

    public String getSessionStatus() {
        return sessionStatus;
    }

    public void setSessionStatus(String sessionStatus) {
        this.sessionStatus = sessionStatus;
    }

    public String getReportFilePath() {
        return reportFilePath;
    }

    public void setReportFilePath(String reportFilePath) {
        this.reportFilePath = reportFilePath;
    }
}
