// AdminStudentController.java
package com.Project.StudentIDVerification.controller;

import com.Project.StudentIDVerification.model.Student;
import com.Project.StudentIDVerification.repository.StudentRepository;
import com.Project.StudentIDVerification.service.StudentService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageImpl;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Optional;

@Controller
@RequestMapping("/students")
public class AdminStudentController {
    private final StudentService studentService;
    private final StudentRepository studentRepository;
    public AdminStudentController(StudentService studentService, StudentRepository studentRepository) {
        this.studentService = studentService;
        this.studentRepository = studentRepository;
    }

    @GetMapping()
    public String getStudents(@RequestParam(value = "page", defaultValue = "0") int page,
                              @RequestParam(value = "size", defaultValue = "10") int size,
                              @RequestParam(value = "search", required = false) String search,
                              Model model) {

        PageRequest pageRequest = PageRequest.of(page, size);

        Page<Student> studentsPage;
        if (search != null && !search.isEmpty()) {
            List<Student> students = studentService.searchStudents(search);
            studentsPage = new PageImpl<>(students);
            model.addAttribute("searchTerm", search);
        } else {
            studentsPage = studentService.getStudents(pageRequest);
        }

        long totalStudents = studentsPage.getTotalElements();
        int currentPage = studentsPage.getNumber();
        int totalPages = studentsPage.getTotalPages();

        model.addAttribute("studentsPage", studentsPage);
        model.addAttribute("currentPage", currentPage);
        model.addAttribute("totalPages", totalPages);
        model.addAttribute("totalStudents", totalStudents);

        return "admin/student_students";
    }

    @GetMapping("/new")
    public String showNewStudentForm(Model model) {
        Student student = new Student();
//      student.setExamResults(new ArrayList<Student.ExamResults>());
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
