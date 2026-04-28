package com.contentgen.dto;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class ChatResponse {
    private String sessionId;
    private String content;
    private String modelUsed;
    private Integer tokensUsed;
    private String messageId;
    
    // AI Service v5.0 metadata
    private String provider;
    private Integer wordCount;
    private Integer charCount;
    
    // Constructor for backward compatibility
    public ChatResponse(String sessionId, String content, String modelUsed, Integer tokensUsed, String messageId) {
        this.sessionId = sessionId;
        this.content = content;
        this.modelUsed = modelUsed;
        this.tokensUsed = tokensUsed;
        this.messageId = messageId;
    }
}
