package com.contentgen.dto;

import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.Data;

@Data
public class AIResponse {
    private String content;
    
    // AI Service v5.0 fields
    private String provider;
    private String model;
    
    @JsonProperty("word_count")
    private Integer wordCount;
    
    @JsonProperty("char_count")
    private Integer charCount;
    
    // Backward compatibility - map model to modelUsed
    public String getModelUsed() {
        return model;
    }
    
    public void setModelUsed(String modelUsed) {
        this.model = modelUsed;
    }
}
