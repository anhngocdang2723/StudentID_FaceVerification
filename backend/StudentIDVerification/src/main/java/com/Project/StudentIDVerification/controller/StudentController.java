// StudentController.java
package com.Project.StudentIDVerification.controller;

import com.Project.StudentIDVerification.model.Student;
import com.Project.StudentIDVerification.model.Student.ExamResults;
import com.Project.StudentIDVerification.repository.StudentRepository;
import com.Project.StudentIDVerification.service.StudentService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;

import java.util.ArrayList;
import java.util.Optional;

@Controller
@RequestMapping("/students")
public class StudentController {

    @Autowired
    private StudentService studentService;
    @Autowired
    private StudentRepository studentRepository;

    @GetMapping
    public String viewHomePage(Model model) {
        model.addAttribute("listStudents", studentService.getAllStudents(true));
        model.addAttribute("totalStudents", studentService.getTotalStudents());
        return "student_students";
    }

    @GetMapping("/new")
    public String showNewStudentForm(Model model) {
        Student student = new Student();
//        student.setExamResults(new ArrayList<Student.ExamResults>());
        student.setStatus(true);
        model.addAttribute("student", student);
        return "student_addNew";
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
            return "student_viewMore";
        } else {
            return "redirect:/students";
        }
    }

    @GetMapping("/edit/{id}")
    public String showFormForUpdate(@PathVariable("id") String id, Model model) {
        Student student = studentService.getStudentById(id).orElseThrow(() -> new RuntimeException("Student not found"));
        model.addAttribute("student", student);
        return "student_edit";
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
