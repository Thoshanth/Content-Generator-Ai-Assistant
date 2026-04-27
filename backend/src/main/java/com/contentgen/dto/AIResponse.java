package com.contentgen.dto;

import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.Data;

@Data
public class AIResponse {
    private String content;
    
    @JsonProperty("model_used")
    private String modelUsed;
    
    @JsonProperty("tokens_used")
    private Integer tokensUsed;
}
