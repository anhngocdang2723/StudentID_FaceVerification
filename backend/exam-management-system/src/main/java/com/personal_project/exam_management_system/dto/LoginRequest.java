package com.personal_project.exam_management_system.dto;

public class LoginRequest {

    private String accountId;
    private String password;

    // Constructor mặc định
    public LoginRequest() {}

    // Getter và Setter
    public String getAccountId() {
        return accountId;
    }

    public void setAccountId(String accountId) {
        this.accountId = accountId;
    }

    public String getPassword() {
        return password;
    }

    public void setPassword(String password) {
        this.password = password;
    }
}
