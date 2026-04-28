package com.contentgen.dto;

import jakarta.validation.constraints.*;
import lombok.Data;

@Data
public class ImageRequest {
    
    @NotBlank(message = "Prompt is required")
    @Size(min = 1, max = 1000, message = "Prompt must be between 1 and 1000 characters")
    private String prompt;
    
    @Size(max = 500, message = "Negative prompt must be less than 500 characters")
    private String negativePrompt;
    
    @Min(value = 64, message = "Width must be at least 64")
    @Max(value = 1024, message = "Width must be at most 1024")
    private Integer width = 512;
    
    @Min(value = 64, message = "Height must be at least 64")
    @Max(value = 1024, message = "Height must be at most 1024")
    private Integer height = 512;
    
    @Min(value = 10, message = "Steps must be at least 10")
    @Max(value = 50, message = "Steps must be at most 50")
    private Integer steps = 30;
    
    @DecimalMin(value = "1.0", message = "Guidance scale must be at least 1.0")
    @DecimalMax(value = "20.0", message = "Guidance scale must be at most 20.0")
    private Double guidanceScale = 7.5;
    
    private String style; // realistic, artistic, anime, etc.
}