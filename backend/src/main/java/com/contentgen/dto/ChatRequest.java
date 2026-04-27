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
}
