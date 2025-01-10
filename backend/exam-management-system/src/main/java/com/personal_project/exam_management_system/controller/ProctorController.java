package com.personal_project.exam_management_system.controller;

import com.personal_project.exam_management_system.entity.ExamSession;
import com.personal_project.exam_management_system.entity.Proctor;
import com.personal_project.exam_management_system.service.ProctorService;
import com.personal_project.exam_management_system.repository.ProctorRepository;
import com.personal_project.exam_management_system.repository.ExamSessionRepository;
import com.personal_project.exam_management_system.service.UserService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;

import java.util.List;
import java.util.Optional;

@Controller
@RequestMapping("/proctor")
public class ProctorController {

    @Autowired
    private UserService userService;

    @Autowired
    private ProctorService proctorService;

    @Autowired
    private ProctorRepository proctorRepository;

    @Autowired
    private ExamSessionRepository examSessionRepository;

    // Trang dashboard-proctor
    @GetMapping("/dashboard-proctor")
    public String dashboardProctor(Model model) {
        String userCode = userService.getUserCode();

        if (userCode != null) {
            Proctor proctor = proctorService.findByProctorCode(userCode);

            if (proctor != null) {
                model.addAttribute("proctor", proctor);
                return "dashboard-proctor";
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
        String userCode = userService.getUserCode();

        if (userCode != null) {
            Proctor proctor = proctorService.findByProctorCode(userCode);

            if (proctor != null) {
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

    @GetMapping("/schedule")
    public String viewProctorExamSchedule(Model model) {
        String proctorCode = userService.getUserCode();
        Optional<Proctor> proctor = proctorRepository.findByProctorCode(proctorCode);

        if (proctor.isEmpty()) {
            model.addAttribute("error", "Giám thị không tồn tại");
            return "error";
        }
        List<ExamSession> examSessions = examSessionRepository.findByProctorCode(proctorCode);

        model.addAttribute("proctor", proctor.get());
        model.addAttribute("examSessions", examSessions);

        return "exam-schedule-proctor";
    }
}
