package com.Project.StudentIDVerification.model;

import lombok.Getter;
import lombok.Setter;
import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.mapping.Document;
import org.springframework.data.mongodb.core.mapping.Field;

import java.util.List;
import java.util.Map;

@Setter
@Getter
@Document(collection = "Rooms") // Gắn với collection "Rooms" trong MongoDB
public class Room {

    // Getters và Setters
    @Id
    private String id; // MongoDB tự động tạo ID

    @Field("room_id") // Tương ứng với field "room_id" trong MongoDB
    private String roomId;

    @Field("capacity") // Tương ứng với field "capacity"
    private int capacity;

    @Field("cameras") // Tương ứng với field "cameras"
    private List<Map<String, Object>> cameras; // Danh sách các camera

    @Field("computers") // Tương ứng với field "computers"
    private List<Map<String, Object>> computers; // Danh sách các máy tính

    // Constructor không tham số (bắt buộc cho Spring Data)
    public Room() {
    }

    // Constructor có tham số
    public Room(String roomId, int capacity, List<Map<String, Object>> cameras, List<Map<String, Object>> computers) {
        this.roomId = roomId;
        this.capacity = capacity;
        this.cameras = cameras;
        this.computers = computers;
    }

    @Override
    public String toString() {
        return "Room{" +
                "id='" + id + '\'' +
                ", roomId='" + roomId + '\'' +
                ", capacity=" + capacity +
                ", cameras=" + cameras +
                ", computers=" + computers +
                '}';
    }
}
