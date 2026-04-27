package com.contentgen.dto;

import com.google.cloud.Timestamp;
import lombok.Data;

@Data
public class ChatMessageDTO {
    private String id;
    private String sessionId;
    private String role;
    private String content;
    private String modelUsed;
    private Integer tokensUsed;
    private Timestamp createdAt;
}
