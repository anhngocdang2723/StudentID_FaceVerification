package com.Project.StudentIDVerification.controller;

import jakarta.servlet.http.HttpSession;
import org.springframework.ui.Model;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;

@Controller
@RequestMapping("/admin_dashboard")
public class AdminController {
    @GetMapping
    public String adminDashboard(HttpSession session, Model model) {
        String userRole = (String) session.getAttribute("userRole");
//      System.out.println("role: " + userRole);
        if ("admin".equals(userRole)) {
            return "admin/admin_dashboard";
        } else {
            model.addAttribute("error", "Bạn không có quyền truy cập vào trang này.");
            return "error";
        }
    }

    @GetMapping("/logout")
    public String logout(HttpSession session) {
        session.invalidate();
        return "redirect:/invigilator/login";
    }
}


