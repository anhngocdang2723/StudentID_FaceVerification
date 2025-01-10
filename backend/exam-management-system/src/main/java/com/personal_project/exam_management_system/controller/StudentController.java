package com.personal_project.exam_management_system.controller;

import com.personal_project.exam_management_system.entity.ExamSession;
import com.personal_project.exam_management_system.entity.*;
import com.personal_project.exam_management_system.repository.ExamRoomRepository;
import com.personal_project.exam_management_system.repository.StudentRepository;
import com.personal_project.exam_management_system.repository.ExamSessionRepository;
import com.personal_project.exam_management_system.service.ExamRoomService;
import com.personal_project.exam_management_system.service.StudentService;
import com.personal_project.exam_management_system.service.UserService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;

import java.util.List;
import java.util.Optional;

@Controller
@RequestMapping("/student")
public class StudentController {

    @Autowired
    private UserService userService;

    @Autowired
    private StudentService studentService;

    @Autowired
    private ExamRoomService examRoomService;

    @Autowired
    private StudentRepository studentRepository;

    @Autowired
    private ExamRoomRepository examRoomRepository;

    @Autowired
    private ExamSessionRepository examSessionRepository;

    // Trang dashboard-student
    @GetMapping("/dashboard-student")
    public String studentDashboard(Model model) {
        String userCode = userService.getUserCode();
//        System.out.println("User Code: " + userCode);
        if (userCode != null) {
            Student student = studentService.findStudentByStudentCode(userCode);

//            System.out.println("Student Info: " + student);

            if (student != null) {
                // Nếu ảnh sinh viên không tồn tại, gán đường dẫn ảnh mặc định
//                if (student.getStudentPhoto() == null || student.getStudentPhoto().isEmpty()) {
//                    student.setStudentPhoto("/images/default-student-photo.jpg");  // Đường dẫn ảnh thẻ sinh viên mặc định
//                }
//                if (student.getFacePhoto() == null || student.getFacePhoto().isEmpty()) {
//                    student.setFacePhoto("/images/default-face-photo.jpg");  // Đường dẫn ảnh khuôn mặt mặc định
//                }
                model.addAttribute("student", student);
                return "dashboard-student";
            } else {
                model.addAttribute("error", "Student not found");
                return "error";
            }
        } else {
            model.addAttribute("error", "User code not found");
            return "error";
        }
    }

    @GetMapping("/info")
    public String studentInfo(Model model) {
        String userCode = userService.getUserCode();

        if (userCode != null) {
            Student student = studentService.findStudentByStudentCode(userCode);

            if (student != null) {
                if (student.getStudentPhoto() == null || student.getStudentPhoto().isEmpty()) {
                    student.setStudentPhoto("/images/default-student-photo.jpg");
                }
                if (student.getFacePhoto() == null || student.getFacePhoto().isEmpty()) {
                    student.setFacePhoto("/images/default-face-photo.jpg");
                }

                model.addAttribute("student", student);
                return "student-info";
            } else {
                model.addAttribute("error", "Student not found");
                return "error";
            }
        } else {
            model.addAttribute("error", "User code not found");
            return "error";
        }
    }

    @GetMapping("/schedule")
    public String viewExamSchedule(Model model) {
        String studentCode = userService.getUserCode();
        if (studentCode == null) {
            model.addAttribute("error", "Student code is required");
            return "error";
        }
        Optional<Student> student = studentRepository.findByStudentCode(studentCode);
        if (student.isEmpty()) {
            model.addAttribute("error", "Sinh viên không tồn tại");
            return "error";
        }
        List<ExamSession> examSessions = examSessionRepository.findByStudentCode(studentCode);

        model.addAttribute("student", student.get());
        model.addAttribute("examSessions", examSessions);

        return "exam-schedule-std";
    }
}
