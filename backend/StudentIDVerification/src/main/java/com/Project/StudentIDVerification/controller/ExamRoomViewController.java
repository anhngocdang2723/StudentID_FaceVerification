package com.Project.StudentIDVerification.controller;

import com.Project.StudentIDVerification.DTO.StudentInfoDTO;
import com.Project.StudentIDVerification.service.ExamService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;

import java.util.List;

@Controller
public class ExamRoomViewController {

    @Autowired
    private ExamService examService;

    @GetMapping("/exam-room")
    public String showExamRoomForm() {
        return "examRoomForm"; // Trả về tên tệp HTML
    }

//    @PostMapping("/exam-room")
//    public String getStudentsInRoom(@RequestParam String roomId, Model model) {
//        List<StudentInfoDTO> students = examService.getStudentsInExamRoom(roomId);
//        model.addAttribute("students", students);
//        model.addAttribute("roomId", roomId);
//        return "examRoomResult"; // Trả về tên tệp HTML cho kết quả
//    }
}
