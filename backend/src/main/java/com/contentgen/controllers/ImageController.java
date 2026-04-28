package com.contentgen.controllers;

import com.contentgen.dto.ImageRequest;
import com.contentgen.dto.ImageResponse;
import com.contentgen.services.ImageService;
import com.contentgen.services.UserService;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.core.io.Resource;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.Authentication;
import org.springframework.web.bind.annotation.*;

import java.util.HashMap;
import java.util.Map;

@RestController
@RequestMapping("/api/images")
@RequiredArgsConstructor
public class ImageController {
    
    private final ImageService imageService;
    private final UserService userService;
    
    @Value("${image.daily.limit}")
    private int dailyImageLimit;
    
    /**
     * Test endpoint to debug authentication (no auth required)
     */
    @GetMapping("/debug-headers")
    public ResponseEntity<?> debugHeaders(HttpServletRequest request) {
        String authHeader = request.getHeader("Authorization");
        
        System.out.println("=== DEBUG HEADERS ===");
        System.out.println("Authorization header: " + authHeader);
        System.out.println("All headers:");
        request.getHeaderNames().asIterator().forEachRemaining(headerName -> {
            System.out.println("  " + headerName + ": " + request.getHeader(headerName));
        });
        
        Map<String, Object> response = new HashMap<>();
        response.put("authHeader", authHeader);
        response.put("hasAuthHeader", authHeader != null);
        response.put("method", request.getMethod());
        response.put("uri", request.getRequestURI());
        
        return ResponseEntity.ok(response);
    }

    /**
     * Test endpoint to debug authentication
     */
    @GetMapping("/test-auth")
    public ResponseEntity<?> testAuth(
            HttpServletRequest request,
            Authentication authentication
    ) {
        String authHeader = request.getHeader("Authorization");
        
        System.out.println("=== AUTH TEST DEBUG ===");
        System.out.println("Authorization header: " + authHeader);
        System.out.println("Authentication object: " + authentication);
        System.out.println("Is authenticated: " + (authentication != null ? authentication.isAuthenticated() : "null"));
        System.out.println("Principal: " + (authentication != null ? authentication.getName() : "null"));
        
        Map<String, Object> response = new HashMap<>();
        response.put("authHeader", authHeader);
        response.put("authenticated", authentication != null && authentication.isAuthenticated());
        response.put("principal", authentication != null ? authentication.getName() : null);
        response.put("authType", authentication != null ? authentication.getClass().getSimpleName() : null);
        
        return ResponseEntity.ok(response);
    }

    /**
     * Generate image using Stable Diffusion
     */
    @PostMapping("/generate")
    public ResponseEntity<?> generateImage(
            Authentication authentication,
            @Valid @RequestBody ImageRequest request
    ) {
        try {
            String userId = authentication.getName();
            
            // Debug logging
            System.out.println("Image generation request from user: " + userId);
            System.out.println("Authentication object: " + authentication);
            System.out.println("Is authenticated: " + authentication.isAuthenticated());
            
            // Check daily image limit (5 images per day for free users)
            if (userService.hasReachedDailyImageLimit(userId, dailyImageLimit)) {
                return ResponseEntity.status(429).body(Map.of(
                    "error", "Daily image generation limit reached",
                    "message", "You have reached your daily limit of " + dailyImageLimit + " images. Please try again tomorrow.",
                    "limit", dailyImageLimit,
                    "resetTime", "24 hours"
                ));
            }
            
            // Generate image
            ImageResponse response = imageService.generateImage(request, userId);
            
            // Increment daily image count
            userService.incrementDailyImageCount(userId);
            
            return ResponseEntity.ok(response);
            
        } catch (Exception e) {
            System.err.println("Image generation error: " + e.getMessage());
            e.printStackTrace();
            return ResponseEntity.status(500).body(Map.of(
                "error", "Image generation failed",
                "message", e.getMessage()
            ));
        }
    }
    
    /**
     * Get available image styles
     */
    @GetMapping("/styles")
    public ResponseEntity<?> getImageStyles() {
        try {
            return ResponseEntity.ok(imageService.getAvailableStyles());
        } catch (Exception e) {
            return ResponseEntity.status(500).body(Map.of(
                "error", "Failed to get styles",
                "message", e.getMessage()
            ));
        }
    }
    
    /**
     * Get image generation presets
     */
    @GetMapping("/presets")
    public ResponseEntity<?> getImagePresets() {
        try {
            return ResponseEntity.ok(imageService.getImagePresets());
        } catch (Exception e) {
            return ResponseEntity.status(500).body(Map.of(
                "error", "Failed to get presets",
                "message", e.getMessage()
            ));
        }
    }
    
    /**
     * Serve generated images
     */
    @GetMapping("/{filename}")
    public ResponseEntity<Resource> getImage(@PathVariable String filename) {
        try {
            Resource resource = imageService.getImageResource(filename);
            
            if (resource.exists() && resource.isReadable()) {
                return ResponseEntity.ok()
                    .contentType(MediaType.IMAGE_PNG)
                    .header(HttpHeaders.CONTENT_DISPOSITION, "inline; filename=\"" + filename + "\"")
                    .body(resource);
            } else {
                return ResponseEntity.notFound().build();
            }
        } catch (Exception e) {
            return ResponseEntity.status(500).build();
        }
    }
    
    /**
     * Get user's daily image usage
     */
    @GetMapping("/usage")
    public ResponseEntity<?> getImageUsage(Authentication authentication) {
        try {
            String userId = authentication.getName();
            int dailyCount = userService.getDailyImageCount(userId);
            
            return ResponseEntity.ok(Map.of(
                "dailyCount", dailyCount,
                "dailyLimit", dailyImageLimit,
                "remaining", Math.max(0, dailyImageLimit - dailyCount),
                "resetTime", "24 hours"
            ));
        } catch (Exception e) {
            return ResponseEntity.status(500).body(Map.of(
                "error", "Failed to get usage",
                "message", e.getMessage()
            ));
        }
    }
}