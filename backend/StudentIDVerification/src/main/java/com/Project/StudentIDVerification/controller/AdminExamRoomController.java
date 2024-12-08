package com.Project.StudentIDVerification.controller;

import com.Project.StudentIDVerification.model.ExamRoom;
import com.Project.StudentIDVerification.service.ExamRoomService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@Controller
@RequestMapping("/examrooms")
public class AdminExamRoomController {

    @Autowired
    private ExamRoomService examRoomService;

    // Hiển thị danh sách tất cả các phòng thi
    @GetMapping
    public String listExamRooms(Model model) {
        List<ExamRoom> examRooms = examRoomService.getAllExamRooms();
        model.addAttribute("examRooms", examRooms);
        return "admin/examroom_list"; // View hiển thị danh sách phòng thi
    }

    // Hiển thị form thêm mới phòng thi
    @GetMapping("/new")
    public String showNewExamRoomForm(Model model) {
        ExamRoom newRoom = new ExamRoom();
        newRoom.setCapacity(20); // Gán giá trị mặc định cho capacity
        model.addAttribute("examRoom", newRoom);
        return "admin/examroom_new"; // View hiển thị form thêm phòng thi
    }

    // Xử lý thêm mới phòng thi
    @PostMapping
    public String createExamRoom(@ModelAttribute("examRoom") ExamRoom examRoom) {
        // Đảm bảo danh sách cameras và computers được gán giá trị mặc định
        examRoom.setDefaultCamerasAndComputers();
        examRoomService.createExamRoom(examRoom);
        return "redirect:/examrooms";
    }

    // Hiển thị form chỉnh sửa phòng thi
    @GetMapping("/edit/{id}")
    public String showEditExamRoomForm(@PathVariable String id, Model model) {
        ExamRoom examRoom = examRoomService.getExamRoomById(id)
                .orElseThrow(() -> new IllegalArgumentException("Invalid room ID: " + id));
        model.addAttribute("examRoom", examRoom);
        return "admin/examroom_edit"; // View hiển thị form chỉnh sửa phòng thi
    }

    // Xử lý cập nhật phòng thi
    @PostMapping("/{id}")
    public String updateExamRoom(@PathVariable String id, @ModelAttribute("examRoom") ExamRoom updatedExamRoom) {
        // Đảm bảo danh sách cameras và computers được giữ nguyên khi chỉnh sửa
        ExamRoom existingRoom = examRoomService.getExamRoomById(id)
                .orElseThrow(() -> new IllegalArgumentException("Invalid room ID: " + id));

        updatedExamRoom.setCameras(existingRoom.getCameras());
        updatedExamRoom.setComputers(existingRoom.getComputers());
        examRoomService.updateExamRoom(id, updatedExamRoom);
        return "redirect:/examrooms";
    }

    // Xoá phòng thi
    @GetMapping("/delete/{id}")
    public String deleteExamRoom(@PathVariable String id) {
        examRoomService.deleteExamRoom(id);
        return "redirect:/examrooms";
    }
}
