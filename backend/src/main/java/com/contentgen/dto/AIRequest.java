package com.contentgen.dto;

import lombok.Data;

@Data
public class AIRequest {
    private String prompt;
    private String contentType = "general";
    private String userId;
}
