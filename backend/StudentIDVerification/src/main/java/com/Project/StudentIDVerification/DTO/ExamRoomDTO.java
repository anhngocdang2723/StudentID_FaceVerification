package com.Project.StudentIDVerification.DTO;

import java.util.List;

public class ExamRoomDTO {
    private String roomName;
    private String invigilator;
    private String examName;
    private List<StudentInfoDTO> students;

    // Constructor, getters and setters
    public ExamRoomDTO(String roomName, String invigilator, String examName, List<StudentInfoDTO> students) {
        this.roomName = roomName;
        this.invigilator = invigilator;
        this.examName = examName;
        this.students = students;
    }

    // Getters and Setters
    public String getRoomName() {
        return roomName;
    }

    public void setRoomName(String roomName) {
        this.roomName = roomName;
    }

    public String getInvigilator() {
        return invigilator;
    }

    public void setInvigilator(String invigilator) {
        this.invigilator = invigilator;
    }

    public String getExamName() {
        return examName;
    }

    public void setExamName(String examName) {
        this.examName = examName;
    }

    public List<StudentInfoDTO> getStudents() {
        return students;
    }

    public void setStudents(List<StudentInfoDTO> students) {
        this.students = students;
    }
}
