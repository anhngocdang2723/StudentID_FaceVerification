package com.Project.StudentIDVerification.controller;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;

@Controller
public class UploadController {

    @GetMapping("/")
    public String index() {
        return "index"; // trả về tên tệp HTML (index.html)
    }
}
