package com.personal_project.exam_management_system.entity;

import jakarta.persistence.*;

@Entity
@Table(name = "examrooms")
public class ExamRoom {

    @Id
    @Column(name = "room_code", nullable = false)
    private String roomCode;


    @Column(name = "address", nullable = false)
    private String address;

    @Column(name = "max_capacity" ,nullable = false)
    private int maxCapacity;

    public ExamRoom() {}

    public ExamRoom(String roomCode, String address, int maxCapacity) {
        this.roomCode = roomCode;
        this.address = address;
        this.maxCapacity = maxCapacity;
    }

    // Getters and Setters
    public String getRoomCode() {
        return roomCode;
    }

    public void setRoomCode(String roomCode) {
        this.roomCode = roomCode;
    }

    public String getAddress() {
        return address;
    }

    public void setAddress(String address) {
        this.address = address;
    }

    public int getMaxCapacity() {
        return maxCapacity;
    }

    public void setMaxCapacity(int maxCapacity) {
        this.maxCapacity = maxCapacity;
    }
}
