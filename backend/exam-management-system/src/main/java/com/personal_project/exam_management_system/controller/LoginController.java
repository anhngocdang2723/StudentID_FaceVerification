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
            model.addAttribute("error", result);
            return "login";
        } else {
            switch (result) {
                case "student/dashboard-student":
                    return "redirect:/student/dashboard-student";
                case "proctor/dashboard-proctor":
                    return "redirect:/proctor/dashboard-proctor";
                case "admin/dashboard-admin":
                    return "redirect:/admin/dashboard-admin";
                default:
                    model.addAttribute("error", "Unknown role");
                    return "login";
            }
        }
    }

    @GetMapping("/logout")
    public String logout() {
        return "redirect:/login";
    }
}
