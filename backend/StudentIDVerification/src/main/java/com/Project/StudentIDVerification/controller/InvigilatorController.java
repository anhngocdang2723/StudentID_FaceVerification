package com.Project.StudentIDVerification.controller;

import java.util.List;
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
import org.springframework.web.bind.annotation.RequestBody;

@Controller
@RequestMapping("/invigilator_invigilators")
public class InvigilatorController {
    @Autowired
    private InvigilatorService invigilatorService;

    @Autowired
    private InvigilatorRepository invigilatorRepository;

    @GetMapping
    public String viewHomepage(Model model) {
        model.addAttribute("listInvigilator", invigilatorService.getAllgiamthi());
        return "invigilator_invigilators"; 
    }

    @PostMapping("/login")
    public String login(@RequestParam("invigilatorId") String maGiamThi,
                        @RequestParam("invigilatorEmail") String email,
                        HttpSession session,
                        Model model) {
        // Kiểm tra nếu là tài khoản admin
        if ("admin".equals(maGiamThi) && "admin".equals(email)) {
            session.setAttribute("userRole", "admin");
            return "redirect:/admin_dashboard"; // Đường dẫn đến trang quản trị
        }

        // Kiểm tra giám thị thông thường
        Invigilator userId = invigilatorRepository.findByInvigilatorId(maGiamThi);
        Invigilator userEmail = invigilatorRepository.findByInvigilatorEmail(email);
        if (userId != null && userEmail != null) {
            session.setAttribute("userRole", "invigilator");
            return "index"; // Trang chính sau khi đăng nhập thành công
        } else {
            model.addAttribute("error", "Mã giám thị hoặc email không đúng.");
            return "login"; // Trang đăng nhập lại nếu thất bại
        }
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
        Optional<Invigilator> invigilator= invigilatorService.getInvigilatorByid(id);
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
