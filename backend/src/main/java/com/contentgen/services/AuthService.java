package com.contentgen.services;

import com.contentgen.dto.LoginRequest;
import com.contentgen.dto.RegisterRequest;
import com.contentgen.models.User;
import com.contentgen.repositories.UserRepository;
import com.contentgen.security.JwtUtil;
import lombok.RequiredArgsConstructor;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;

import java.util.HashMap;
import java.util.Map;
import java.util.concurrent.ExecutionException;

@Service
@RequiredArgsConstructor
public class AuthService {
    
    private final UserRepository userRepository;
    private final PasswordEncoder passwordEncoder;
    private final JwtUtil jwtUtil;
    
    /**
     * Register new user in Firebase Firestore
     */
    public User register(RegisterRequest request) {
        try {
            // Check if email already exists
            if (userRepository.existsByEmail(request.getEmail())) {
                throw new RuntimeException("Email already registered");
            }
            
            // Check if username already exists
            if (userRepository.existsByUsername(request.getUsername())) {
                throw new RuntimeException("Username already taken");
            }
            
            // Create new user
            User user = new User();
            user.setEmail(request.getEmail());
            user.setUsername(request.getUsername());
            user.setPasswordHash(passwordEncoder.encode(request.getPassword()));
            user.setFullName(request.getFullName());
            user.setPlan("free");
            user.setDailyMessageCount(0);
            
            return userRepository.save(user);
        } catch (ExecutionException | InterruptedException e) {
            throw new RuntimeException("Error registering user: " + e.getMessage(), e);
        }
    }
    
    /**
     * Login user and generate JWT tokens
     */
    public Map<String, String> login(LoginRequest request) {
        try {
            System.out.println("Login attempt for email: " + request.getEmail());
            
            // Get user from Firebase
            User user = userRepository.findByEmail(request.getEmail())
                    .orElseThrow(() -> {
                        System.out.println("User not found: " + request.getEmail());
                        return new RuntimeException("User not found");
                    });
            
            System.out.println("User found: " + user.getEmail());
            System.out.println("Password hash exists: " + (user.getPasswordHash() != null));
            System.out.println("Password hash length: " + (user.getPasswordHash() != null ? user.getPasswordHash().length() : 0));
            
            // Verify password
            boolean matches = passwordEncoder.matches(request.getPassword(), user.getPasswordHash());
            System.out.println("Password matches: " + matches);
            
            if (!matches) {
                throw new RuntimeException("Invalid password");
            }
            
            // Generate access and refresh tokens
            String accessToken = jwtUtil.generateToken(user.getId(), user.getEmail());
            String refreshToken = jwtUtil.generateRefreshToken(user.getId(), user.getEmail());
            System.out.println("Tokens generated successfully");
            
            Map<String, String> tokens = new HashMap<>();
            tokens.put("accessToken", accessToken);
            tokens.put("refreshToken", refreshToken);
            
            return tokens;
        } catch (ExecutionException | InterruptedException e) {
            System.out.println("Error during login: " + e.getMessage());
            throw new RuntimeException("Error during login: " + e.getMessage(), e);
        }
    }
    
    /**
     * Refresh access token using refresh token
     */
    public Map<String, String> refreshToken(String refreshToken) {
        try {
            // Validate refresh token
            if (!jwtUtil.validateRefreshToken(refreshToken)) {
                throw new RuntimeException("Invalid or expired refresh token");
            }
            
            // Extract user info from refresh token
            String userId = jwtUtil.extractUserId(refreshToken);
            String email = jwtUtil.extractEmail(refreshToken);
            
            // Verify user still exists
            User user = userRepository.findById(userId)
                    .orElseThrow(() -> new RuntimeException("User not found"));
            
            // Generate new access token
            String newAccessToken = jwtUtil.generateToken(user.getId(), user.getEmail());
            
            Map<String, String> tokens = new HashMap<>();
            tokens.put("accessToken", newAccessToken);
            tokens.put("refreshToken", refreshToken); // Return same refresh token
            
            return tokens;
        } catch (ExecutionException | InterruptedException e) {
            throw new RuntimeException("Error refreshing token: " + e.getMessage(), e);
        }
    }
    
    /**
     * Validate JWT token
     */
    public boolean validateToken(String token) {
        return jwtUtil.validateToken(token);
    }
    
    /**
     * Extract user ID from JWT token
     */
    public String getUserIdFromToken(String token) {
        return jwtUtil.extractUserId(token);
    }
}
