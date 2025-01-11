package com.personal_project.exam_management_system.service;

import com.personal_project.exam_management_system.entity.User;
import com.personal_project.exam_management_system.repository.UserRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

@Service
public class UserService {

    @Autowired
    private UserRepository userRepository;

    private String userCode;

    public String authenticate(String accountId, String password) {
        User user = userRepository.findByAccountIdAndPassword(accountId, password).orElse(null);

        if (user != null) {
            this.userCode = user.getAccountId();

            System.out.println("User account_id (user_code): " + userCode);

            Long roleId = user.getRole() != null ? user.getRole().getRoleId() : null;
            System.out.println("User role id: " + roleId);

            if (roleId != null) {
                switch (roleId.intValue()) {
                    case 1:
                        return "student/dashboard-student";
                    case 2:
                        return "proctor/dashboard-proctor";
                    case 3:
                        return "admin/dashboard-admin";
                    default:
                        return "Invalid role";
                }
            } else {
                return "Invalid role";
            }
        } else {
            return "Invalid credentials";
        }
    }

    public String getUserCode() {
        return this.userCode;
    }

    public void save(User user) {
        userRepository.save(user);
    }
}

