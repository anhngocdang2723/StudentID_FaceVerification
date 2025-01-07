package com.personal_project.exam_management_system.controller;

import com.personal_project.exam_management_system.entity.User;
import com.personal_project.exam_management_system.repository.UserRepository;
import com.personal_project.exam_management_system.dto.LoginRequest; // Đảm bảo import lớp LoginRequest
import com.personal_project.exam_management_system.service.UserService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;

import java.util.Optional;

@Controller
@RequestMapping("/users")
public class UserController {

    @Autowired
    private UserService userService;

    @Autowired
    private UserRepository userRepository; // Inject UserRepository vào controller

    // Trang đăng nhập
    @GetMapping("/login")
    public String showLoginPage() {
        return "login"; // Trả về trang login.html
    }
//
//    @PostMapping("/login")
//    public ResponseEntity<String> login(@RequestBody LoginRequest loginRequest) {
//        String accountId = loginRequest.getAccountId();
//        String password = loginRequest.getPassword();
//
//        // Kiểm tra tài khoản và mật khẩu (không mã hóa)
//        Optional<User> userOptional = userRepository.findByAccountId(accountId); // Gọi findByAccountId từ đối tượng userRepository
//        if (userOptional.isPresent()) {
//            User user = userOptional.get();
//            if (password.equals(user.getPassword())) { // So sánh mật khẩu trực tiếp
//                // Lấy thông tin role của tài khoản
//                String role = String.valueOf(user.getRole());
//
//                // Thông báo đăng nhập thành công kèm theo role
//                return ResponseEntity.ok("Đăng nhập thành công! Role của tài khoản: " + role);
//            } else {
//                return ResponseEntity.status(HttpStatus.UNAUTHORIZED).body("Mật khẩu không đúng!");
//            }
//        } else {
//            return ResponseEntity.status(HttpStatus.NOT_FOUND).body("Tài khoản không tồn tại!");
//        }
//    }

    @PostMapping("/login")
    public String login(
            @RequestParam("accountId") String accountId,
            @RequestParam("password") String password,
            Model model) {

        Optional<User> userOptional = userRepository.findByAccountId(accountId);
        if (userOptional.isPresent()) {
            User user = userOptional.get();
            if (password.equals(user.getPassword())) {
                // Logic xử lý khi đăng nhập thành công
                model.addAttribute("successMessage", "Đăng nhập thành công!");
                return "login";
            } else {
                // Mật khẩu sai
                model.addAttribute("errorMessage", "Mật khẩu không đúng!");
                return "error";
            }
        } else {
            // Không tìm thấy tài khoản
            model.addAttribute("errorMessage", "Error: Student not found");
            return "error";
        }
    }

//    // Đăng nhập: Kiểm tra accountId và password, nếu đúng chuyển đến giao diện thông tin theo role
//    @PostMapping("/login")
//    public String login(@RequestParam("accountId") String accountId,
//                        @RequestParam("password") String password,
//                        RedirectAttributes redirectAttributes) {
//        Optional<User> user = userService.login(accountId, password);
//
//        if (user.isPresent()) {
//            // Lưu thông tin người dùng vào flash attribute
//            redirectAttributes.addFlashAttribute("user", user.get());
//
//            // Kiểm tra role và chuyển hướng
//            String role = String.valueOf(user.get().getRole());
//            if (role != null) {
//                switch (role) {
//                    case "student":
//                        return "redirect:/students/info/" + accountId; // Trang thông tin sinh viên
//                    case "proctor":
//                        return "redirect:/proctors/info/" + accountId; // Trang thông tin giám thị
//                    case "admin":
//                        return "redirect:/admin/dashboard"; // Trang thông tin admin
//                    default:
//                        redirectAttributes.addFlashAttribute("error", "Invalid role");
//                        return "redirect:/users/login"; // Quay lại login nếu không xác định role
//                }
//            } else {
//                redirectAttributes.addFlashAttribute("error", "Role is missing or invalid");
//                return "redirect:/users/login"; // Quay lại login nếu role không hợp lệ
//            }
//        } else {
//            redirectAttributes.addFlashAttribute("error", "Invalid account ID or password");
//            return "redirect:/users/login"; // Quay lại trang login nếu đăng nhập thất bại
//        }
//    }
}
