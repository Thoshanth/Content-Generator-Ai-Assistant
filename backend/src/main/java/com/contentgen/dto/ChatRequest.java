package com.contentgen.dto;

import jakarta.validation.constraints.NotBlank;
import lombok.Data;

@Data
public class ChatRequest {
    
    @NotBlank(message = "Prompt is required")
    private String prompt;
    
    private String contentType = "general";
    
    private String sessionId;
    
    private String sessionTitle;
    
    // AI Service v5.0 features
    private String tone = "professional";
    
    private String length = "auto";
    
    private String language = "English";
    
    private Boolean regenerate = false;
    
    private String customInstructions;
    
    private String uploadedText;
}
