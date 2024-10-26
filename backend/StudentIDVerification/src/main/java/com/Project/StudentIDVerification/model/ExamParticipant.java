package com.Project.StudentIDVerification.model;

import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.mapping.Document;
import org.springframework.data.mongodb.core.mapping.Field;

@Document(collection = "ExamParticipants")
public class ExamParticipant {
    @Id
    private String id; // Trường _id sẽ được MongoDB tự động tạo ra
    @Field("exam_id")
    private String examId;
    @Field("std_id")
    private String stdId;
    @Field("exam_room")
    private String examRoom;

    // Constructor, Getters và Setters
    public ExamParticipant(String examId, String stdId, String examRoom) {
        this.examId = examId;
        this.stdId = stdId;
        this.examRoom = examRoom;
    }

    public String getId() {
        return id;
    }

    public void setId(String id) {
        this.id = id;
    }

    public String getExamId() {
        return examId;
    }

    public void setExamId(String examId) {
        this.examId = examId;
    }

    public String getStdId() {
        return stdId;
    }

    public void setStdId(String stdId) {
        this.stdId = stdId;
    }

    public String getExamRoom() {
        return examRoom;
    }

    public void setExamRoom(String examRoom) {
        this.examRoom = examRoom;
    }
}
