package com.Project.StudentIDVerification.controller;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;

@Controller
public class UploadController {

    @GetMapping("/uploadImage")
    public String index() {
        return "uploadImage";
    }
}
