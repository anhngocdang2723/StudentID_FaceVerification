package com.personal_project.exam_management_system.service;

import com.personal_project.exam_management_system.entity.Proctor;
import com.personal_project.exam_management_system.repository.ProctorRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class ProctorService {

    @Autowired
    private ProctorRepository proctorRepository;

    public Proctor findByProctorCode(String proctorCode) {
        return proctorRepository.findByProctorCode(proctorCode)
                .orElseThrow(() -> new RuntimeException("Proctor not found with code: " + proctorCode));
    }

    public Proctor addProctor(Proctor proctor) {
        return proctorRepository.save(proctor);
    }

    public Proctor updateProctor(Proctor proctor) {
        return proctorRepository.save(proctor);
    }

    public List<Proctor> getAllProctors() {
        return proctorRepository.findAll();
    }
}
