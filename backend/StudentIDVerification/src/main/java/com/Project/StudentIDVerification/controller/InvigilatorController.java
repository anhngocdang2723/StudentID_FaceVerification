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
import org.springframework.web.bind.annotation.ModelAttribute;
import org.springframework.web.bind.annotation.PathVariable;
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

    // Hiển thị trang đăng nhập
    @GetMapping("/login")
    public String showLoginPage() {
        return "login";
    }

    // Kiểm tra đăng nhập
    @PostMapping("/login")
    public String login(@RequestParam("invigilatorId") String invigilatorId,
                        @RequestParam("invigilatorEmail") String email,
                        HttpSession session,
                        Model model) {

        if ("admin".equalsIgnoreCase(invigilatorId) && "admin".equalsIgnoreCase(email)) {
            session.setAttribute("userRole", "admin");
            System.out.println("Admin logged in");
            return "redirect:/admin_dashboard";
        }

        Invigilator invigilator = invigilatorRepository.findByInvigilatorIdAndInvigilatorEmail(invigilatorId, email);
        if (invigilator != null) {
            session.setAttribute("userRole", "invigilator");
            session.setAttribute("invigilatorId", invigilatorId);
            session.setAttribute("invigilatorName", invigilator.getInvigilatorName());
            System.out.println("invigilatorId: " + session.getAttribute("invigilatorId") + "/userRole: "+ session.getAttribute("userRole") + "/Name: "+ session.getAttribute("invigilatorName"));
            //return "redirect:/invigilator/home"; // Điều hướng đến trang chủ giám thị  ???????? ĐANG LỖI Ở VIỆC KHÔNG LẤY ĐƯỢC SESSION
            return "invigilator";
        }

        model.addAttribute("error", "Mã giám thị hoặc email không đúng.");
        return "login";
    }

    //Lấy trang chủ giám thị ???????? ĐANG LỖI Ở VIỆC KHÔNG LẤY ĐƯỢC SESSION
    @GetMapping("/home")
    public String invigilatorHome(HttpSession session, Model model) {
        // Kiểm tra xem người dùng đã đăng nhập chưa (kiểm tra session)
        if (!checkAccess(session, "invigilator")) {
            return "redirect:/invigilator/login"; // Nếu chưa đăng nhập, chuyển về trang login
        }

        // Nếu đã đăng nhập, lấy thông tin giám thị
        String invigilatorId = (String) session.getAttribute("invigilatorId");
        Optional<Invigilator> invigilatorOpt = invigilatorRepository.findById(invigilatorId);
        if (invigilatorOpt.isPresent()) {
            Invigilator invigilator = invigilatorOpt.get();
            model.addAttribute("invigilatorName", invigilator.getInvigilatorName());
            return "invigilator"; // Trả về trang chủ giám thị
        }

        return "redirect:/invigilator/login"; // Nếu không tìm thấy giám thị, chuyển về trang login
    }

    @GetMapping("/info")
    public String showPersonalInfo(HttpSession session, Model model) {
        if (!checkAccess(session, "invigilator")) {
            return "redirect:/invigilator/login";
        }
        String invigilatorId = (String) session.getAttribute("invigilatorId");

        System.out.println("Searching for invigilator with id: " + invigilatorId);
        try {
            Invigilator invigilator = invigilatorRepository.findByInvigilatorId(invigilatorId);
            if (invigilator != null) {
                model.addAttribute("invigilator", invigilator);
                return "invigilator-info";
            } else {
                model.addAttribute("error", "Không tìm thấy thông tin giám thị.");
                return "error";
            }
        } catch (Exception e) {
            model.addAttribute("error", "Lỗi khi truy xuất dữ liệu giám thị.");
            return "error";
        }
    }

    // Đăng xuất
    @GetMapping("/logout")
    public String logout(HttpSession session) {
        session.invalidate(); // Xóa toàn bộ session
        return "redirect:/invigilator/login"; // Quay lại trang đăng nhập
    }

    private boolean checkAccess(HttpSession session, String role) {
        String userRole = (String) session.getAttribute("userRole");
        return role.equalsIgnoreCase(userRole); // Kiểm tra xem quyền trong session có khớp với quyền yêu cầu không
    }

    @GetMapping("/new")
    public String addnewInvigilator(Model model) {
        Invigilator invigilator=new Invigilator();
        model.addAttribute("invigilator", invigilator);
        return "invigilator_addnew";
    }

    @PostMapping("/save")
    public String saveinvigilator(@ModelAttribute("invigilator") Invigilator invigilator) {
        //TODO: process POST request
        invigilatorService.addInvigilator(invigilator);
        return "redirect:/invigilator_invigilators";
    }

    @GetMapping("/edit/{id}")
    public String showFormForUpdate(@PathVariable("id") String id, Model model) {
        Optional<Invigilator> invigilator= invigilatorService.getInvigilatorById(id);
        model.addAttribute("invigilator", invigilator);
        return "invigilator_edit";
    }

    @PostMapping("/update/{id})")
    public String updateGiamthi(@PathVariable("id") String id, @ModelAttribute("invigilator") Invigilator invigilatorDetails) {
        //TODO: process POST request
        invigilatorService.updateInvigilator(id, invigilatorDetails);
        return "redirect:/invigilator_invigilators";
    }

    @GetMapping("delete/{id}")
    public String deleteGiamThi(@PathVariable String id) {
        invigilatorService.deleteInvigilator(id);
        return "redirect:/invigilator_invigilators";
    }
}
