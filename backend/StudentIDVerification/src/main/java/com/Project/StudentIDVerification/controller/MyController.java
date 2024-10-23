package com.Project.StudentIDVerification.controller;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api")
public class MyController {
    @GetMapping("/hello")
    public String sayHello() {
        return "Hello, Spring Boot!";
    }
    @GetMapping("/goodbye")
    public String sayGoodbye() {
        return "Goodbye, Spring Boot!";
    }
}
