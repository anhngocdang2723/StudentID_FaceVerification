package com.Project.StudentIDVerification.controller;

import com.Project.StudentIDVerification.model.*;
import com.Project.StudentIDVerification.repository.*;
import com.Project.StudentIDVerification.service.ExamRoomService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.servlet.mvc.support.RedirectAttributes;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;

@Controller
@RequestMapping("/examrooms")
public class AdminExamRoomController {

    @Autowired
    private ExamRoomService examRoomService;

    @Autowired
    private ExamRoomRepository examRoomRepository;

    @Autowired
    private ExamRepository examRepository;

    @Autowired
    private InvigilatorRepository invigilatorRepository;

    @Autowired
    private StudentRepository studentRepository;

    @Autowired
    private RoomRepository roomRepository;

    // Phương thức chuyển đổi từ List<String> (mã sinh viên) thành List<StudentRef>
    private List<ExamRoom.StudentRef> convertToStudentRefs(List<String> studentIds) {
        List<ExamRoom.StudentRef> studentRefs = new ArrayList<>();
        for (String studentId : studentIds) {
            studentRefs.add(new ExamRoom.StudentRef(studentId));
        }
        return studentRefs;
    }

    // Phương thức chuyển đổi từ List<Map<String, Object>> sang List<Camera>
    private List<ExamRoom.Camera> convertToCameras(List<Map<String, Object>> cameraData) {
        List<ExamRoom.Camera> cameras = new ArrayList<>();
        for (Map<String, Object> data : cameraData) {
            ExamRoom.Camera camera = new ExamRoom.Camera();
            camera.setCameraId((String) data.get("id"));
            camera.setLocation((String) data.get("location"));
            cameras.add(camera);
        }
        return cameras;
    }

    // Phương thức chuyển đổi từ List<Map<String, Object>> sang List<Computer>
    private List<ExamRoom.Computer> convertToComputers(List<Map<String, Object>> computerData) {
        List<ExamRoom.Computer> computers = new ArrayList<>();
        for (Map<String, Object> data : computerData) {
            ExamRoom.Computer computer = new ExamRoom.Computer();
            computer.setComputerId((String) data.get("id"));
            computer.setStatus((String) data.get("status"));
            computers.add(computer);
        }
        return computers;
    }

    @GetMapping
    public String listExamRooms(Model model) {
        List<ExamRoom> examRooms = examRoomService.getAllExamRooms();
        model.addAttribute("examRooms", examRooms);
        return "admin/examroom_list";
    }

    @GetMapping("/create")
    public String showCreateExamRoomForm(Model model) {
        List<Room> rooms = roomRepository.findAll();
        model.addAttribute("rooms", rooms);

        List<Invigilator> invigilators = invigilatorRepository.findAll();
        model.addAttribute("invigilators", invigilators);

        List<Exam> exams = examRepository.findAll();
        model.addAttribute("exams", exams);

        return "admin/examroom_create";
    }

    // Kiểm tra và phân bổ sinh viên vào phòng thi
    private List<ExamRoom> assignStudentsToRooms(List<Room> selectedRooms, List<String> invigilatorIds, List<Student> allStudents, String examId) {
        int studentIndex = 0;
        List<ExamRoom> examRooms = new ArrayList<>();

        for (int i = 0; i < selectedRooms.size(); i++) {
            Room room = selectedRooms.get(i);
            String invigilatorId = invigilatorIds.get(i);

            // Phân bổ sinh viên vào phòng thi
            List<String> assignedStudents = new ArrayList<>();
            for (int j = 0; j < room.getCapacity() && studentIndex < allStudents.size(); j++) {
                assignedStudents.add(allStudents.get(studentIndex).getStdId());
                studentIndex++;
            }

            System.out.println("Assigned Students for room " + room.getRoomId() + ": " + assignedStudents);

            // Chuyển danh sách ID sinh viên thành danh sách StudentRef
            List<ExamRoom.StudentRef> studentRefs = convertToStudentRefs(assignedStudents);

            // Tạo đối tượng ExamRoom
            ExamRoom examRoom = new ExamRoom();
            examRoom.setRoomId(room.getRoomId());
            examRoom.setCapacity(room.getCapacity());
            examRoom.setExamId(examId);
            examRoom.setInvigilatorId(invigilatorId);
            examRoom.setStudents(studentRefs);

            examRoom.setDefaultCamerasAndComputers();
            System.out.println("Created ExamRoom: " + examRoom);

            examRoomRepository.save(examRoom);
            examRooms.add(examRoom);
        }

        return examRooms;
    }

    @PostMapping("/create")
    public String createExamRoom(@RequestParam String examId,
                                 @RequestParam List<String> roomIds,
                                 @RequestParam List<String> invigilatorIds,
                                 Model model, RedirectAttributes redirectAttributes) {

        // In thông tin nhận được từ form
//        System.out.println("Received request to create ExamRoom with the following data:");
//        System.out.println("examId: " + examId);
//        System.out.println("roomIds: " + roomIds);
//        System.out.println("invigilatorIds: " + invigilatorIds);

        if (examId == null || roomIds == null || invigilatorIds == null || roomIds.isEmpty() || invigilatorIds.isEmpty()) {
            System.out.println("One or more parameters are missing!");
            model.addAttribute("error", "Dữ liệu không đầy đủ!");
            return "admin/examroom_create";
        }

        // Lấy danh sách Rooms từ roomIds đã chọn
        List<Room> selectedRooms = roomRepository.findByRoomIdIn(roomIds);
        System.out.println("Selected Rooms: " + selectedRooms);

        // Kiểm tra số lượng Room và Invigilator có khớp không
        if (selectedRooms.size() != invigilatorIds.size()) {
            model.addAttribute("error", "Số lượng phòng và giám thị không khớp!");
            return "admin/examroom_create";
        }

        // Lấy toàn bộ danh sách sinh viên
        List<Student> allStudents = studentRepository.findAll();
        if (allStudents.isEmpty()) {
            model.addAttribute("error", "Không đủ sinh viên để phân chia!");
            return "admin/examroom_create";
        }

        // Phân chia sinh viên vào từng phòng
        List<ExamRoom> examRooms = assignStudentsToRooms(selectedRooms, invigilatorIds, allStudents, examId);

        model.addAttribute("examRooms", examRooms);
        return "redirect:/examrooms";
    }

    @GetMapping("/edit/{id}")
    public String showEditExamRoomForm(@PathVariable String id, Model model) {
        ExamRoom examRoom = examRoomService.getExamRoomById(id)
                .orElseThrow(() -> new IllegalArgumentException("Invalid room ID: " + id));
        model.addAttribute("examRoom", examRoom);
        return "admin/examroom_edit"; // View hiển thị form chỉnh sửa phòng thi
    }

    @PostMapping("/{id}")
    public String updateExamRoom(@PathVariable String id, @ModelAttribute("examRoom") ExamRoom updatedExamRoom) {
        ExamRoom existingRoom = examRoomService.getExamRoomById(id)
                .orElseThrow(() -> new IllegalArgumentException("Invalid room ID: " + id));

        updatedExamRoom.setCameras(existingRoom.getCameras());
        updatedExamRoom.setComputers(existingRoom.getComputers());
        examRoomService.updateExamRoom(id, updatedExamRoom);
        return "redirect:/examrooms";
    }

    @GetMapping("/delete/{id}")
    public String deleteExamRoom(@PathVariable String id) {
        examRoomService.deleteExamRoom(id);
        return "redirect:/examrooms";
    }

}
