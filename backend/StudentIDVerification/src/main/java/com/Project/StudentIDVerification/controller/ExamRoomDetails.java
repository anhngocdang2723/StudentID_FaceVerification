package com.Project.StudentIDVerification.controller;

import com.Project.StudentIDVerification.DTO.StudentInfoDTO;
import java.util.List;

public class ExamRoomDetails {
    private String roomId;
    private String invigilator;
    private String examName;
    private List<StudentInfoDTO> students;

    public ExamRoomDetails(String roomId, String invigilator, String examName, List<StudentInfoDTO> students) {
        this.roomId = roomId;
        this.invigilator = invigilator;
        this.examName = examName;
        this.students = students;
    }

    // Getters và Setters
    public String getRoomId() {
        return roomId;
    }

    public String getInvigilator() {
        return invigilator;
    }

    public String getExamName() {
        return examName;
    }

    public List<StudentInfoDTO> getStudents() {
        return students;
    }
}
