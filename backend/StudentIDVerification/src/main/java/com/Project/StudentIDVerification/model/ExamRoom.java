package com.Project.StudentIDVerification.model;

import lombok.Getter;
import lombok.Setter;
import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.mapping.Document;
import org.springframework.data.mongodb.core.mapping.Field;

import java.util.ArrayList;
import java.util.List;

@Setter
@Getter
@Document(collection = "ExamRooms")
public class ExamRoom {
    @Id
    private String id; // MongoDB auto-generated _id

    @Field("room_id")
    private String roomId; // Mã phòng, VD: TTKT505

    private int capacity; // Số lượng sinh viên trong phòng thi

    @Field("exam_id")
    private String examId; // FK từ collection Exams

    @Field("invigilator_id")
    private String invigilatorId; // FK từ collection Invigilators

    private List<StudentRef> students; // Danh sách chứa mã sinh viên std_id từ Students

    private List<Camera> cameras; // Danh sách camera gắn giá trị mặc định

    private List<Computer> computers; // Danh sách máy tính gắn giá trị mặc định

    @Setter
    @Getter
    private List<String> studentIds;  // Thêm trường chứa danh sách mã sinh viên


    // Thông tin sau khi join
    private String examName;         // Tên bài thi
    private String invigilatorName;  // Tên giám thị

    // Static block để khởi tạo giá trị mặc định
    {
        setDefaultCamerasAndComputers();
        capacity = 20; // Giá trị mặc định cho capacity
    }

    // Phương thức thiết lập lại giá trị mặc định cho cameras và computers
    public void setDefaultCamerasAndComputers() {
        // Thiết lập danh sách camera mặc định
        cameras = new ArrayList<>();
        cameras.add(new Camera("CAM01", "Cam góc trên"));
        cameras.add(new Camera("CAM02", "Cam góc dưới"));

        // Thiết lập danh sách máy tính mặc định
        computers = new ArrayList<>();
        for (int i = 1; i <= 20; i++) {
            computers.add(new Computer("PC" + String.format("%03d", i), "trống"));
        }
    }

    // Inner classes for embedded objects
    @Setter
    @Getter
    public static class StudentRef {
        @Field("std_id")
        private String stdId; // Mã sinh viên

        public StudentRef() {}

        public StudentRef(String stdId) {
            this.stdId = stdId;
        }
    }

    @Setter
    @Getter
    public static class Camera {
        private String cameraId; // ID của camera
        private String location; // Vị trí camera

        public Camera() {}

        public Camera(String cameraId, String location) {
            this.cameraId = cameraId;
            this.location = location;
        }
    }

    @Setter
    @Getter
    public static class Computer {
        private String computerId; // ID của máy tính
        private String status; // Trạng thái máy tính (trống/bận)

        public Computer() {}

        public Computer(String computerId, String status) {
            this.computerId = computerId;
            this.status = status;
        }
    }


    @Override
    public String toString() {
        return "ExamRoom{" +
                "id='" + id + '\'' +
                ", roomId='" + roomId + '\'' +
                ", capacity=" + capacity +
                ", examId='" + examId + '\'' +
                ", invigilatorId='" + invigilatorId + '\'' +
                ", numberOfStudents=" + (students != null ? students.size() : 0) +
                ", cameras=" + cameras.size() +
                ", computers=" + computers.size() +
                '}';
    }
}
