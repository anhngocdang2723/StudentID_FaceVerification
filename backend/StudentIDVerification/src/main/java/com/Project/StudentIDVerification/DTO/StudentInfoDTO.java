package com.Project.StudentIDVerification.DTO;

import lombok.Getter;

@Getter
//Data Transfer Object (DTO)
public class StudentInfoDTO {
    private final String stdName;
    private final String stdId;
    private final String stdPhone;

    public StudentInfoDTO(String stdName, String stdId, String stdPhone) {
        this.stdName = stdName;
        this.stdId = stdId;
        this.stdPhone = stdPhone;
    }
}