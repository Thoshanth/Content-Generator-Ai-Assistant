package com.contentgen.models;

import com.google.cloud.Timestamp;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class ChatSession {
    
    private String id;
    private String userId;
    private String title;
    private String contentType = "general";
    private Timestamp createdAt;
    private Timestamp updatedAt;
}
