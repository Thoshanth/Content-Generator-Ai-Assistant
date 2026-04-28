package com.contentgen.services;

import com.contentgen.dto.AIRequest;
import com.contentgen.dto.AIResponse;
import com.contentgen.models.ChatMessage;
import lombok.RequiredArgsConstructor;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.MediaType;
import org.springframework.http.codec.ServerSentEvent;
import org.springframework.stereotype.Service;
import org.springframework.web.reactive.function.client.WebClient;
import reactor.core.publisher.Flux;

import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

@Service
@RequiredArgsConstructor
public class AIProxyService {
    
    @Value("${ai.service.url}")
    private String aiServiceUrl;
    
    private final WebClient.Builder webClientBuilder;
    
    /**
     * Call Python AI service (non-streaming)
     */
    public AIResponse generateContent(AIRequest request, List<ChatMessage> conversationHistory) {
        WebClient webClient = webClientBuilder.baseUrl(aiServiceUrl).build();
        
        // Convert conversation history to format expected by Python service
        List<Map<String, String>> history = conversationHistory.stream()
                .map(msg -> {
                    Map<String, String> map = new HashMap<>();
                    map.put("role", msg.getRole());
                    map.put("content", msg.getContent());
                    return map;
                })
                .collect(Collectors.toList());
        
        // Build request payload with v5.0 features
        Map<String, Object> payload = new HashMap<>();
        payload.put("prompt", request.getPrompt());
        payload.put("content_type", request.getContentType());
        payload.put("conversation_history", history);
        payload.put("user_id", request.getUserId());
        payload.put("tone", request.getTone());
        payload.put("length", request.getLength());
        payload.put("language", request.getLanguage());
        payload.put("regenerate", request.getRegenerate());
        
        if (request.getCustomInstructions() != null) {
            payload.put("custom_instructions", request.getCustomInstructions());
        }
        if (request.getUploadedText() != null) {
            payload.put("uploaded_text", request.getUploadedText());
        }
        
        // Call Python service
        return webClient.post()
                .uri("/chat/")
                .contentType(MediaType.APPLICATION_JSON)
                .bodyValue(payload)
                .retrieve()
                .bodyToMono(AIResponse.class)
                .block();
    }
    
    /**
     * Call Python AI service with streaming
     */
    public Flux<ServerSentEvent<String>> generateContentStream(
            AIRequest request, 
            List<ChatMessage> conversationHistory
    ) {
        WebClient webClient = webClientBuilder.baseUrl(aiServiceUrl).build();
        
        // Convert conversation history
        List<Map<String, String>> history = conversationHistory.stream()
                .map(msg -> {
                    Map<String, String> map = new HashMap<>();
                    map.put("role", msg.getRole());
                    map.put("content", msg.getContent());
                    return map;
                })
                .collect(Collectors.toList());
        
        // Build request payload with v5.0 features
        Map<String, Object> payload = new HashMap<>();
        payload.put("prompt", request.getPrompt());
        payload.put("content_type", request.getContentType());
        payload.put("conversation_history", history);
        payload.put("user_id", request.getUserId());
        payload.put("tone", request.getTone());
        payload.put("length", request.getLength());
        payload.put("language", request.getLanguage());
        payload.put("regenerate", request.getRegenerate());
        
        if (request.getCustomInstructions() != null) {
            payload.put("custom_instructions", request.getCustomInstructions());
        }
        if (request.getUploadedText() != null) {
            payload.put("uploaded_text", request.getUploadedText());
        }
        
        // Call Python service with streaming
        return webClient.post()
                .uri("/chat/stream")
                .contentType(MediaType.APPLICATION_JSON)
                .bodyValue(payload)
                .retrieve()
                .bodyToFlux(String.class)
                .map(data -> ServerSentEvent.<String>builder()
                        .data(data)
                        .build());
    }
}
