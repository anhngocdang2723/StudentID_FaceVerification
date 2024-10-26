package com.Project.StudentIDVerification.DTO;

public class StudentInfoDTO {
    private String stdName;
    private String stdId;
    private String stdPhone;

    public StudentInfoDTO(String stdName, String stdId, String stdPhone) {
        this.stdName = stdName;
        this.stdId = stdId;
        this.stdPhone = stdPhone;
    }

    // Getters
    public String getStdName() {
        return stdName;
    }

    public String getStdId() {
        return stdId;
    }

    public String getStdPhone() {
        return stdPhone;
    }
}
