package com.contentgen.dto;

import com.google.cloud.Timestamp;
import lombok.Data;

@Data
public class UserProfileDTO {
    private String id;
    private String email;
    private String username;
    private String fullName;
    private String avatarUrl;
    private String plan;
    private Timestamp createdAt;
    private Long totalSessions;
    private Long totalMessages;
    private Integer dailyMessageCount;
}
