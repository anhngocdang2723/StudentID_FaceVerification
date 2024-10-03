package com.example.demo.com.example.demo; // Nếu bạn tạo package con, sử dụng đúng package

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController // Đánh dấu class này là một controller
public class Controller {

    @GetMapping("/hello") // Đường dẫn cho endpoint này
    public String sayHello() {
        return "Hello, Spring Boot!"; // Phản hồi trả về cho client
    }
    @GetMapping("/goodbye")
    public String sayGoodbye() {
        return "Goodbye, Spring Boot!";
    }

}
