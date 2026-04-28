package com.contentgen.dto;

import com.google.cloud.Timestamp;
import lombok.Data;
import java.util.Map;

@Data
public class ChatMessageDTO {
    private String id;
    private String sessionId;
    private String role;
    private String content;
    private String modelUsed;
    private Integer tokensUsed;
    private Timestamp createdAt;
    
    // Image generation fields
    private String messageType = "text"; // 'text' or 'image'
    private String imageUrl;
    private String imagePrompt;
    private String imageModel;
    private Map<String, Object> imageParameters;
}
