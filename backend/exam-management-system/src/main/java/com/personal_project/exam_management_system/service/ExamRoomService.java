package com.personal_project.exam_management_system.service;

import com.personal_project.exam_management_system.entity.ExamRoom;
import com.personal_project.exam_management_system.repository.ExamRoomRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import java.util.List;
import java.util.Optional;

@Service
public class ExamRoomService {

    @Autowired
    private ExamRoomRepository examRoomRepository;

    public List<ExamRoom> getAllRooms() {
        return examRoomRepository.findAll();
    }

    public Optional<ExamRoom> getRoomByCode(String roomCode) {
        return examRoomRepository.findById(roomCode);
    }

    public ExamRoom addRoom(ExamRoom examRoom) {
        return examRoomRepository.save(examRoom);
    }

    public void deleteRoom(String roomCode) {
        examRoomRepository.deleteById(roomCode);
    }

    public ExamRoom updateRoom(String roomCode, ExamRoom updatedRoom) {
        return examRoomRepository.findById(roomCode).map(room -> {
            room.setAddress(updatedRoom.getAddress());
            room.setMaxCapacity(updatedRoom.getMaxCapacity());
            return examRoomRepository.save(room);
        }).orElseThrow(() -> new RuntimeException("Room not found"));
    }
}

