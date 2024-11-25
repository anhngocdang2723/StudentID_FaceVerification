package com.Project.StudentIDVerification.controller;

import jakarta.servlet.http.HttpSession;
import org.springframework.ui.Model;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;

@Controller
@RequestMapping("/admin_dashboard")
public class AdminController {
    @GetMapping
    public String adminDashboard(HttpSession session, Model model) {
        // Kiểm tra role từ session
        String userRole = (String) session.getAttribute("userRole");
        if ("admin".equals(userRole)) {
            return "admin_dashboard"; // Hiển thị trang quản trị nếu là admin
        } else {
            model.addAttribute("error", "Bạn không có quyền truy cập vào trang này.");
            return "error"; // Trang lỗi nếu không phải admin
        }
    }

    @GetMapping("/logout")
    public String logout(HttpSession session) {
        session.invalidate(); // Xóa toàn bộ session
        return "redirect:/login"; // Quay lại trang đăng nhập
    }
}


