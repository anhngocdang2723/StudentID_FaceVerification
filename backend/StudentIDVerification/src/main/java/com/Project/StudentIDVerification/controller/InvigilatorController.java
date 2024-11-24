package com.Project.StudentIDVerification.controller;

import java.util.List;
import java.util.Optional;

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
                        Model model) {
        Invigilator userId = invigilatorRepository.findByInvigilatorId(maGiamThi);
        Invigilator userEmail = invigilatorRepository.findByInvigilatorEmail(email);
        if (userId != null && userEmail !=null) {
            // Xử lý khi đăng nhập thành công (ví dụ: chuyển hướng đến trang chủ)
            return "index";
        } else {
            model.addAttribute("error", "Mã giám thị hoặc email không đúng.");
            return "login";
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
