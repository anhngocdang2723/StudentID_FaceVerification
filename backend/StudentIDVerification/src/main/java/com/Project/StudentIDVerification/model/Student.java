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

    // Getters và Setters
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
    private ExamResults examResults; // Đối tượng điểm thi

    // Đổi tên trường để tuân thủ quy tắc đặt tên
    @Field("status")
    private boolean status; // Đối tượng trạng thái

    // Lớp nội bộ cho examResults (đã bổ sung các trường cần thiết)
    @Setter
    @Getter
    public static class ExamResults {
        // Getters và Setters
        @Field("subject") // Tên môn học
        private String subject; // Tên môn học
        @Field("score") // Điểm
        private double score;    // Điểm thi

    }
}