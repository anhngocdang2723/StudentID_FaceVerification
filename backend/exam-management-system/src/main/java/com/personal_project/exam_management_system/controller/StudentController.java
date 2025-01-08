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

    @GetMapping("/dashboard_student")
    public String studentDashboard(Model model) {
        // Lấy userCode từ UserService
        String userCode = userService.getUserCode();

        // Debugging: In ra giá trị userCode
        System.out.println("User Code: " + userCode);

        if (userCode != null) {
            // Truy vấn thông tin sinh viên theo userCode
            Student student = studentService.findByStudentCode(userCode);

            // Debugging: In ra thông tin sinh viên
            System.out.println("Student Info: " + student);

            if (student != null) {
                // Nếu ảnh sinh viên không tồn tại, gán đường dẫn ảnh mặc định
                if (student.getStudentPhoto() == null || student.getStudentPhoto().isEmpty()) {
                    student.setStudentPhoto("path/to/default/student-photo.jpg");  // Đường dẫn ảnh thẻ sinh viên mặc định
                }
                if (student.getFacePhoto() == null || student.getFacePhoto().isEmpty()) {
                    student.setFacePhoto("path/to/default/face-photo.jpg");  // Đường dẫn ảnh khuôn mặt mặc định
                }

                // Truyền thông tin sinh viên vào model
                model.addAttribute("student", student);
                return "dashboard_student";  // Trả về trang dashboard_student.html
            } else {
                model.addAttribute("error", "Student not found");
                return "error";  // Nếu không tìm thấy sinh viên, hiển thị trang lỗi
            }
        } else {
            model.addAttribute("error", "User code not found");
            return "error";  // Nếu không lấy được userCode, hiển thị lỗi
        }
    }
}
