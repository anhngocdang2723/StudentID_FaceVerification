package com.personal_project.exam_management_system.controller;

import com.personal_project.exam_management_system.entity.ExamSession;
import com.personal_project.exam_management_system.entity.Proctor;
import com.personal_project.exam_management_system.entity.Student;
import com.personal_project.exam_management_system.service.ProctorService;
import com.personal_project.exam_management_system.repository.ProctorRepository;
import com.personal_project.exam_management_system.repository.ExamSessionRepository;
import com.personal_project.exam_management_system.service.UserService;
import com.personal_project.exam_management_system.service.ExamSessionService;
import com.personal_project.exam_management_system.config.AppConfig;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.*;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.net.HttpURLConnection;
import java.net.URL;
import java.nio.charset.StandardCharsets;
import java.util.List;
import java.util.Map;
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

    @Autowired
    private ExamSessionService examSessionService;

    @Autowired
    private AppConfig appConfig;



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

    @GetMapping("/start-exam-session")
    public String startExamSession(Model model) {
        return "start-exam-session";
    }

    @PostMapping("/start-exam-session")
    @ResponseBody  // Đảm bảo trả về dữ liệu JSON thay vì view
    public ResponseEntity<?> startExamSession(@RequestBody Map<String, String> payload) {
        String sessionCode = payload.get("sessionCode");
        String url = "http://127.0.0.1:8000/get-student-info/";

        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.APPLICATION_JSON);

        HttpEntity<String> entity = new HttpEntity<>("{\"sessionCode\":\"" + sessionCode + "\"}", headers);

        try {
            ResponseEntity<String> response = appConfig.restTemplate().exchange(url, HttpMethod.POST, entity, String.class);

            if (response.getStatusCode() == HttpStatus.OK) {
                return ResponseEntity.ok(response.getBody());  // Trả về JSON từ Flask
            } else {
                return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body("{\"error\": \"Không lấy được danh sách sinh viên\"}");
            }
        } catch (Exception e) {
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body("{\"error\": \"Lỗi kết nối đến Flask API\"}");
        }
    }

    @GetMapping("/verify-face")
    public String verifyFace(@RequestParam("student_id") String studentId,
                             @RequestParam("name") String name,
                             @RequestParam("phone") String phone,
                             @RequestParam("image_url") String imageUrl,
                             Model model) {
        model.addAttribute("studentId", studentId);
        model.addAttribute("name", name);
        model.addAttribute("phone", phone);
        model.addAttribute("imageUrl", imageUrl);
        return "verify-face";
    }
}
