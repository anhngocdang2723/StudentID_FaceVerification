package com.Project.StudentIDVerification.service;

import com.Project.StudentIDVerification.model.Room;
import com.Project.StudentIDVerification.repository.RoomRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Optional;

@Service
public class RoomService {
    private final RoomRepository roomRepository;

    @Autowired
    public RoomService(RoomRepository roomRepository) {
        this.roomRepository = roomRepository;
    }

    // Lấy danh sách tất cả các phòng
    public List<Room> getAllRooms() {
        return roomRepository.findAll();
    }

    // Lấy thông tin một phòng theo ID
    public Optional<Room> getRoomById(String roomId) {
        return roomRepository.findById(roomId);
    }

    // Thêm mới một phòng
    public Room addRoom(Room room) {
        return roomRepository.save(room);
    }

    // Cập nhật thông tin phòng
    public Room updateRoom(String roomId, Room updatedRoom) {
        Optional<Room> existingRoomOpt = roomRepository.findById(roomId);
        if (existingRoomOpt.isPresent()) {
            Room existingRoom = existingRoomOpt.get();
            existingRoom.setCapacity(updatedRoom.getCapacity());
            existingRoom.setCameras(updatedRoom.getCameras());
            existingRoom.setComputers(updatedRoom.getComputers());
            return roomRepository.save(existingRoom);
        } else {
            throw new RuntimeException("Room with ID " + roomId + " not found");
        }
    }

    // Xóa một phòng
    public void deleteRoom(String roomId) {
        if (roomRepository.existsById(roomId)) {
            roomRepository.deleteById(roomId);
        } else {
            throw new RuntimeException("Room with ID " + roomId + " not found");
        }
    }
}
