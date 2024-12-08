package com.Project.StudentIDVerification.service;

import com.Project.StudentIDVerification.model.Exam;
import com.Project.StudentIDVerification.model.ExamRoom;
import com.Project.StudentIDVerification.model.Invigilator;
import com.Project.StudentIDVerification.model.Student;
import com.Project.StudentIDVerification.repository.ExamRepository;
import com.Project.StudentIDVerification.repository.ExamRoomRepository;
import com.Project.StudentIDVerification.repository.InvigilatorRepository;
import com.Project.StudentIDVerification.repository.StudentRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.ArrayList;
import java.util.List;
import java.util.Optional;

@Service
public class ExamRoomService {

    @Autowired
    private ExamRoomRepository examRoomRepository;

    @Autowired
    private ExamRepository examRepository;

    @Autowired
    private InvigilatorRepository invigilatorRepository;

    @Autowired
    private StudentRepository studentRepository;

    public List<ExamRoom> getAllExamRooms() {
        List<ExamRoom> examRooms = examRoomRepository.findAll();

        // Bổ sung tên bài thi, tên giám thị và mã sinh viên
        for (ExamRoom room : examRooms) {
            // Xử lý thông tin bài thi
            if (room.getExamId() != null) {
                System.out.println("[DEBUG] Exam ID: " + room.getExamId());
                Optional<Exam> exam = examRepository.findByExamId(room.getExamId());
                if (exam.isPresent()) {
                    room.setExamName(exam.get().getExamName());
                } else {
                    System.out.println("[ERROR] Exam not found for ID: " + room.getExamId());
                    room.setExamName("Unknown Exam");
                }
            }

            // Xử lý thông tin giám thị
            if (room.getInvigilatorId() != null) {
                System.out.println("[DEBUG] Invigilator ID: " + room.getInvigilatorId());
                Invigilator invigilator = invigilatorRepository.findByInvigilatorId(room.getInvigilatorId());
                if (invigilator != null) {
                    room.setInvigilatorName(invigilator.getInvigilatorName());
                } else {
                    System.out.println("[ERROR] Invigilator not found for ID: " + room.getInvigilatorId());
                    room.setInvigilatorName("Unknown Invigilator");
                }
            }

            // Xử lý thông tin sinh viên và thêm vào phòng thi
            List<String> studentIds = new ArrayList<>();
            if (room.getStudents() != null && !room.getStudents().isEmpty()) {
                for (ExamRoom.StudentRef studentRef : room.getStudents()) {
                    String studentId = studentRef.getStdId();

                    if (studentId != null && !studentId.trim().isEmpty()) {
                        System.out.println("[DEBUG] Student ID in room: " + studentId);
                        Student student = studentRepository.findByStdId(studentId);
                        if (student != null) {
                            studentIds.add(student.getStdId());
                        } else {
                            System.out.println("[ERROR] Student not found for ID: " + studentId);
                        }
                    } else {
                        System.out.println("[ERROR] Invalid Student ID: " + studentId);  // Log rõ ràng lý do
                    }
                }
            }
            room.setStudentIds(studentIds);  // Thêm mã sinh viên vào phòng thi
        }

        // Log thông tin chi tiết về phòng thi
        System.out.println("[INFO] Fetching all exam rooms: " + examRooms.size() + " rooms found.");
        for (ExamRoom room : examRooms) {
            System.out.println("[INFO] Room ID: " + room.getRoomId());
            System.out.println("[INFO] Exam Name: " + room.getExamName());
            System.out.println("[INFO] Invigilator Name: " + room.getInvigilatorName());
            System.out.println("[INFO] Student IDs: " + room.getStudentIds());
        }

        return examRooms;
    }

    // Lấy thông tin phòng thi theo id
    public Optional<ExamRoom> getExamRoomById(String id) {
        Optional<ExamRoom> room = examRoomRepository.findById(id);
        if (room.isPresent()) {
            System.out.println("[INFO] Found exam room with ID: " + id);
        } else {
            System.out.println("[WARNING] Exam room with ID: " + id + " not found.");
        }
        return room;
    }

    // Lấy thông tin phòng thi theo roomId
    public ExamRoom getExamRoomByRoomId(String roomId) {
        ExamRoom room = examRoomRepository.findByRoomId(roomId);
        if (room != null) {
            System.out.println("[INFO] Found exam room with room ID: " + roomId);
        } else {
            System.out.println("[WARNING] Exam room with room ID: " + roomId + " not found.");
        }
        return room;
    }

    // Tạo phòng thi mới
    public void createExamRoom(ExamRoom examRoom) {
        // Kiểm tra trùng roomId
        if (examRoomRepository.findByRoomId(examRoom.getRoomId()) != null) {
            String errorMsg = "Room ID " + examRoom.getRoomId() + " đã tồn tại!";
            System.out.println("[ERROR] " + errorMsg);
            throw new IllegalArgumentException(errorMsg);
        }

        // Gán giá trị mặc định nếu cần thiết
        setDefaultValues(examRoom);

        examRoomRepository.save(examRoom);
        System.out.println("[INFO] Created new exam room with Room ID: " + examRoom.getRoomId());
    }

    // Cập nhật thông tin phòng thi
    public void updateExamRoom(String id, ExamRoom updatedExamRoom) {
        ExamRoom existingRoom = examRoomRepository.findById(id)
                .orElseThrow(() -> {
                    String errorMsg = "Không tìm thấy phòng thi với ID: " + id;
                    System.out.println("[ERROR] " + errorMsg);
                    return new IllegalArgumentException(errorMsg);
                });

        // Cập nhật thông tin
        existingRoom.setRoomId(updatedExamRoom.getRoomId());
        existingRoom.setCapacity(updatedExamRoom.getCapacity());
        existingRoom.setExamId(updatedExamRoom.getExamId());
        existingRoom.setInvigilatorId(updatedExamRoom.getInvigilatorId());
        existingRoom.setStudents(updatedExamRoom.getStudents());

        // Giữ nguyên danh sách cameras và computers (hoặc cập nhật nếu cần)
        if (updatedExamRoom.getCameras() != null) {
            existingRoom.setCameras(updatedExamRoom.getCameras());
        }
        if (updatedExamRoom.getComputers() != null) {
            existingRoom.setComputers(updatedExamRoom.getComputers());
        }

        examRoomRepository.save(existingRoom);
        System.out.println("[INFO] Updated exam room with ID: " + id);
    }

    // Xoá phòng thi
    public void deleteExamRoom(String id) {
        if (examRoomRepository.existsById(id)) {
            examRoomRepository.deleteById(id);
            System.out.println("[INFO] Deleted exam room with ID: " + id);
        } else {
            String errorMsg = "Không tìm thấy phòng thi với ID: " + id;
            System.out.println("[ERROR] " + errorMsg);
            throw new IllegalArgumentException(errorMsg);
        }
    }

    // Gán giá trị mặc định cho phòng thi nếu cần
    private void setDefaultValues(ExamRoom examRoom) {
        if (examRoom.getCameras() == null || examRoom.getCameras().isEmpty()) {
            examRoom.setCameras(List.of(
                    new ExamRoom.Camera("CAM01", "Cam góc trên"),
                    new ExamRoom.Camera("CAM02", "Cam góc dưới")
            ));
            System.out.println("[INFO] Default cameras added to exam room: " + examRoom.getRoomId());
        }

        if (examRoom.getComputers() == null || examRoom.getComputers().isEmpty()) {
            List<ExamRoom.Computer> defaultComputers = new java.util.ArrayList<>();
            for (int i = 1; i <= examRoom.getCapacity(); i++) {
                defaultComputers.add(new ExamRoom.Computer("PC" + String.format("%03d", i), "trống"));
            }
            examRoom.setComputers(defaultComputers);
            System.out.println("[INFO] Default computers added to exam room: " + examRoom.getRoomId());
        }
    }
}
