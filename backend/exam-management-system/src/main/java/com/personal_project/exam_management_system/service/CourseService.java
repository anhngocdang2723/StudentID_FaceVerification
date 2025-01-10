package com.personal_project.exam_management_system.service;

import com.personal_project.exam_management_system.entity.Course;
import com.personal_project.exam_management_system.repository.CourseRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Optional;

@Service
public class CourseService {

    private final CourseRepository courseRepository;

    @Autowired
    public CourseService(CourseRepository courseRepository) {
        this.courseRepository = courseRepository;
    }

    // Lấy tất cả các học phần
    public List<Course> getAllCourses() {
        return courseRepository.findAll();
    }

    // Lấy học phần theo mã học phần
    public Optional<Course> getCourseByCode(String courseCode) {
        return courseRepository.findAll().stream()
                .filter(course -> course.getCourseCode().equals(courseCode))
                .findFirst();
    }

    // Thêm mới học phần
    public Course addCourse(Course course) {
        return courseRepository.save(course);
    }

    // Cập nhật thông tin học phần
    public Course updateCourse(Course course) {
        return courseRepository.save(course);
    }

    // Xóa học phần
    public void deleteCourse(Long courseId) {
        courseRepository.deleteById(courseId);
    }
}
