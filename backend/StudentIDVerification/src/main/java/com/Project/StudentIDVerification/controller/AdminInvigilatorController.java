package com.Project.StudentIDVerification.controller;

import com.Project.StudentIDVerification.model.Invigilator;
import com.Project.StudentIDVerification.service.InvigilatorService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Optional;

@Controller
@RequestMapping("/invigilators")
public class AdminInvigilatorController {
    private final InvigilatorService invigilatorService;
    public AdminInvigilatorController(InvigilatorService invigilatorService) {
        this.invigilatorService = invigilatorService;
    }

    // Hiển thị danh sách giám thị
    @GetMapping
    public String listAllInvigilators(Model model) {
        List<Invigilator> invigilators = invigilatorService.getAllInvigilators();
        model.addAttribute("invigilators", invigilators);
        return "admin/invigilator_invigilators";
    }

    // Hiển thị form thêm mới giám thị
    @GetMapping("/new")
    public String addNewInvigilator(Model model) {
        model.addAttribute("invigilator", new Invigilator());
        return "admin/invigilator_addnew";
    }

    // Lưu giám thị mới
    @PostMapping("/save")
    public String saveInvigilator(@ModelAttribute("invigilator") Invigilator invigilator) {
        invigilatorService.addInvigilator(invigilator);
        return "redirect:/invigilators";
    }

    // Hiển thị form chỉnh sửa giám thị
    @GetMapping("/edit/{id}")
    public String showFormForUpdate(@PathVariable("id") String id, Model model) {
        Optional<Invigilator> invigilator = invigilatorService.getInvigilatorById(id);
        if (invigilator.isPresent()) {
            model.addAttribute("invigilator", invigilator.get());
            return "admin/invigilator_edit";
        } else {
            return "redirect:/invigilators";
        }
    }

    // Cập nhật giám thị
    @PostMapping("/update/{id}")
    public String updateInvigilator(@PathVariable("id") String id, @ModelAttribute("invigilator") Invigilator invigilatorDetails) {
        invigilatorService.updateInvigilator(id, invigilatorDetails);
        return "redirect:/invigilators";
    }

    // Xóa giám thị
    @GetMapping("/delete/{id}")
    public String deleteInvigilator(@PathVariable("id") String id) {
        invigilatorService.deleteInvigilator(id);
        return "redirect:/invigilators";
    }
}
