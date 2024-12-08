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
    @Id
    private String id;

    @Field("invigilator_id")
    private String invigilatorId;

    @Field("invigilator_name")
    private String invigilatorName;

    @Field("invigilator_phone")
    private String invigilatorPhone;

    @Field("invigilator_email")
    private String invigilatorEmail;

    public Invigilator get() {
        // TODO Auto-generated method stub
        throw new UnsupportedOperationException("Unimplemented method 'get'");
    }

}