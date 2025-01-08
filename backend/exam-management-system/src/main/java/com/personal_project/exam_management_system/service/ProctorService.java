package com.personal_project.exam_management_system.service;

import com.personal_project.exam_management_system.entity.Proctor;
import com.personal_project.exam_management_system.repository.ProctorRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

@Service
public class ProctorService {

    @Autowired
    private ProctorRepository proctorRepository;

    // Phương thức tìm kiếm thông tin giám thị theo mã giám thị
    public Proctor findByProctorCode(String proctorCode) {
        return proctorRepository.findByProctorCode(proctorCode)
                .orElseThrow(() -> new RuntimeException("Proctor not found with code: " + proctorCode));
    }
}
