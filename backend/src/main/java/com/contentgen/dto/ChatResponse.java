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
}
