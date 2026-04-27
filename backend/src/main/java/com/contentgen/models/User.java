package com.contentgen.models;

import com.google.cloud.Timestamp;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class User {
    
    private String id;
    private String email;
    private String username;
    private String passwordHash;
    private String fullName;
    private String avatarUrl;
    private String plan = "free";
    private Integer dailyMessageCount = 0;
    private Timestamp lastMessageDate;
    private Timestamp createdAt;
    private Timestamp updatedAt;
}
