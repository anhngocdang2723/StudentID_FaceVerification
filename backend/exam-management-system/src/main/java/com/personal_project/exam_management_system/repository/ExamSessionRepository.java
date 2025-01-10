package com.personal_project.exam_management_system.repository;

import com.personal_project.exam_management_system.dto.ExamSessionDetailDTO;
import com.personal_project.exam_management_system.entity.*;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

import java.util.List;

public interface ExamSessionRepository extends JpaRepository<ExamSession, String> {
    @Query("SELECT es FROM ExamSession es WHERE es.studentCodes LIKE %:studentCode%")
    List<ExamSession> findByStudentCode(@Param("studentCode") String studentCode);

    @Query("SELECT es FROM ExamSession es WHERE es.proctorCode LIKE %:proctorCode%")
    List<ExamSession> findByProctorCode(@Param("proctorCode") String proctorCode);

    @Query(value = "SELECT " +
            "es.session_code, " +
            "c.course_name, " +
            "er.address, " +
            "GROUP_CONCAT(s.full_name) AS list_student_names, " +
            "p.full_name AS proctor_name, " +
            "es.exam_date_time, " +
            "es.session_status, " +
            "es.report_file_path " +
            "FROM ExamSessions es " +
            "JOIN Courses c ON es.course_code = c.course_code " +
            "JOIN ExamRooms er ON es.room_code = er.room_code " +
            "JOIN Proctors p ON es.proctor_code = p.proctor_code " +
            "JOIN Students s ON (',' || es.student_codes || ',') LIKE ('%,' || s.student_code || ',%') " +
            "WHERE es.session_code = :sessionCode " +
            "GROUP BY es.session_code, c.course_name, er.address, p.full_name, es.exam_date_time, es.session_status, es.report_file_path",
            nativeQuery = true)
    List<Object[]> getExamSessionDetailsRaw(@Param("sessionCode") String sessionCode);

}


