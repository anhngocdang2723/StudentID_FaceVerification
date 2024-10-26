package com.Project.StudentIDVerification.model;

import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.mapping.Document;
import org.springframework.data.mongodb.core.mapping.Field;

import java.util.List;

@Document(collection = "ExamRooms")
public class ExamRoom {
    @Id
    private String id; // _id trong MongoDB
    @Field("room_id")
    private String roomId; // Mã phòng thi
    @Field("invigilator_id")
    private String invigilatorId; // Mã giám thị
    @Field("students")
    private List<StudentReference> students; // Danh sách sinh viên tham gia

    // Getters và Setters
    public String getId() {
        return id;
    }

    public void setId(String id) {
        this.id = id;
    }

    public String getRoomId() {
        return roomId;
    }

    public void setRoomId(String roomId) {
        this.roomId = roomId;
    }

    public String getInvigilatorId() {
        return invigilatorId;
    }

    public void setInvigilatorId(String invigilatorId) {
        this.invigilatorId = invigilatorId;
    }

    public List<StudentReference> getStudents() {
        return students;
    }

    public void setStudents(List<StudentReference> students) {
        this.students = students;
    }

    public static class StudentReference {
        @Field("std_id")
        private String stdId; // Mã sinh viên

        public String getStdId() {
            return stdId;
        }

        public void setStdId(String stdId) {
            this.stdId = stdId;
        }
    }
}
