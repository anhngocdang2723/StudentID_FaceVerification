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
            return "redirect:/" + result;  // result có thể là "dashboard_student", "dashboard_proctor", "dashboard_admin"
        }
    }

    // Các endpoint cho từng dashboard

    @GetMapping("/dashboard_proctor")
    public String proctorDashboard() {
        return "dashboard_proctor";  // Trả về trang dashboard_proctor.html
    }

    @GetMapping("/dashboard_admin")
    public String adminDashboard() {
        return "dashboard_admin";  // Trả về trang dashboard_admin.html
    }
}
