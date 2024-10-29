package com.Project.StudentIDVerification.controller;

import com.Project.StudentIDVerification.DTO.StudentInfoDTO;
import com.Project.StudentIDVerification.model.ExamRoom;
import com.Project.StudentIDVerification.model.Invigilator;
import com.Project.StudentIDVerification.model.Student;
import com.Project.StudentIDVerification.repository.ExamRoomRepository;
import com.Project.StudentIDVerification.repository.InvigilatorRepository;
import com.Project.StudentIDVerification.repository.StudentRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;

import java.util.ArrayList;
import java.util.Optional;

@Controller
@RequestMapping("/examroom")
public class ExamRoomController {

    @Autowired
    private ExamRoomRepository examRoomRepository;

    @Autowired
    private StudentRepository studentRepository;

    @Autowired
    private InvigilatorRepository invigilatorRepository; // Đảm bảo đã tiêm InvigilatorRepository

    // Phương thức để hiển thị danh sách sinh viên theo roomId
    @GetMapping("/{roomId}/students")
    public String getStudentsByRoomId(@PathVariable String roomId, Model model) {
        Optional<ExamRoom> examRoomOptional = examRoomRepository.findByRoomId(roomId);
        ArrayList<Object> studentsInfo = new ArrayList<>();

        if (examRoomOptional.isPresent()) {
            ExamRoom examRoom = examRoomOptional.get();
            for (ExamRoom.StudentReference studentReference : examRoom.getStudents()) {
                String stdId = studentReference.getStdId(); // Lấy stdId từ StudentReference
                Optional<Student> studentOptional = Optional.ofNullable(studentRepository.findByStdId(stdId)); // Tìm sinh viên theo stdId

                Invigilator invigilator = invigilatorRepository.findByInvigilatorId(examRoom.getInvigilatorId());

                model.addAttribute("invigilatorName", invigilator != null ? invigilator.getInvigilatorName() : "Chưa có thông tin");

                // Sử dụng ifPresent để thêm thông tin sinh viên vào danh sách nếu tồn tại
                studentOptional.ifPresent(student -> {
                    StudentInfoDTO studentInfoDTO = new StudentInfoDTO(student.getStdName(), student.getStdId(), student.getStdPhone());
                    studentsInfo.add(studentInfoDTO);
                });
            }
            // Đưa danh sách sinh viên vào model để truyền tới giao diện
            model.addAttribute("students", studentsInfo);
            model.addAttribute("roomId", roomId); // Thêm roomId để hiển thị trên giao diện
            return "examRoom"; // Trả về tên file giao diện (examRoom.html)
        } else {
            // Nếu không tìm thấy phòng thi, bạn có thể trả về một thông báo hoặc trang khác
            model.addAttribute("message", "Không tìm thấy phòng thi với ID: " + roomId);
            return "error"; // Trả về tên file giao diện lỗi (error.html)
        }
    }
}
