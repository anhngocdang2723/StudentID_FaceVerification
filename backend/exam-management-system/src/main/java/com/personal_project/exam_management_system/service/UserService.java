package com.personal_project.exam_management_system.service;

import com.personal_project.exam_management_system.entity.User;
import com.personal_project.exam_management_system.repository.UserRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

@Service
public class UserService {

    @Autowired
    private UserRepository userRepository;

    // Khai báo biến userCode để lưu trữ mã người dùng
    private String userCode;

    public String authenticate(String accountId, String password) {
        // Tìm kiếm người dùng với accountId và password
        User user = userRepository.findByAccountIdAndPassword(accountId, password).orElse(null);

        if (user != null) {
            // Lưu account_id vào biến tạm user_code
            this.userCode = user.getAccountId();  // Sử dụng this để gán giá trị cho biến toàn cục

            // In ra account_id (user_code)
            System.out.println("User account_id (user_code): " + userCode);

            // Lấy role_id và xác định giao diện tương ứng
            Long roleId = user.getRole() != null ? user.getRole().getRoleId() : null;
            System.out.println("User role id: " + roleId);

            if (roleId != null) {
                // Dựa vào role_id trả về giao diện tương ứng
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
            // Sai tài khoản hoặc mật khẩu
            return "Invalid credentials";
        }
    }

    // Phương thức trả về userCode
    public String getUserCode() {
        return this.userCode;  // Trả về giá trị của userCode
    }
}

