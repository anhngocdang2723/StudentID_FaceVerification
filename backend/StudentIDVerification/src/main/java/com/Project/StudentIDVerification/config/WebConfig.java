package com.Project.StudentIDVerification.config;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.servlet.config.annotation.CorsRegistry;
import org.springframework.web.servlet.config.annotation.WebMvcConfigurer;

@Configuration
public class WebConfig implements WebMvcConfigurer {

    @Override
    public void addCorsMappings(CorsRegistry registry) {
        registry.addMapping("/api/**")  // Đường dẫn mà bạn muốn áp dụng CORS
                .allowedOrigins("http://127.0.0.1:8000")  // Địa chỉ FastAPI
                .allowedMethods("GET", "POST", "PUT", "DELETE", "OPTIONS")  // Các phương thức cho phép
                .allowedHeaders("*")  // Cho phép tất cả header
                .allowCredentials(true);  // Nếu cần thiết
    }
}
