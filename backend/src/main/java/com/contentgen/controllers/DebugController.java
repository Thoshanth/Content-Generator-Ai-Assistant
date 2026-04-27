package com.contentgen.controllers;

import com.contentgen.models.User;
import com.contentgen.repositories.UserRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.web.bind.annotation.*;

import java.util.Map;
import java.util.concurrent.ExecutionException;

@RestController
@RequestMapping("/api/debug")
@RequiredArgsConstructor
public class DebugController {
    
    private final UserRepository userRepository;
    private final PasswordEncoder passwordEncoder;
    
    /**
     * Check if user exists by email
     */
    @GetMapping("/user/{email}")
    public ResponseEntity<?> checkUser(@PathVariable String email) {
        try {
            boolean exists = userRepository.existsByEmail(email);
            if (exists) {
                User user = userRepository.findByEmail(email).orElse(null);
                return ResponseEntity.ok(Map.of(
                        "exists", true,
                        "userId", user != null ? user.getId() : "null",
                        "email", user != null ? user.getEmail() : "null",
                        "username", user != null ? user.getUsername() : "null",
                        "hasPassword", user != null && user.getPasswordHash() != null
                ));
            } else {
                return ResponseEntity.ok(Map.of("exists", false));
            }
        } catch (ExecutionException | InterruptedException e) {
            return ResponseEntity.badRequest().body(Map.of("error", e.getMessage()));
        }
    }
    
    /**
     * Test password verification
     */
    @PostMapping("/verify-password")
    public ResponseEntity<?> verifyPassword(@RequestBody Map<String, String> request) {
        try {
            String email = request.get("email");
            String password = request.get("password");
            
            User user = userRepository.findByEmail(email).orElse(null);
            if (user == null) {
                return ResponseEntity.ok(Map.of("userFound", false));
            }
            
            boolean matches = passwordEncoder.matches(password, user.getPasswordHash());
            
            return ResponseEntity.ok(Map.of(
                    "userFound", true,
                    "passwordMatches", matches,
                    "userId", user.getId()
            ));
        } catch (Exception e) {
            return ResponseEntity.badRequest().body(Map.of("error", e.getMessage()));
        }
    }
}
