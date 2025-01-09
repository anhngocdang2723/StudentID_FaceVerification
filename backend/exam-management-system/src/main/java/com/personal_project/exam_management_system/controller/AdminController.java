package com.personal_project.exam_management_system.controller;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;

@Controller
@RequestMapping("/admin")
public class AdminController {
    @GetMapping("/dashboard-admin")
    public String dashboardAdmin() {
        return "dashboard-admin";
    }
}
