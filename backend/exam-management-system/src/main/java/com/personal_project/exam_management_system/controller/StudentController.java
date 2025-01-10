package com.personal_project.exam_management_system.controller;

import com.personal_project.exam_management_system.entity.Student;
import com.personal_project.exam_management_system.service.StudentService;
import com.personal_project.exam_management_system.service.UserService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;

@Controller
@RequestMapping("/student")
public class StudentController {

    @Autowired
    private UserService userService;

    @Autowired
    private StudentService studentService;

    // Trang dashboard-student
    @GetMapping("/dashboard-student")
    public String studentDashboard(Model model) {
        // Lấy userCode để query thông tin sv
        String userCode = userService.getUserCode();

//        System.out.println("User Code: " + userCode);

        if (userCode != null) {
            // query thông tin sv
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

                // Truyền thông tin sinh viên vào model
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

    // Trang thông tin cá nhân
    @GetMapping("/info")
    public String studentInfo(Model model) {
        // Lấy userCode từ UserService
        String userCode = userService.getUserCode();

        if (userCode != null) {
            // Truy vấn thông tin sinh viên theo userCode
            Student student = studentService.findStudentByStudentCode(userCode);

            if (student != null) {
                // Nếu ảnh sinh viên không tồn tại, gán đường dẫn ảnh mặc định
                if (student.getStudentPhoto() == null || student.getStudentPhoto().isEmpty()) {
                    student.setStudentPhoto("/images/default-student-photo.jpg");
                }
                if (student.getFacePhoto() == null || student.getFacePhoto().isEmpty()) {
                    student.setFacePhoto("/images/default-face-photo.jpg");
                }

                // Truyền thông tin sinh viên vào model
                model.addAttribute("student", student);
                return "student-info";  // Trả về trang student-info.html
            } else {
                model.addAttribute("error", "Student not found");
                return "error";
            }
        } else {
            model.addAttribute("error", "User code not found");
            return "error";
        }
    }
}
