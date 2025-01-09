package com.personal_project.exam_management_system.controller;

import com.personal_project.exam_management_system.entity.Proctor;
import com.personal_project.exam_management_system.service.ProctorService;
import com.personal_project.exam_management_system.service.UserService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;

@Controller
@RequestMapping("/proctor")
public class ProctorController {

    @Autowired
    private UserService userService;

    @Autowired
    private ProctorService proctorService;

    // Trang dashboard-proctor
    @GetMapping("/dashboard-proctor")
    public String dashboardProctor(Model model) {
        // Lấy userCode để query thông tin giám thị
        String userCode = userService.getUserCode();

        if (userCode != null) {
            // query thông tin giám thị
            Proctor proctor = proctorService.findByProctorCode(userCode);

            if (proctor != null) {
                // Truyền thông tin giám thị vào model
                model.addAttribute("proctor", proctor);
                return "dashboard-proctor";  // Trả về trang dashboard-proctor.html
            } else {
                model.addAttribute("error", "Proctor not found");
                return "error";
            }
        } else {
            model.addAttribute("error", "User code not found");
            return "error";
        }
    }

    // Trang thông tin cá nhân của giám thị
    @GetMapping("/info")
    public String proctorInfo(Model model) {
        // Lấy userCode từ UserService
        String userCode = userService.getUserCode();

        if (userCode != null) {
            // Truy vấn thông tin giám thị theo userCode
            Proctor proctor = proctorService.findByProctorCode(userCode);

            if (proctor != null) {
                // Truyền thông tin giám thị vào model
                model.addAttribute("proctor", proctor);
                return "proctor-info";  // Trả về trang proctor-info.html
            } else {
                model.addAttribute("error", "Proctor not found");
                return "error";
            }
        } else {
            model.addAttribute("error", "User code not found");
            return "error";
        }
    }
}
