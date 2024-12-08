package com.Project.StudentIDVerification.service;

import java.util.List;
import java.util.Optional;

import org.springframework.stereotype.Service;

import com.Project.StudentIDVerification.model.Invigilator;
import com.Project.StudentIDVerification.repository.InvigilatorRepository;

@Service
public class InvigilatorService {
    private final InvigilatorRepository invigilatorRepository;

    public InvigilatorService(InvigilatorRepository invigilatorRepository) {
        this.invigilatorRepository = invigilatorRepository;
    }

    public List<Invigilator> getAllInvigilators() {
        return invigilatorRepository.findAll();
    }

    public Optional<Invigilator> getInvigilatorById(String id) {
        return invigilatorRepository.findById(id);
    }

    public void addInvigilator(Invigilator invigilator) {
        invigilatorRepository.save(invigilator);
    }

    public void updateInvigilator(String id, Invigilator updatedInvigilator) {
        Optional<Invigilator> existingInvigilatorOpt = invigilatorRepository.findById(id);
        if (existingInvigilatorOpt.isPresent()) {
            Invigilator existingInvigilator = existingInvigilatorOpt.get();
            existingInvigilator.setInvigilatorName(updatedInvigilator.getInvigilatorName());
            existingInvigilator.setInvigilatorEmail(updatedInvigilator.getInvigilatorEmail());
            existingInvigilator.setInvigilatorPhone(updatedInvigilator.getInvigilatorPhone());
            invigilatorRepository.save(existingInvigilator);
        } else {
            throw new RuntimeException("Giám thị không tồn tại với ID: " + id);
        }
    }

    public void deleteInvigilator(String id) {
        if (invigilatorRepository.existsById(id)) {
            invigilatorRepository.deleteById(id);
        } else {
            throw new RuntimeException("Không thể xóa vì giám thị không tồn tại với ID: " + id);
        }
    }
}