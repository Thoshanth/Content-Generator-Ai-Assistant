package com.contentgen.dto;

import lombok.Data;

@Data
public class AIRequest {
    private String prompt;
    private String contentType = "general";
    private String userId;
    
    // AI Service v5.0 features
    private String tone = "professional";
    private String length = "auto";
    private String language = "English";
    private Boolean regenerate = false;
    private String customInstructions;
    private String uploadedText;
}
