package com.Project.StudentIDVerification.service;

import com.Project.StudentIDVerification.DTO.StudentInfoDTO;
import com.Project.StudentIDVerification.model.ExamRoom;
import com.Project.StudentIDVerification.model.Invigilator;
import com.Project.StudentIDVerification.repository.ExamRoomRepository;
import com.Project.StudentIDVerification.repository.InvigilatorRepository;
import com.Project.StudentIDVerification.repository.StudentRepository;
import com.Project.StudentIDVerification.controller.ExamRoomDetails; // Đảm bảo nhập đúng lớp
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.ArrayList;
import java.util.List;

@Service
public class ExamService {

    @Autowired
    private ExamRoomRepository examRoomRepository;

    @Autowired
    private StudentRepository studentRepository;

    @Autowired
    private InvigilatorRepository invigilatorRepository;

    public ExamRoomDetails getExamRoomDetails(String roomId) {
        ExamRoomDetails details = null;

        // Tìm phòng thi theo roomId
        var examRoomOptional = examRoomRepository.findByRoomId(roomId);
        if (examRoomOptional.isPresent()) {
            ExamRoom examRoom = examRoomOptional.get();
            List<StudentInfoDTO> studentsInRoom = getStudentsInExamRoom(roomId);

            // Tìm thông tin giám thị
            Invigilator invigilator = invigilatorRepository.findByInvigilatorId(examRoom.getInvigilatorId()).orElse(null);
            String invigilatorName = invigilator != null ? invigilator.getInvigilatorName() : "Không có thông tin";

            // Tạo đối tượng ExamRoomDetails
            details = new ExamRoomDetails(
                    examRoom.getRoomId(),
                    invigilatorName,
                    "Tên bài thi", // Nếu có, bạn cần có thông tin bài thi trong ExamRoom hoặc từ đâu đó
                    studentsInRoom
            );
        }

        return details;
    }

    public List<StudentInfoDTO> getStudentsInExamRoom(String roomId) {
        List<StudentInfoDTO> studentsInRoom = new ArrayList<>();

        // Tìm phòng thi theo roomId
        examRoomRepository.findByRoomId(roomId).ifPresent(examRoom -> {
            for (ExamRoom.StudentReference studentRef : examRoom.getStudents()) {
                // Tìm từng sinh viên theo stdId
                studentRepository.findByStdId(studentRef.getStdId()).ifPresent(student -> {
                    // Chuyển đổi sang StudentInfoDTO và thêm vào danh sách
                    StudentInfoDTO studentInfo = new StudentInfoDTO(student.getStdName(), student.getStdId(), student.getStdPhone());
                    studentsInRoom.add(studentInfo);
                });
            }
        });

        return studentsInRoom;
    }
}
