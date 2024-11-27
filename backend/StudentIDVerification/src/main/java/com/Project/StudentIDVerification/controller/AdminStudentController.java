// AdminStudentController.java
package com.Project.StudentIDVerification.controller;

import com.Project.StudentIDVerification.model.Student;
import com.Project.StudentIDVerification.repository.StudentRepository;
import com.Project.StudentIDVerification.service.StudentService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;

import java.util.Optional;

@Controller
@RequestMapping("/students")
public class AdminStudentController {

    @Autowired
    private StudentService studentService;
    @Autowired
    private StudentRepository studentRepository;

    // Danh sách sinh viên
    @GetMapping()
    public String getStudents(@RequestParam(value = "page", defaultValue = "0") int page,
                              @RequestParam(value = "size", defaultValue = "10") int size,
                              Model model) {

        PageRequest pageRequest = PageRequest.of(page, size);

        Page<Student> studentsPage = studentService.getStudents(pageRequest);

        long totalStudents = studentsPage.getTotalElements();

        int currentPage = studentsPage.getNumber();
        int totalPages = studentsPage.getTotalPages();

        // Thêm các giá trị vào model
        model.addAttribute("studentsPage", studentsPage);
        model.addAttribute("currentPage", currentPage);
        model.addAttribute("totalPages", totalPages);
        model.addAttribute("totalStudents", totalStudents);

        return "admin/student_students";
    }

    @GetMapping("/new")
    public String showNewStudentForm(Model model) {
        Student student = new Student();
//        student.setExamResults(new ArrayList<Student.ExamResults>());
        student.setStatus(true);
        model.addAttribute("student", student);
        return "admin/student_addNew";
    }

    @PostMapping("/save")
    public String saveStudent(@ModelAttribute("student") Student student) {
        studentService.createStudent(student);
        return "redirect:/students";
    }

    @GetMapping("/viewmore/{id}")
    public String viewMore(@PathVariable("id") String id, Model model) {
        Optional<Student> student = studentRepository.findById(id);
        if (student.isPresent()) {
            model.addAttribute("student", student.get());
            return "admin/student_viewMore";
        } else {
            return "redirect:/students";
        }
    }

    @GetMapping("/edit/{id}")
    public String showFormForUpdate(@PathVariable("id") String id, Model model) {
        Student student = studentService.getStudentById(id).orElseThrow(() -> new RuntimeException("Student not found"));
        model.addAttribute("student", student);
        return "admin/student_edit";
    }

    @PostMapping("/update/{id}")
    public String updateStudent(@PathVariable("id") String id, @ModelAttribute("student") Student studentDetails) {
        studentService.updateStudent(id, studentDetails);
        return "redirect:/students";
    }

    @GetMapping("/delete/{id}")
    public String deleteStudent(@PathVariable("id") String id) {
        Optional<Student> optionalStudent = studentRepository.findById(id);

        if (optionalStudent.isPresent()) {
            Student student = optionalStudent.get();
            student.setStatus(false);
            studentRepository.save(student);
        }
        return "redirect:/students";
    }
}
