package com.Project.StudentIDVerification.controller;

import java.util.Optional;

import jakarta.servlet.http.HttpSession;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestMapping;

import com.Project.StudentIDVerification.model.Invigilator;
import com.Project.StudentIDVerification.repository.InvigilatorRepository;
import com.Project.StudentIDVerification.service.InvigilatorService;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.PostMapping;

@Controller
@RequestMapping("/invigilator")
public class InvigilatorController {
    @Autowired
    private InvigilatorService invigilatorService;
    @Autowired
    private InvigilatorRepository invigilatorRepository;

    // Trang đăng nhập
    @GetMapping("/login")
    public String showLoginPage() {
        return "invigilator/login";  // Điều chỉnh lại đường dẫn
    }

    // Trang dashboard giám thị sau khi đăng nhập thành công
    @PostMapping("/login")
    public String login(@RequestParam("invigilatorId") String invigilatorId,
                        @RequestParam("invigilatorEmail") String email,
                        HttpSession session,
                        Model model) {
        // Kiểm tra tài khoản admin
        if ("admin".equalsIgnoreCase(invigilatorId) && "admin".equalsIgnoreCase(email)) {
            session.setAttribute("userRole", "admin");
            return "redirect:/admin_dashboard"; // Điều hướng đến trang admin dashboard
        }

        Invigilator invigilator = invigilatorRepository.findByInvigilatorIdAndInvigilatorEmail(invigilatorId, email);
        if (invigilator != null) {
            session.setAttribute("userRole", "invigilator");
            session.setAttribute("invigilatorId", invigilatorId);
            session.setAttribute("invigilatorName", invigilator.getInvigilatorName());

            // log console
//            System.out.println("Login successful for invigilator: ");
//            System.out.println("ID: " + invigilatorId);
//            System.out.println("Name: " + invigilator.getInvigilatorName());
//            System.out.println("Role: invigilator");

            // Sau khi đăng nhập thành công, chuyển đến trang dashboard giám thị
//            return "redirect:/invigilator/home";
            return "invigilator/invigilator_dashboard";
        }

        model.addAttribute("error", "Mã giám thị hoặc email không đúng.");
        return "invigilator/login";
    }

    @GetMapping("/home")
    public String invigilatorHome(HttpSession session, Model model) {

//        if (!checkAccess(session)) {
//            return "redirect:/invigilator/login";
//        }

        String invigilatorId = (String) session.getAttribute("invigilatorId");
        Optional<Invigilator> invigilatorOpt = invigilatorRepository.findById(invigilatorId);

        //log console
//        System.out.println("Invigilator ID: " + invigilatorId);
//        System.out.println("User Role: " + session.getAttribute("userRole"));

        if (invigilatorOpt.isPresent()) {
            model.addAttribute("invigilatorName", invigilatorOpt.get().getInvigilatorName());
            return "invigilator/invigilator_dashboard";
        }

        return "redirect:/invigilator/login";
    }

    // Hiển thị thông tin cá nhân
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

    private boolean checkAccess(HttpSession session) {
        String sessionRole = (String) session.getAttribute("userRole");

        return sessionRole != null && sessionRole.equals("invigilator");
    }

}
