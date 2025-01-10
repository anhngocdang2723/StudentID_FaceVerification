package com.personal_project.exam_management_system.repository;

import com.personal_project.exam_management_system.entity.Course;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface CourseRepository extends JpaRepository<Course, Long> {
    // Bạn có thể thêm các phương thức truy vấn nếu cần.
}
