package com.Project.StudentIDVerification.model;

import lombok.Getter;
import lombok.Setter;
import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.mapping.Document;
import org.springframework.data.mongodb.core.mapping.Field;

@Getter
@Setter
@Document(collection = "Exams")
public class Exam {
    @Id
    private String id;

    @Field("exam_id")
    private String examId;

    @Field("exam_name")
    private String examName;

    @Field("exam_date")
    private String examDate;
}
