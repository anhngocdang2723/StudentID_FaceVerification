package com.personal_project.exam_management_system.dto;

public class ExamSessionDetailDTO {

    private String sessionCode;
    private String courseName;
    private String address;
    private String listStudentNames;  // Đổi từ List<String> thành String
    private String proctorName;
    private String examDateTime;
    private String sessionStatus;
    private String reportFilePath;

    // Constructor
    public ExamSessionDetailDTO(String sessionCode, String courseName, String address,
                                String listStudentNames, String proctorName,
                                String examDateTime, String sessionStatus, String reportFilePath) {
        this.sessionCode = sessionCode;
        this.courseName = courseName;
        this.address = address;
        this.listStudentNames = listStudentNames;
        this.proctorName = proctorName;
        this.examDateTime = examDateTime;
        this.sessionStatus = sessionStatus;
        this.reportFilePath = reportFilePath;
    }

    // Getters and Setters
    public String getSessionCode() {
        return sessionCode;
    }

    public void setSessionCode(String sessionCode) {
        this.sessionCode = sessionCode;
    }

    public String getCourseName() {
        return courseName;
    }

    public void setCourseName(String courseName) {
        this.courseName = courseName;
    }

    public String getAddress() {
        return address;
    }

    public void setAddress(String address) {
        this.address = address;
    }

    public String getListStudentNames() {
        return listStudentNames;
    }

    public void setListStudentNames(String listStudentNames) {
        this.listStudentNames = listStudentNames;
    }

    public String getProctorName() {
        return proctorName;
    }

    public void setProctorName(String proctorName) {
        this.proctorName = proctorName;
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
