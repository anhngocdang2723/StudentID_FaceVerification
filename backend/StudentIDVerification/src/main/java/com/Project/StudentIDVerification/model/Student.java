package com.Project.StudentIDVerification.model;

import lombok.Getter;
import lombok.Setter;
import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.mapping.Document;
import org.springframework.data.mongodb.core.mapping.Field;

@Setter
@Getter
@Document(collection = "Students")
public class Student {
    @Id
    private String id;

    @Field("std_id")
    private String stdId;

    @Field("std_name")
    private String stdName;

    @Field("std_dob")
    private String stdDob;

    @Field("std_class")
    private String stdClass;

    @Field("std_faculty")
    private String stdFaculty;

    @Field("std_course")
    private String stdCourse;

    @Field("std_email")
    private String stdEmail;

    @Field("std_phone")
    private String stdPhone;

    @Field("exam_results")
    private ExamResults examResults;

    @Field("status")
    private boolean status;

    @Setter
    @Getter
    public static class ExamResults {
        @Field("subject")
        private String subject;

        @Field("score")
        private double score;
    }
}