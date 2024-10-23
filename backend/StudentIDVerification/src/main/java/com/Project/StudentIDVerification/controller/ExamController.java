package com.Project.StudentIDVerification.controller;

import com.Project.StudentIDVerification.DTO.StudentInfoDTO;
import com.Project.StudentIDVerification.service.ExamService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/exams")
public class ExamController {

    @Autowired
    private ExamService examService;

    @GetMapping("/students-in-room/{roomId}")
    public ExamRoomDetails getStudentsInRoom(@PathVariable String roomId) {
        return examService.getExamRoomDetails(roomId);
    }
}
