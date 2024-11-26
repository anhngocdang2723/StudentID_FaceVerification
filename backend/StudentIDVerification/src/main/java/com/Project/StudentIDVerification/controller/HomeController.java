package com.Project.StudentIDVerification.controller;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;

@Controller
public class HomeController {
    // Trang mặc định khi truy cập vào /
    @GetMapping("/")
    public String redirectToLogin() {
        return "redirect:/invigilator/login";
    }
}
