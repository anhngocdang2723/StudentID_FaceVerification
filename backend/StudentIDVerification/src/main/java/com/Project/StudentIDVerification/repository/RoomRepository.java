package com.Project.StudentIDVerification.repository;

import com.Project.StudentIDVerification.model.Room;
import org.springframework.data.mongodb.repository.MongoRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface RoomRepository extends MongoRepository<Room, String> {
    // Tìm danh sách phòng dựa trên roomId
    List<Room> findByRoomIdIn(List<String> roomIds);
}
