package com.Project.StudentIDVerification.controller;

import java.util.Optional;

import jakarta.servlet.http.HttpSession;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.core.io.FileSystemResource;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.*;

import com.Project.StudentIDVerification.model.Invigilator;
import com.Project.StudentIDVerification.repository.InvigilatorRepository;
import com.Project.StudentIDVerification.service.InvigilatorService;

import org.springframework.ui.Model;

@Controller
@RequestMapping("/invigilator")
public class InvigilatorController {
    private final InvigilatorService invigilatorService;
    private final InvigilatorRepository invigilatorRepository;
    public InvigilatorController(InvigilatorService invigilatorService, InvigilatorRepository invigilatorRepository) {
        this.invigilatorService = invigilatorService;
        this.invigilatorRepository = invigilatorRepository;
    }

    @GetMapping("/login")
    public String showLoginPage() {
        return "invigilator/login";
    }

    // Dashboard giám thị
    @PostMapping("/login")
    public String login(@RequestParam("invigilatorId") String invigilatorId,
                        @RequestParam("invigilatorEmail") String email,
                        HttpSession session,
                        Model model) {
        if ("admin".equalsIgnoreCase(invigilatorId) && "admin".equalsIgnoreCase(email)) {
            session.setAttribute("userRole", "admin");
            return "redirect:/admin_dashboard";
        }

        Invigilator invigilator = invigilatorRepository.findByInvigilatorIdAndInvigilatorEmail(invigilatorId, email);
        if (invigilator != null) {
            session.setAttribute("userRole", "invigilator");
            session.setAttribute("invigilatorId", invigilatorId);
            session.setAttribute("invigilatorName", invigilator.getInvigilatorName());
            // log console truy vấn dữ liệu
//            System.out.println("Login successful for invigilator: ");
//            System.out.println("ID: " + invigilatorId);
//            System.out.println("Name: " + invigilator.getInvigilatorName());
//            System.out.println("Role: invigilator");
//          return "redirect:/invigilator/home"; //Lỗi vẫn ở trang login
            return "invigilator/invigilator-dashboard";
        }
        model.addAttribute("error", "Mã giám thị hoặc email không đúng.");
        return "invigilator/login";
    }

    @GetMapping("/home")
    public String invigilatorHome(HttpSession session, Model model) {
        if (!checkAccess(session)) {
            return "redirect:/invigilator/login";
        }

        String invigilatorId = (String) session.getAttribute("invigilatorId");
        Optional<Invigilator> invigilatorOpt = invigilatorRepository.findById(invigilatorId);

        //log console nhận session
//        System.out.println("Invigilator ID: " + invigilatorId);
//        System.out.println("User Role: " + session.getAttribute("userRole"));

        if (invigilatorOpt.isPresent()) {
            model.addAttribute("invigilatorName", invigilatorOpt.get().getInvigilatorName());
            return "invigilator/invigilator-dashboard";
        }
        return "redirect:/invigilator/login";
    }

    // Xem tt cá nhân
    @GetMapping("/info")
    public String showPersonalInfo(HttpSession session, Model model) {
//        if (checkAccess(session)) {
//            return "redirect:/invigilator/login";
//        }
        String invigilatorId = (String) session.getAttribute("invigilatorId");
        Invigilator invigilator = invigilatorRepository.findByInvigilatorId(invigilatorId);
        if (invigilator != null) {
            model.addAttribute("invigilator", invigilator);
            return "invigilator/invigilator-info";
        } else {
            model.addAttribute("error", "Không tìm thấy thông tin giám thị.");
            return "error";
        }
    }

    @GetMapping("/logout")
    public String logout(HttpSession session) {
        session.invalidate();
        return "redirect:/invigilator/login";
    }
    private boolean checkAccess(HttpSession session) {
        String sessionRole = (String) session.getAttribute("userRole");

        return sessionRole != null && sessionRole.equals("invigilator");
    }

    @GetMapping("/api-integration")
    public String apiIntegrationPage() {
        return "invigilator/api_integration";
    }

    @GetMapping("/upload-image")
    public String uploadImagePage() {
        return "invigilator/uploadImage";
    }

    @GetMapping("/view-exam-paper/{filename}")
    public ResponseEntity<FileSystemResource> viewExamPaper(@PathVariable String filename) {
        // Đường dẫn gốc nơi lưu file PDF
        String fileBasePath = "C:/exam-papers/";  // Thay thế bằng đường dẫn thật của bạn

        FileSystemResource fileResource = new FileSystemResource(fileBasePath + filename);
        if (!fileResource.exists()) {
            return ResponseEntity.notFound().build();
        }

        HttpHeaders headers = new HttpHeaders();
        headers.add(HttpHeaders.CONTENT_DISPOSITION, "inline; filename=" + filename);

        return ResponseEntity.ok()
                .headers(headers)
                .contentType(MediaType.APPLICATION_PDF)
                .body(fileResource);
    }
}