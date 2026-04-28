package com.contentgen.dto;

import lombok.Data;
import java.util.Map;

@Data
public class ImageResponse {
    
    private String imageUrl;
    private String prompt;
    private String modelUsed;
    private Double generationTime;
    private Long seed;
    private Map<String, Object> parameters;
}