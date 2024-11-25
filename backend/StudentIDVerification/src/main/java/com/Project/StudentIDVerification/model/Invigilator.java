package com.Project.StudentIDVerification.model;

import lombok.Getter;
import lombok.Setter;
import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.mapping.Document;
import org.springframework.data.mongodb.core.mapping.Field;

@Getter
@Setter
@Document(collection = "Invigilators")
public class Invigilator {
    // Getters và Setters
    @Id
    private String id; // _id trong MongoDB
    @Field("invigilator_id")
    private String invigilatorId; // Mã giám thị
    @Field("invigilator_name")
    private String invigilatorName; // Tên giám thị
    @Field("invigilator_phone")
    private String invigilatorPhone; // Số điện thoại
    @Field("invigilator_email")
    private String invigilatorEmail; // Email


    public Invigilator get() {
        // TODO Auto-generated method stub
        throw new UnsupportedOperationException("Unimplemented method 'get'");
    }

}
