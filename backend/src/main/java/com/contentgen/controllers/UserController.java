package com.contentgen.controllers;

import com.contentgen.dto.UserProfileDTO;
import com.contentgen.dto.UserStatsDTO;
import com.contentgen.models.User;
import com.contentgen.services.UserService;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.Authentication;
import org.springframework.web.bind.annotation.*;

import java.util.Map;

@RestController
@RequestMapping("/api/user")
@RequiredArgsConstructor
public class UserController {
    
    private final UserService userService;
    
    /**
     * Get current user profile
     */
    @GetMapping("/profile")
    public ResponseEntity<?> getProfile(Authentication authentication) {
        try {
            String userId = authentication.getName();
            UserProfileDTO profile = userService.getUserProfile(userId);
            return ResponseEntity.ok(profile);
        } catch (Exception e) {
            return ResponseEntity.badRequest().body(Map.of("error", e.getMessage()));
        }
    }
    
    /**
     * Update user profile
     */
    @PutMapping("/profile")
    public ResponseEntity<?> updateProfile(
            Authentication authentication,
            @RequestBody Map<String, String> updates
    ) {
        try {
            String userId = authentication.getName();
            String fullName = updates.get("fullName");
            String avatarUrl = updates.get("avatarUrl");
            
            User user = userService.updateUserProfile(userId, fullName, avatarUrl);
            
            return ResponseEntity.ok(Map.of(
                    "message", "Profile updated successfully",
                    "user", user
            ));
        } catch (Exception e) {
            return ResponseEntity.badRequest().body(Map.of("error", e.getMessage()));
        }
    }
    
    /**
     * Change password
     */
    @PutMapping("/password")
    public ResponseEntity<?> changePassword(
            Authentication authentication,
            @RequestBody Map<String, String> passwords
    ) {
        try {
            String userId = authentication.getName();
            String oldPassword = passwords.get("oldPassword");
            String newPassword = passwords.get("newPassword");
            
            userService.changePassword(userId, oldPassword, newPassword);
            
            return ResponseEntity.ok(Map.of("message", "Password changed successfully"));
        } catch (Exception e) {
            return ResponseEntity.badRequest().body(Map.of("error", e.getMessage()));
        }
    }
    
    /**
     * Get user statistics
     */
    @GetMapping("/stats")
    public ResponseEntity<?> getStats(Authentication authentication) {
        try {
            String userId = authentication.getName();
            UserStatsDTO stats = userService.getUserStats(userId);
            return ResponseEntity.ok(stats);
        } catch (Exception e) {
            return ResponseEntity.badRequest().body(Map.of("error", e.getMessage()));
        }
    }
    
    /**
     * Delete user account
     */
    @DeleteMapping("/account")
    public ResponseEntity<?> deleteAccount(Authentication authentication) {
        try {
            String userId = authentication.getName();
            userService.deleteUserAccount(userId);
            return ResponseEntity.ok(Map.of("message", "Account deleted successfully"));
        } catch (Exception e) {
            return ResponseEntity.badRequest().body(Map.of("error", e.getMessage()));
        }
    }
}
