package com.Project.StudentIDVerification.controller;

import ch.qos.logback.core.model.Model;
import com.Project.StudentIDVerification.DTO.StudentInfoDTO;
import com.Project.StudentIDVerification.model.ExamRoom;
import com.Project.StudentIDVerification.model.Invigilator;
import com.Project.StudentIDVerification.model.Student;
import com.Project.StudentIDVerification.repository.ExamRoomRepository;
import com.Project.StudentIDVerification.repository.InvigilatorRepository;
import com.Project.StudentIDVerification.repository.StudentRepository;
import jakarta.servlet.http.HttpServletResponse;
import org.apache.poi.ss.usermodel.Row;
import org.apache.poi.ss.usermodel.Sheet;
import org.apache.poi.ss.usermodel.Workbook;
import org.apache.poi.xssf.usermodel.XSSFWorkbook;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.servlet.ModelAndView;

import java.io.IOException;
import java.util.ArrayList;
import java.util.Optional;

@Controller
@RequestMapping("/examroom")
public class ExamRoomController {

    private final ExamRoomRepository examRoomRepository;
    private final StudentRepository studentRepository;
    private final InvigilatorRepository invigilatorRepository;

    public ExamRoomController(ExamRoomRepository examRoomRepository, StudentRepository studentRepository, InvigilatorRepository invigilatorRepository) {
        this.examRoomRepository = examRoomRepository;
        this.studentRepository = studentRepository;
        this.invigilatorRepository = invigilatorRepository;
    }

    @GetMapping("/{roomId}/students")
    public ModelAndView getStudentsByRoomId(@PathVariable String roomId) {
        ModelAndView modelAndView = new ModelAndView();

        Optional<ExamRoom> examRoomOptional = Optional.ofNullable(examRoomRepository.findByRoomId(roomId));

        if (examRoomOptional.isPresent()) {
            ExamRoom examRoom = examRoomOptional.get();
            ArrayList<StudentInfoDTO> studentsInfo = new ArrayList<>();

            for (ExamRoom.StudentRef studentReference : examRoom.getStudents()) {
                String stdId = studentReference.getStdId();
                Optional<Student> studentOptional = Optional.ofNullable(studentRepository.findByStdId(stdId));
                studentOptional.ifPresent(student -> {
                    StudentInfoDTO studentInfoDTO = new StudentInfoDTO(student.getStdName(), student.getStdId(), student.getStdPhone());
                    studentsInfo.add(studentInfoDTO);
                });
            }

            Invigilator invigilator = invigilatorRepository.findByInvigilatorId(examRoom.getInvigilatorId());
            String invigilatorName = invigilator != null ? invigilator.getInvigilatorName() : "Chưa có thông tin";

            // Thêm dữ liệu vào ModelAndView
            modelAndView.addObject("students", studentsInfo);
            modelAndView.addObject("invigilatorName", invigilatorName);
            modelAndView.addObject("roomId", roomId);
            modelAndView.addObject("cameras", examRoom.getCameras());
            modelAndView.addObject("computers", examRoom.getComputers());

            // Đặt View
            modelAndView.setViewName("examRoom");
        } else {
            modelAndView.addObject("message", "Không tìm thấy phòng thi với ID: " + roomId);
            modelAndView.setViewName("error");
        }

        return modelAndView;
    }

    // Xuất file Excel danh sách sinh viên
    @PostMapping("/{roomId}/export")
    @ResponseBody
    public void exportStudentsToExcel(@PathVariable String roomId, HttpServletResponse response) throws IOException {
        Optional<ExamRoom> examRoomOptional = Optional.ofNullable(examRoomRepository.findByRoomId(roomId));

        if (examRoomOptional.isPresent()) {
            ExamRoom examRoom = examRoomOptional.get();
            ArrayList<StudentInfoDTO> studentsInfo = new ArrayList<>();

            // Lấy danh sách sinh viên
            for (ExamRoom.StudentRef studentReference : examRoom.getStudents()) {
                String stdId = studentReference.getStdId();
                Optional<Student> studentOptional = Optional.ofNullable(studentRepository.findByStdId(stdId));
                studentOptional.ifPresent(student -> {
                    StudentInfoDTO studentInfoDTO = new StudentInfoDTO(student.getStdName(), student.getStdId(), student.getStdPhone());
                    studentsInfo.add(studentInfoDTO);
                });
            }

            // Tạo workbook và sheet
            Workbook workbook = new XSSFWorkbook();
            Sheet sheet = workbook.createSheet("Students");

            // Header
            Row headerRow = sheet.createRow(0);
            headerRow.createCell(0).setCellValue("Student ID");
            headerRow.createCell(1).setCellValue("Student Name");
            headerRow.createCell(2).setCellValue("Phone");

            // Ghi dữ liệu vào sheet
            int rowNum = 1;
            for (StudentInfoDTO student : studentsInfo) {
                Row row = sheet.createRow(rowNum++);
                row.createCell(0).setCellValue(student.getStdId());
                row.createCell(1).setCellValue(student.getStdName());
                row.createCell(2).setCellValue(student.getStdPhone());
            }

            // Thiết lập phản hồi
            response.setContentType("application/vnd.openxmlformats-officedocument.spreadsheetml.sheet");
            response.setHeader("Content-Disposition", "attachment; filename=students.xlsx");
            workbook.write(response.getOutputStream());
            workbook.close();
        } else {
            response.sendError(HttpServletResponse.SC_NOT_FOUND, "Không tìm thấy phòng thi với ID: " + roomId);
        }
    }
}
