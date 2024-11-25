package com.Project.StudentIDVerification.service;

import java.util.List;
import java.util.Optional;

import org.apache.xmlbeans.impl.xb.xsdschema.Public;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.Project.StudentIDVerification.model.Invigilator;
import com.Project.StudentIDVerification.repository.InvigilatorRepository;

@Service
public class InvigilatorService {
    @Autowired
    private InvigilatorRepository invigilatorRepository;

    public List<Invigilator> getAllgiamthi(){
        return invigilatorRepository.findAll();
    }

    public Optional<Invigilator> getInvigilatorByid(String id){
        Optional<Invigilator> invigilator= invigilatorRepository.findById(id);
        return invigilator;
    }

    public Invigilator addInvigilator(Invigilator invigilator){
        return invigilatorRepository.save(invigilator);
    }

    public Invigilator updateInvigilator(String id, Invigilator updatedGiamThi) {
         Invigilator existingGiamThi = invigilatorRepository.findByInvigilatorId(id);
        if (existingGiamThi != null) {
            Invigilator giamThi = existingGiamThi.get();
            giamThi.setInvigilatorName(updatedGiamThi.getInvigilatorName());
            giamThi.setInvigilatorEmail(updatedGiamThi.getInvigilatorEmail());
            giamThi.setInvigilatorId(updatedGiamThi.getInvigilatorId());
            giamThi.setInvigilatorPhone(updatedGiamThi.getInvigilatorPhone());
            return invigilatorRepository.save(giamThi);
        } else {
            throw new RuntimeException("Giám thị không tồn tại với ID: " + id);
        }
    }
    
    public void deleteInvigilator(String id){
        invigilatorRepository.deleteById(id);
    }
}
