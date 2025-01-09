package com.personal_project.exam_management_system.controller;

import com.personal_project.exam_management_system.service.UserService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;

@Controller
public class LoginController {

    @Autowired
    private UserService userService;

    // Hiển thị trang đăng nhập
    @GetMapping("/login")
    public String showLoginPage() {
        return "login";  // Chỉ trả về tên của file login.html
    }

    // Xử lý đăng nhập khi người dùng gửi form
    @PostMapping("/login")
    public String login(@RequestParam String accountId, @RequestParam String password, Model model) {
        String result = userService.authenticate(accountId, password);

        if (result.equals("Invalid credentials") || result.equals("Invalid role")) {
            model.addAttribute("error", result);  // Hiển thị lỗi
            return "login";  // Quay lại trang đăng nhập
        } else {
            // Chuyển hướng đến trang dashboard tương ứng
            // Đảm bảo sử dụng các đường dẫn đúng với vai trò người dùng
            switch (result) {
                case "student/dashboard-student":
                    return "redirect:/student/dashboard-student";  // Đối với sinh viên
                case "proctor/dashboard-proctor":
                    return "redirect:/proctor/dashboard-proctor";  // Đối với giám thị
                case "admin/dashboard-admin":
                    return "redirect:/admin/dashboard-admin";  // Đối với quản trị viên
                default:
                    model.addAttribute("error", "Unknown role");
                    return "login";  // Nếu không xác định được vai trò
            }
        }
    }

    // Các endpoint cho từng dashboard

//    @GetMapping("/student/dashboard-student")
//    public String studentDashboard() {
//        return "dashboard-student";  // Trả về trang dashboard-student.html
//    }
//
//    @GetMapping("/proctor/dashboard-proctor")
//    public String proctorDashboard() {
//        return "dashboard-proctor";  // Trả về trang dashboard-proctor.html
//    }
//
//    @GetMapping("/admin/dashboard-admin")
//    public String adminDashboard() {
//        return "dashboard-admin";  // Trả về trang dashboard-admin.html
//    }
}
