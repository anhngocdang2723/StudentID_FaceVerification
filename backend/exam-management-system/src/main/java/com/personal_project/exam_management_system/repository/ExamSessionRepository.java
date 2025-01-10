package com.personal_project.exam_management_system.repository;

import com.personal_project.exam_management_system.dto.ExamSessionDetailDTO;
import com.personal_project.exam_management_system.entity.*;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

import java.util.List;

public interface ExamSessionRepository extends JpaRepository<ExamSession, String> {

//    @Query("SELECT es.sessionCode, c.courseName, er.address, " +
//            "GROUP_CONCAT(s.fullName) AS listStudentNames, " +
//            "p.fullName AS proctorName, es.examDateTime, es.sessionStatus, es.reportFilePath " +
//            "FROM ExamSession es " +
//            "JOIN Course c ON es.courseCode = c.courseCode " +
//            "JOIN ExamRoom er ON es.roomCode = er.roomCode " +
//            "JOIN Proctor p ON es.proctorCode = p.proctorCode " +
//            "JOIN Student s ON (',' || es.studentCodes || ',') LIKE ('%,' || s.studentCode || ',%')" +
////            "JOIN Student s ON ('es.studentCodes') LIKE ('%,s.studentCode') " +
//            "WHERE es.sessionCode = :sessionCode " +
//            "GROUP BY es.sessionCode, c.courseName, er.address, p.fullName, es.examDateTime, es.sessionStatus, es.reportFilePath")
//    List<Object[]> getExamSessionDetailsRaw(@Param("sessionCode") String sessionCode);

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


