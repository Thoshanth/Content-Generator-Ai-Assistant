package com.contentgen.dto;

import com.google.cloud.Timestamp;
import lombok.Data;

import java.util.List;

@Data
public class ChatSessionDTO {
    private String id;
    private String userId;
    private String title;
    private String contentType;
    private Timestamp createdAt;
    private Timestamp updatedAt;
    private List<ChatMessageDTO> messages;
}
