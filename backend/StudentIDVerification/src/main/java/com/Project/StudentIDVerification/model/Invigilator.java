package com.Project.StudentIDVerification.model;

import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.mapping.Document;
import org.springframework.data.mongodb.core.mapping.Field;

@Document(collection = "Invigilators")
public class Invigilator {
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

    // Getters và Setters
    public String getId() {
        return id;
    }

    public void setId(String id) {
        this.id = id;
    }

    public String getInvigilatorId() {
        return invigilatorId;
    }

    public void setInvigilatorId(String invigilatorId) {
        this.invigilatorId = invigilatorId;
    }

    public String getInvigilatorName() {
        return invigilatorName;
    }

    public void setInvigilatorName(String invigilatorName) {
        this.invigilatorName = invigilatorName;
    }

    public String getInvigilatorPhone() {
        return invigilatorPhone;
    }

    public void setInvigilatorPhone(String invigilatorPhone) {
        this.invigilatorPhone = invigilatorPhone;
    }

    public String getInvigilatorEmail() {
        return invigilatorEmail;
    }

    public void setInvigilatorEmail(String invigilatorEmail) {
        this.invigilatorEmail = invigilatorEmail;
    }
}
