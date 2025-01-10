package com.personal_project.exam_management_system.service;

import com.personal_project.exam_management_system.dto.ExamSessionDetailDTO;
import com.personal_project.exam_management_system.entity.ExamSession;
import com.personal_project.exam_management_system.repository.ExamSessionRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Optional;

@Service
public class ExamSessionService {

    @Autowired
    private ExamSessionRepository examSessionRepository;

    public List<ExamSession> getAllExamSessions() {
        return examSessionRepository.findAll();
    }

    public Optional<ExamSession> getExamSessionById(String sessionCode) {
        return examSessionRepository.findById(sessionCode);
    }

    public ExamSessionDetailDTO getExamSessionDetails(String sessionCode) {
        List<Object[]> results = examSessionRepository.getExamSessionDetailsRaw(sessionCode);

        if (!results.isEmpty()) {
            Object[] firstRow = results.get(0); // Dùng chỉ số để lấy giá trị từ kết quả query

            String sessionCodeFromDb = (String) firstRow[0];
            String courseName = (String) firstRow[1];
            String address = (String) firstRow[2];
            String listStudentNames = (String) firstRow[3];  // Đây là chuỗi chứa danh sách tên sinh viên
            String proctorName = (String) firstRow[4];
            String examDateTime = (String) firstRow[5];
            String sessionStatus = (String) firstRow[6];
            String reportFilePath = (String) firstRow[7];

            // Trả về DTO với trường listStudentNames là chuỗi
            return new ExamSessionDetailDTO(sessionCodeFromDb, courseName, address, listStudentNames, proctorName, examDateTime, sessionStatus, reportFilePath);
        }

        return null;
    }

}



