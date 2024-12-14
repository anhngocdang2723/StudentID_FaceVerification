package com.Project.StudentIDVerification.DTO;

import java.util.List;

public class ExamRoomCreateDTO {
    private String roomId;  // Mã phòng thi
    private int capacity;   // Số lượng sinh viên
    private String examId;  // Mã bài thi
    private String invigilatorId;  // Mã giám thị
    private List<String> studentIds;  // Danh sách mã sinh viên

    // Getter và Setter
    public String getRoomId() {
        return roomId;
    }

    public void setRoomId(String roomId) {
        this.roomId = roomId;
    }

    public int getCapacity() {
        return capacity;
    }

    public void setCapacity(int capacity) {
        this.capacity = capacity;
    }

    public String getExamId() {
        return examId;
    }

    public void setExamId(String examId) {
        this.examId = examId;
    }

    public String getInvigilatorId() {
        return invigilatorId;
    }

    public void setInvigilatorId(String invigilatorId) {
        this.invigilatorId = invigilatorId;
    }

    public List<String> getStudentIds() {
        return studentIds;
    }

    public void setStudentIds(List<String> studentIds) {
        this.studentIds = studentIds;
    }
}
