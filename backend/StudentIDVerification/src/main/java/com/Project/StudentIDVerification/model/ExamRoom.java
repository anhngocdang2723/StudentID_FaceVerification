package com.Project.StudentIDVerification.model;

import lombok.Getter;
import lombok.Setter;
import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.mapping.Document;
import org.springframework.data.mongodb.core.mapping.Field;

import java.util.List;

@Setter
@Getter
@Document(collection = "ExamRooms")
public class ExamRoom {
    @Id
    private String id;

    @Field("room_id")
    private String roomId;

    @Field("invigilator_id")
    private String invigilatorId;

    @Field("students")
    private List<StudentReference> students; // Danh sách sinh viên tham gia

    @Setter
    @Getter
    public static class StudentReference {
        @Field("std_id")
        private String stdId;
    }
}
