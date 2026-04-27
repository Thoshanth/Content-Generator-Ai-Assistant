package com.contentgen.dto;

import com.google.cloud.Timestamp;
import lombok.Data;

@Data
public class UserStatsDTO {
    private Long totalSessions;
    private Long totalMessages;
    private Long userMessages;
    private Integer dailyMessageCount;
    private Timestamp lastMessageDate;
}
