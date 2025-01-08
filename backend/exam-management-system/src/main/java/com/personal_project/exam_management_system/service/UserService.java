package com.personal_project.exam_management_system.service;

import com.personal_project.exam_management_system.entity.User;
import com.personal_project.exam_management_system.repository.UserRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

@Service
public class UserService {

    @Autowired
    private UserRepository userRepository;

    public String authenticate(String accountId, String password) {
        // Tìm kiếm người dùng với accountId và password
        User user = userRepository.findByAccountIdAndPassword(accountId, password).orElse(null);

        if (user != null) {
            // Đăng nhập thành công, in ra role_id
            Long roleId = user.getRole() != null ? user.getRole().getRoleId() : null;
            System.out.println("User role_id: " + roleId);
            return "Login successful";
        } else {
            // Sai tài khoản hoặc mật khẩu
            return "Invalid credentials";
        }
    }
}
