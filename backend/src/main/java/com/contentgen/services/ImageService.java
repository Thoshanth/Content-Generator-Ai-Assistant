package com.contentgen.services;

import com.contentgen.dto.ImageRequest;
import com.contentgen.dto.ImageResponse;
import com.contentgen.models.ChatMessage;
import lombok.RequiredArgsConstructor;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.core.io.FileSystemResource;
import org.springframework.core.io.Resource;
import org.springframework.http.MediaType;
import org.springframework.stereotype.Service;
import org.springframework.web.reactive.function.client.WebClient;

import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.UUID;

@Service
@RequiredArgsConstructor
public class ImageService {
    
    @Value("${ai.service.url}")
    private String aiServiceUrl;
    
    @Value("${image.storage.path}")
    private String imageStoragePath;
    
    private final WebClient.Builder webClientBuilder;
    private final ChatService chatService;
    
    /**
     * Generate image using Python AI service
     */
    public ImageResponse generateImage(ImageRequest request, String userId) {
        WebClient webClient = webClientBuilder.baseUrl(aiServiceUrl).build();
        
        // Build request payload for Python service
        Map<String, Object> payload = new HashMap<>();
        payload.put("prompt", request.getPrompt());
        payload.put("negative_prompt", request.getNegativePrompt());
        payload.put("width", request.getWidth());
        payload.put("height", request.getHeight());
        payload.put("steps", request.getSteps());
        payload.put("guidance_scale", request.getGuidanceScale());
        payload.put("style", request.getStyle());
        payload.put("user_id", userId);
        
        // Call Python service
        ImageResponse response = webClient.post()
                .uri("/image/generate")
                .contentType(MediaType.APPLICATION_JSON)
                .bodyValue(payload)
                .retrieve()
                .bodyToMono(ImageResponse.class)
                .block();
        
        // Save image message to chat history
        if (response != null) {
            saveImageMessage(request, response, userId);
        }
        
        return response;
    }
    
    /**
     * Get available image styles from Python service
     */
    public Map<String, Object> getAvailableStyles() {
        WebClient webClient = webClientBuilder.baseUrl(aiServiceUrl).build();
        
        return webClient.get()
                .uri("/image/styles")
                .retrieve()
                .bodyToMono(Map.class)
                .block();
    }
    
    /**
     * Get image generation presets from Python service
     */
    public Map<String, Object> getImagePresets() {
        WebClient webClient = webClientBuilder.baseUrl(aiServiceUrl).build();
        
        return webClient.get()
                .uri("/image/presets")
                .retrieve()
                .bodyToMono(Map.class)
                .block();
    }
    
    /**
     * Get image resource for serving
     */
    public Resource getImageResource(String filename) {
        Path imagePath = Paths.get(imageStoragePath, filename);
        return new FileSystemResource(imagePath);
    }
    
    /**
     * Save image generation as chat message
     */
    private void saveImageMessage(ImageRequest request, ImageResponse response, String userId) {
        try {
            // Create user message for image request
            ChatMessage userMessage = new ChatMessage();
            userMessage.setId(UUID.randomUUID().toString());
            userMessage.setUserId(userId);
            userMessage.setRole("user");
            userMessage.setContent("Generate image: " + request.getPrompt());
            userMessage.setMessageType("image_request");
            // Note: sessionId will be null for now - we could create a session or handle this differently
            
            // Create assistant message with generated image
            ChatMessage assistantMessage = new ChatMessage();
            assistantMessage.setId(UUID.randomUUID().toString());
            assistantMessage.setUserId(userId);
            assistantMessage.setRole("assistant");
            assistantMessage.setContent("Generated image");
            assistantMessage.setMessageType("image");
            assistantMessage.setImageUrl(response.getImageUrl());
            assistantMessage.setImagePrompt(response.getPrompt());
            assistantMessage.setImageModel(response.getModelUsed());
            assistantMessage.setImageParameters(response.getParameters());
            // Note: sessionId will be null for now - we could create a session or handle this differently
            
            // Save both messages
            chatService.saveMessage(userMessage);
            chatService.saveMessage(assistantMessage);
            
        } catch (Exception e) {
            // Log error but don't fail the image generation
            System.err.println("Failed to save image message: " + e.getMessage());
            e.printStackTrace();
        }
    }
}