package com.contentgen.services;

import com.contentgen.dto.UserProfileDTO;
import com.contentgen.dto.UserStatsDTO;
import com.contentgen.models.User;
import com.contentgen.repositories.ChatMessageRepository;
import com.contentgen.repositories.ChatSessionRepository;
import com.contentgen.repositories.UserRepository;
import com.google.cloud.Timestamp;
import lombok.RequiredArgsConstructor;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;

import java.time.Instant;
import java.time.LocalDate;
import java.time.ZoneId;
import java.util.concurrent.ExecutionException;

@Service
@RequiredArgsConstructor
public class UserService {
    
    private final UserRepository userRepository;
    private final ChatSessionRepository chatSessionRepository;
    private final ChatMessageRepository chatMessageRepository;
    private final PasswordEncoder passwordEncoder;
    
    /**
     * Get user by ID from Firebase Firestore
     */
    public User getUserById(String userId) {
        try {
            return userRepository.findById(userId)
                    .orElseThrow(() -> new RuntimeException("User not found"));
        } catch (ExecutionException | InterruptedException e) {
            throw new RuntimeException("Error fetching user: " + e.getMessage(), e);
        }
    }
    
    /**
     * Get user by email from Firebase Firestore
     */
    public User getUserByEmail(String email) {
        try {
            return userRepository.findByEmail(email)
                    .orElseThrow(() -> new RuntimeException("User not found"));
        } catch (ExecutionException | InterruptedException e) {
            throw new RuntimeException("Error fetching user: " + e.getMessage(), e);
        }
    }
    
    /**
     * Get user by username from Firebase Firestore
     */
    public User getUserByUsername(String username) {
        try {
            return userRepository.findByUsername(username)
                    .orElseThrow(() -> new RuntimeException("User not found"));
        } catch (ExecutionException | InterruptedException e) {
            throw new RuntimeException("Error fetching user: " + e.getMessage(), e);
        }
    }
    
    /**
     * Get user profile with stats from Firebase Firestore
     */
    public UserProfileDTO getUserProfile(String userId) {
        try {
            User user = getUserById(userId);
            
            long totalSessions = chatSessionRepository.countByUserId(userId);
            long totalMessages = chatMessageRepository.countByUserIdAndRole(userId, "user");
            
            UserProfileDTO profile = new UserProfileDTO();
            profile.setId(user.getId());
            profile.setEmail(user.getEmail());
            profile.setUsername(user.getUsername());
            profile.setFullName(user.getFullName());
            profile.setAvatarUrl(user.getAvatarUrl());
            profile.setPlan(user.getPlan());
            profile.setCreatedAt(user.getCreatedAt());
            profile.setTotalSessions(totalSessions);
            profile.setTotalMessages(totalMessages);
            profile.setDailyMessageCount(user.getDailyMessageCount());
            
            return profile;
        } catch (ExecutionException | InterruptedException e) {
            throw new RuntimeException("Error fetching user profile: " + e.getMessage(), e);
        }
    }
    
    /**
     * Update user profile in Firebase Firestore
     */
    public User updateUserProfile(String userId, String fullName, String avatarUrl) {
        try {
            User user = getUserById(userId);
            
            if (fullName != null && !fullName.isBlank()) {
                user.setFullName(fullName);
            }
            
            if (avatarUrl != null) {
                user.setAvatarUrl(avatarUrl);
            }
            
            return userRepository.save(user);
        } catch (ExecutionException | InterruptedException e) {
            throw new RuntimeException("Error updating user profile: " + e.getMessage(), e);
        }
    }
    
    /**
     * Change user password in Firebase Firestore
     */
    public void changePassword(String userId, String oldPassword, String newPassword) {
        try {
            User user = getUserById(userId);
            
            if (!passwordEncoder.matches(oldPassword, user.getPasswordHash())) {
                throw new RuntimeException("Current password is incorrect");
            }
            
            user.setPasswordHash(passwordEncoder.encode(newPassword));
            userRepository.save(user);
        } catch (ExecutionException | InterruptedException e) {
            throw new RuntimeException("Error changing password: " + e.getMessage(), e);
        }
    }
    
    /**
     * Delete user account and all related data from Firebase Firestore
     */
    public void deleteUserAccount(String userId) {
        try {
            // Note: In Firestore, we need to manually delete related documents
            // Consider using Cloud Functions for cascade deletes in production
            userRepository.deleteById(userId);
        } catch (ExecutionException | InterruptedException e) {
            throw new RuntimeException("Error deleting user account: " + e.getMessage(), e);
        }
    }
    
    /**
     * Check if user has reached daily message limit
     */
    public boolean hasReachedDailyLimit(String userId, int dailyLimit) {
        try {
            User user = getUserById(userId);
            
            LocalDate today = LocalDate.now();
            LocalDate lastMessageDate = user.getLastMessageDate() != null 
                ? Instant.ofEpochSecond(user.getLastMessageDate().getSeconds())
                    .atZone(ZoneId.systemDefault())
                    .toLocalDate()
                : null;
            
            // Reset counter if it's a new day
            if (lastMessageDate == null || !lastMessageDate.equals(today)) {
                user.setDailyMessageCount(0);
                user.setLastMessageDate(Timestamp.now());
                userRepository.save(user);
                return false;
            }
            
            return user.getDailyMessageCount() >= dailyLimit;
        } catch (ExecutionException | InterruptedException e) {
            throw new RuntimeException("Error checking daily limit: " + e.getMessage(), e);
        }
    }
    
    /**
     * Increment user's daily message count in Firebase Firestore
     */
    public void incrementDailyMessageCount(String userId) {
        try {
            User user = getUserById(userId);
            
            LocalDate today = LocalDate.now();
            LocalDate lastMessageDate = user.getLastMessageDate() != null 
                ? Instant.ofEpochSecond(user.getLastMessageDate().getSeconds())
                    .atZone(ZoneId.systemDefault())
                    .toLocalDate()
                : null;
            
            // Reset counter if it's a new day
            if (lastMessageDate == null || !lastMessageDate.equals(today)) {
                user.setDailyMessageCount(1);
            } else {
                user.setDailyMessageCount(user.getDailyMessageCount() + 1);
            }
            
            user.setLastMessageDate(Timestamp.now());
            userRepository.save(user);
        } catch (ExecutionException | InterruptedException e) {
            throw new RuntimeException("Error incrementing message count: " + e.getMessage(), e);
        }
    }
    
    /**
     * Get user statistics from Firebase Firestore
     */
    public UserStatsDTO getUserStats(String userId) {
        try {
            long totalSessions = chatSessionRepository.countByUserId(userId);
            long totalMessages = chatMessageRepository.countByUserId(userId);
            long userMessages = chatMessageRepository.countByUserIdAndRole(userId, "user");
            
            User user = getUserById(userId);
            
            UserStatsDTO stats = new UserStatsDTO();
            stats.setTotalSessions(totalSessions);
            stats.setTotalMessages(totalMessages);
            stats.setUserMessages(userMessages);
            stats.setDailyMessageCount(user.getDailyMessageCount());
            stats.setLastMessageDate(user.getLastMessageDate());
            
            return stats;
        } catch (ExecutionException | InterruptedException e) {
            throw new RuntimeException("Error fetching user stats: " + e.getMessage(), e);
        }
    }
    
    /**
     * Check if user has reached daily image generation limit
     */
    public boolean hasReachedDailyImageLimit(String userId, int dailyLimit) {
        try {
            User user = getUserById(userId);
            
            LocalDate today = LocalDate.now();
            LocalDate lastImageDate = user.getLastImageDate() != null 
                ? Instant.ofEpochSecond(user.getLastImageDate().getSeconds())
                    .atZone(ZoneId.systemDefault())
                    .toLocalDate()
                : null;
            
            // Reset counter if it's a new day
            if (lastImageDate == null || !lastImageDate.equals(today)) {
                user.setDailyImageCount(0);
                user.setLastImageDate(Timestamp.now());
                userRepository.save(user);
                return false;
            }
            
            return user.getDailyImageCount() >= dailyLimit;
        } catch (ExecutionException | InterruptedException e) {
            throw new RuntimeException("Error checking daily image limit: " + e.getMessage(), e);
        }
    }
    
    /**
     * Increment user's daily image generation count
     */
    public void incrementDailyImageCount(String userId) {
        try {
            User user = getUserById(userId);
            
            LocalDate today = LocalDate.now();
            LocalDate lastImageDate = user.getLastImageDate() != null 
                ? Instant.ofEpochSecond(user.getLastImageDate().getSeconds())
                    .atZone(ZoneId.systemDefault())
                    .toLocalDate()
                : null;
            
            // Reset counter if it's a new day
            if (lastImageDate == null || !lastImageDate.equals(today)) {
                user.setDailyImageCount(1);
            } else {
                user.setDailyImageCount(user.getDailyImageCount() + 1);
            }
            
            user.setLastImageDate(Timestamp.now());
            userRepository.save(user);
        } catch (ExecutionException | InterruptedException e) {
            throw new RuntimeException("Error incrementing image count: " + e.getMessage(), e);
        }
    }
    
    /**
     * Get user's daily image generation count
     */
    public int getDailyImageCount(String userId) {
        User user = getUserById(userId);
        
        LocalDate today = LocalDate.now();
        LocalDate lastImageDate = user.getLastImageDate() != null 
            ? Instant.ofEpochSecond(user.getLastImageDate().getSeconds())
                .atZone(ZoneId.systemDefault())
                .toLocalDate()
            : null;
        
        // Reset counter if it's a new day
        if (lastImageDate == null || !lastImageDate.equals(today)) {
            return 0;
        }
        
        return user.getDailyImageCount() != null ? user.getDailyImageCount() : 0;
    }
}
