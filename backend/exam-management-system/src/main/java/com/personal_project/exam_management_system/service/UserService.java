package com.personal_project.exam_management_system.service;

import com.personal_project.exam_management_system.entity.User;
import com.personal_project.exam_management_system.repository.UserRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.Optional;

@Service
public class UserService {

    @Autowired
    private UserRepository userRepository;

    // Xác thực tài khoản và mật khẩu (không mã hóa)
    public Optional<User> login(String accountId, String password) {
        Optional<User> user = userRepository.findByAccountId(accountId);

        if (user.isPresent() && user.get().getPassword().equals(password)) {
            return user;
        }
        return Optional.empty();
    }
}
