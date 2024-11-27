package com.Project.StudentIDVerification.controller;

import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.ControllerAdvice;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.servlet.mvc.support.RedirectAttributes;

import java.io.IOException;
import java.nio.file.AccessDeniedException;

@ControllerAdvice
public class GlobalExceptionHandler {
    @ExceptionHandler(AccessDeniedException.class)
    public String handleAccessDeniedException(Model model) {
        model.addAttribute("errorTitle", "Lỗi: Access denied");
        model.addAttribute("errorMessage","Không có quyền truy cập");
        return "error";
    }

    @ExceptionHandler(Exception.class)
    public String handleGeneralException(Exception e, Model model, RedirectAttributes redirectAttributes) {
        model.addAttribute("errorTitle","Lỗi hệ thống");
        model.addAttribute("errorMessage",e.getMessage());
        return "error";
    }
}
