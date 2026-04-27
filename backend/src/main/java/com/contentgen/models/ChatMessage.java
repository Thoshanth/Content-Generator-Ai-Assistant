package com.contentgen.models;

import com.google.cloud.Timestamp;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class ChatMessage {
    
    private String id;
    private String sessionId;
    private String userId;
    private String role; // 'user' or 'assistant'
    private String content;
    private String modelUsed;
    private Integer tokensUsed;
    private Timestamp createdAt;
}
