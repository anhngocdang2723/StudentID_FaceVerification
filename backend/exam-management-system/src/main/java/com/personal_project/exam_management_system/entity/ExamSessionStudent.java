package com.personal_project.exam_management_system.entity;

import jakarta.persistence.*;
import org.springframework.data.annotation.Id;

@Entity
public class ExamSessionStudent {
    @jakarta.persistence.Id
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne
    @JoinColumn(name = "session_code")
    private ExamSession examSession;

    @ManyToOne
    @JoinColumn(name = "student_code")
    private Student student;

    public void setId(Long id) {
        this.id = id;
    }

    public Long getId() {
        return id;
    }
}

