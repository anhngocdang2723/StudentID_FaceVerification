package com.Project.StudentIDVerification.controller;

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
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;

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

    // Lấy dữ liệu phòng thi
    @GetMapping("/{roomId}/students")
    public String getStudentsByRoomId(@PathVariable String roomId, Model model) {
        Optional<ExamRoom> examRoomOptional = examRoomRepository.findByRoomId(roomId);
        ArrayList<Object> studentsInfo = new ArrayList<>();

        if (examRoomOptional.isPresent()) {
            ExamRoom examRoom = examRoomOptional.get();
            for (ExamRoom.StudentReference studentReference : examRoom.getStudents()) {
                String stdId = studentReference.getStdId();
                Optional<Student> studentOptional = Optional.ofNullable(studentRepository.findByStdId(stdId)); // Tìm sinh viên theo stdId

                Invigilator invigilator = invigilatorRepository.findByInvigilatorId(examRoom.getInvigilatorId());

                model.addAttribute("invigilatorName", invigilator != null ? invigilator.getInvigilatorName() : "Chưa có thông tin");

                studentOptional.ifPresent(student -> {
                    StudentInfoDTO studentInfoDTO = new StudentInfoDTO(student.getStdName(), student.getStdId(), student.getStdPhone());
                    studentsInfo.add(studentInfoDTO);
                });
            }
            model.addAttribute("students", studentsInfo);
            model.addAttribute("roomId", roomId);
            return "examRoom";
        } else {
            model.addAttribute("message", "Không tìm thấy phòng thi với ID: " + roomId);
            return "error";
        }
    }

    // Xuất file excel
    @PostMapping("/{roomId}/export")
    @ResponseBody
    public void exportStudentsToExcel(@PathVariable String roomId, HttpServletResponse response) throws IOException {
        Optional<ExamRoom> examRoomOptional = examRoomRepository.findByRoomId(roomId);

        if (examRoomOptional.isPresent()) {
            ExamRoom examRoom = examRoomOptional.get();
            ArrayList<StudentInfoDTO> studentsInfo = new ArrayList<>();
            for (ExamRoom.StudentReference studentReference : examRoom.getStudents()) {
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

            // Tạo header
            Row headerRow = sheet.createRow(0);
            headerRow.createCell(0).setCellValue("Student ID");
            headerRow.createCell(1).setCellValue("Student Name");
            headerRow.createCell(2).setCellValue("Phone");

            // Thêm dữ liệu vào sheet
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
