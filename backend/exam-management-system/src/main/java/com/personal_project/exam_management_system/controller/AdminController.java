package com.personal_project.exam_management_system.controller;

import com.personal_project.exam_management_system.dto.ExamSessionDetailDTO;
import com.personal_project.exam_management_system.entity.*;
import com.personal_project.exam_management_system.service.*;
import jakarta.annotation.Resource;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.core.io.FileSystemResource;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.*;
import org.springframework.ui.Model;
import org.springframework.web.servlet.mvc.support.RedirectAttributes;

import java.nio.file.Path;
import java.nio.file.Paths;
import java.time.LocalDate;
import java.time.format.DateTimeFormatter;

import java.util.*;
import java.util.stream.Collectors;

@Controller
@RequestMapping("/admin")
public class AdminController {

    @Autowired
    private StudentService studentService;

    @Autowired
    private RoleService roleService;

    @Autowired
    private UserService userService;

    @Autowired
    private ProctorService proctorService;

    @Autowired
    private CourseService courseService;

    @Autowired
    private ExamRoomService examRoomService;

    @Autowired
    private ExamSessionService examSessionService;

    // Hiển thị dashboard quản trị viên
    @GetMapping("/dashboard-admin")
    public String dashboardAdmin(Model model) {
        model.addAttribute("pageContent", "dashboard-admin");
        return "template-admin";
    }

    // ====================================== Quản lý sinh viên ========================================
    // Hiển thị danh sách sinh viên
    @GetMapping("/manage-students")
    public String manageStudents(Model model) {
        List<Student> students = studentService.findAllStudents();
        model.addAttribute("students", students);
        model.addAttribute("pageContent", "manage-students");
        return "template-admin";  // Trả về layout chung
    }

    // Tìm kiếm sinh viên theo mã sinh viên
    @GetMapping("/manage-students/search")
    public String searchStudents(@RequestParam("studentCode") String studentCode, Model model) {
        List<Student> students = (List<Student>) studentService.findStudentsByStudentCode(studentCode);
        model.addAttribute("students", students);
        model.addAttribute("pageContent", "manage-students");
        return "template-admin";
    }

    // Hiển thị form thêm mới sinh viên
    @GetMapping("/manage-students/create")
    public String showCreateForm(Model model) {
        model.addAttribute("student", new Student());
        return "create-student";
    }

    // Tạo luôn user mới theo thông tin sv
    @PostMapping("/manage-students")
    public String createStudent(Student student) {
        studentService.save(student);

        User user = new User();
        user.setAccountId(student.getStudentCode());
        user.setPassword("iloveyou");

        Role studentRole = roleService.findById(1L);
        user.setRole(studentRole);

        DateTimeFormatter formatter = DateTimeFormatter.ofPattern("yyyy-MM-dd");
        String createdAt = LocalDate.now().format(formatter);
        user.setCreatedAt(createdAt);

        userService.save(user);

        return "redirect:/admin/manage-students";
    }

    // Hiển thị form chỉnh sửa thông tin sinh viên
    @GetMapping("/edit-student")
    public String editStudentForm(@RequestParam("studentCode") String studentCode, Model model) {
        Student student = studentService.findStudentByStudentCode(studentCode);
        if (student == null) {
            model.addAttribute("errorMessage", "Không tìm thấy sinh viên.");
            return "error";
        }
        model.addAttribute("student", student);
        return "edit-student";
    }

    // Xử lý cập nhật thông tin sinh viên
    @PostMapping("/edit-student")
    public String updateStudent(@ModelAttribute("student") Student student, RedirectAttributes redirectAttributes) {
        try {
            Student existingStudent = studentService.findStudentByStudentCode(student.getStudentCode());
            if (existingStudent == null) {
                redirectAttributes.addFlashAttribute("errorMessage", "Sinh viên không tồn tại.");
                return "redirect:/admin/manage-students";
            }
            // Cập nhật thông tin sinh viên
            existingStudent.setFullName(student.getFullName());
            existingStudent.setDepartment(student.getDepartment());
            existingStudent.setClassName(student.getClassName());
            existingStudent.setCohort(student.getCohort());
            existingStudent.setGender(student.getGender());
            existingStudent.setDateOfBirth(student.getDateOfBirth());
            existingStudent.setPhoneNumber(student.getPhoneNumber());
            existingStudent.setEmail(student.getEmail());
            existingStudent.setStatus(student.getStatus());
            existingStudent.setStudentPhoto(student.getStudentPhoto());
            existingStudent.setFacePhoto(student.getFacePhoto());

            studentService.updateStudent(existingStudent);

            redirectAttributes.addFlashAttribute("successMessage", "Cập nhật thông tin sinh viên thành công.");
        } catch (Exception e) {
            redirectAttributes.addFlashAttribute("errorMessage", "Có lỗi xảy ra khi cập nhật thông tin.");
        }
        return "redirect:/admin/manage-students";
    }

    // Xử lý chuyển trạng thái sinh viên sang INACTIVE
    @GetMapping("/delete-student")
    public String deleteStudent(@RequestParam("studentCode") String studentCode, RedirectAttributes redirectAttributes) {
        try {
            Student student = studentService.findStudentByStudentCode(studentCode);
            if (student == null) {
                redirectAttributes.addFlashAttribute("errorMessage", "Không tìm thấy sinh viên.");
                return "redirect:/admin/manage-students";
            }

            student.setStatus(Student.Status.valueOf("INACTIVE"));

            studentService.updateStudent(student);

            redirectAttributes.addFlashAttribute("successMessage", "Sinh viên đã được chuyển sang trạng thái không hoạt động.");
        } catch (Exception e) {
            redirectAttributes.addFlashAttribute("errorMessage", "Có lỗi xảy ra khi chuyển trạng thái sinh viên.");
        }
        return "redirect:/admin/manage-students";
    }

    // ====================================== Quản lý giám thị ========================================
    // Hiển thị danh sách giám thị
    @GetMapping("/manage-proctors")
    public String manageProctors(Model model) {
        List<Proctor> proctors = proctorService.getAllProctors();
        model.addAttribute("proctors", proctors);
        model.addAttribute("pageContent", "manage-proctors");
        return "template-admin";
    }

    // ====================================== Quản lý học phần ========================================
    // Hiển thị tất cả học phần
    @GetMapping("/manage-courses")
    public String getAllCourses(Model model) {
        model.addAttribute("courses", courseService.getAllCourses());
        model.addAttribute("pageContent", "manage-courses");
        return "template-admin";
    }

    // Hiển thị form thêm học phần
    @GetMapping("/manage-courses/course/create")
    public String showAddCourseForm(Model model) {
        model.addAttribute("course", new Course());
        return "create-course";
    }

    @PostMapping("/manage-courses/course/create")
    public String addCourse(@ModelAttribute("course") Course course) {
        courseService.addCourse(course);
        return "redirect:/admin/manage-courses";
    }

    // Hiển thị form sửa học phần
    @GetMapping("/courses/edit/{courseCode}")
    public String showEditCourseForm(@PathVariable("courseCode") String courseCode, Model model) {
        courseService.getAllCourses().stream()
                .filter(c -> c.getCourseCode().equals(courseCode))
                .findFirst().ifPresent(course -> model.addAttribute("course", course));
        return "edit-course";
    }

    @PostMapping("/courses/edit")
    public String updateCourse(@ModelAttribute("course") Course course) {
        courseService.updateCourse(course);
        return "redirect:/admin/manage-courses";
    }

    // Xóa học phần
    @GetMapping("/courses/delete/{courseCode}")
    public String deleteCourse(@PathVariable("courseCode") String courseCode) {
        courseService.deleteCourse(Long.valueOf(courseCode));
        return "redirect:/admin/manage-courses";
    }

    // ====================================== Quản lý phòng thi ========================================
    @GetMapping("/manage-examrooms")
    public String getAllRooms(Model model) {
        List<ExamRoom> rooms = examRoomService.getAllRooms();
        model.addAttribute("rooms", rooms);
        model.addAttribute("pageContent", "manage-examrooms");
        return "template-admin";
    }

    // Lấy thông tin phòng thi theo mã
    @GetMapping("/exam-rooms/{roomCode}")
    public String getRoomByCode(@PathVariable String roomCode, Model model) {
        Optional<ExamRoom> room = examRoomService.getRoomByCode(roomCode);
        if (room.isPresent()) {
            model.addAttribute("room", room.get());
            return "edit-examroom";
        } else {
            return "redirect:/admin/manage-examrooms";
        }
    }

    // Hiển thị form thêm phòng thi
    @GetMapping("/exam-rooms/add")
    public String showAddExamRoomForm(Model model) {
        model.addAttribute("examRoom", new ExamRoom());
        return "create-examroom";
    }

    @PostMapping("/exam-rooms/add")
    public String addExamRoom(@ModelAttribute("examRoom") ExamRoom examRoom) {
        examRoomService.addRoom(examRoom);
        return "redirect:/admin/manage-examrooms";
    }

    // Cập nhật thông tin phòng thi
    @PutMapping("/exam-rooms/{roomCode}")
    public String updateRoom(@PathVariable String roomCode, @ModelAttribute ExamRoom updatedRoom) {
        examRoomService.updateRoom(roomCode, updatedRoom);
        return "redirect:/admin/exam-rooms";
    }

    // Xóa phòng thi
    @DeleteMapping("/exam-rooms/{roomCode}")
    public String deleteRoom(@PathVariable String roomCode) {
        examRoomService.deleteRoom(roomCode);
        return "redirect:/admin/exam-rooms";
    }

    // ====================================== Quản lý ca thi ========================================
    @GetMapping("/manage-exam_sessions")
    public String manageExamSessions(Model model) {
        model.addAttribute("examSessions", examSessionService.getAllExamSessions());
        model.addAttribute("pageContent", "manage-exam_sessions");
        return "template-admin";
    }

    @GetMapping("/manage-exam_sessions/exam_session/{sessionCode}")
    public String getExamSessionDetail(@PathVariable String sessionCode, Model model) {
        ExamSessionDetailDTO examSessionDetails = examSessionService.getExamSessionDetails(sessionCode);

        if (examSessionDetails != null) {
            System.out.println("Exam Session Details: " + examSessionDetails);
            model.addAttribute("examSessionDetails", examSessionDetails);  // Đúng với giao diện HTML
        } else {
            model.addAttribute("errorMessage", "Không tìm thấy thông tin ca thi.");
        }
        model.addAttribute("pageContent", "exam_session-detail");
        return "template-admin";
    }

    @GetMapping("/manage-exam_sessions/create")
    public String showCreateExamSessionPage(Model model) {
        List<ExamRoom> examRooms = examRoomService.getAllRooms();
        List<Course> courses = courseService.getAllCourses();
        List<Proctor> proctors = proctorService.getAllProctors();

        model.addAttribute("examRooms", examRooms);
        model.addAttribute("courses", courses);
        model.addAttribute("proctors", proctors);

        return "create-exam_session";
    }

    @PostMapping("/manage-exam_sessions/create")
    public String createExamSessions(@RequestParam List<String> selectedRoomCodes,
                                     @RequestParam List<String> selectedProctorCodes,
                                     @RequestParam String courseCode,
                                     @RequestParam String examDateTime) {

        // Kiểm tra nếu số phòng và số giám thị không khớp
        if (selectedRoomCodes.size() != selectedProctorCodes.size()) {
            return "redirect:/error";  // Redirect về trang lỗi nếu không đúng
        }

        // Lấy danh sách tất cả sinh viên từ database
        List<Student> allStudents = studentService.findAllStudents();
        List<String> studentCodes = allStudents.stream()
                .map(Student::getStudentCode)
                .collect(Collectors.toList());

        Random rand = new Random();
        int totalRooms = selectedRoomCodes.size();
        int studentsPerRoom = studentCodes.size() / totalRooms;

        for (int i = 0; i < totalRooms; i++) {
            ExamSession examSession = new ExamSession();
            examSession.setSessionCode("SESSION-" + selectedRoomCodes.get(i) +"-"+ selectedProctorCodes.get(i));
            examSession.setCourseCode(courseCode);
            examSession.setRoomCode(String.valueOf(Collections.singletonList(selectedRoomCodes.get(i))));
            examSession.setProctorCode(selectedProctorCodes.get(i));
            examSession.setExamDateTime(examDateTime);
            examSession.setSessionStatus("Scheduled");
            examSession.setReportFilePath(null);

            List<String> randomStudentCodes = getRandomStudents(studentCodes, studentsPerRoom);
            examSession.setStudentCodes(String.join(",", randomStudentCodes));

            examSessionService.save(examSession);

            studentCodes.removeAll(randomStudentCodes);
        }
        return "redirect:/admin/manage-exam_sessions";
    }

    private List<String> getRandomStudents(List<String> students, int count) {
        List<String> randomStudents = new ArrayList<>();
        Random rand = new Random();
        for (int i = 0; i < count; i++) {
            if (students.isEmpty()) break;
            int index = rand.nextInt(students.size());
            randomStudents.add(students.get(index));
            students.remove(index);
        }
        return randomStudents;
    }

    // ====================================== Quản lý báo cáo ========================================
}
