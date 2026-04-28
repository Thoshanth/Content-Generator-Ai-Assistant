package com.contentgen.controllers;

import com.contentgen.dto.*;
import com.contentgen.models.ChatMessage;
import com.contentgen.models.ChatSession;
import com.contentgen.services.AIProxyService;
import com.contentgen.services.ChatService;
import com.contentgen.services.UserService;
import jakarta.validation.Valid;
import lombok.RequiredArgsConstructor;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.http.codec.ServerSentEvent;
import org.springframework.security.core.Authentication;
import org.springframework.web.bind.annotation.*;
import reactor.core.publisher.Flux;

import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/api/chat")
@RequiredArgsConstructor
public class ChatController {
    
    private final ChatService chatService;
    private final AIProxyService aiProxyService;
    private final UserService userService;
    
    @Value("${rate.limit.daily}")
    private int dailyLimit;
    
    @Value("${rate.limit.enabled}")
    private boolean rateLimitEnabled;
    
    /**
     * Send message and get AI response (non-streaming)
     */
    @PostMapping("/message")
    public ResponseEntity<?> sendMessage(
            Authentication authentication,
            @Valid @RequestBody ChatRequest request
    ) {
        try {
            String userId = authentication.getName();
            
            // Check rate limit (disabled by default)
            if (rateLimitEnabled && userService.hasReachedDailyLimit(userId, dailyLimit)) {
                return ResponseEntity.status(429).body(Map.of(
                        "error", "Daily message limit reached",
                        "limit", dailyLimit
                ));
            }
            
            // Create or get session
            ChatSession session;
            if (request.getSessionId() != null) {
                session = chatService.getSessionById(request.getSessionId(), userId);
            } else {
                String title = request.getSessionTitle() != null 
                        ? request.getSessionTitle() 
                        : "New Chat";
                session = chatService.createSession(userId, title, request.getContentType());
            }
            
            // Save user message to database
            ChatMessage userMessage = chatService.saveUserMessage(
                    session.getId(), 
                    userId, 
                    request.getPrompt()
            );
            
            // Get last 5 messages for context from database
            List<ChatMessage> conversationHistory = chatService.getLastNMessages(session.getId(), 5);
            
            // Call AI service
            AIRequest aiRequest = new AIRequest();
            aiRequest.setPrompt(request.getPrompt());
            aiRequest.setContentType(request.getContentType());
            aiRequest.setUserId(userId);
            aiRequest.setTone(request.getTone());
            aiRequest.setLength(request.getLength());
            aiRequest.setLanguage(request.getLanguage());
            aiRequest.setRegenerate(request.getRegenerate());
            aiRequest.setCustomInstructions(request.getCustomInstructions());
            aiRequest.setUploadedText(request.getUploadedText());
            
            AIResponse aiResponse = aiProxyService.generateContent(aiRequest, conversationHistory);
            
            // Save AI response to database
            ChatMessage assistantMessage = chatService.saveAssistantMessage(
                    session.getId(),
                    userId,
                    aiResponse.getContent(),
                    aiResponse.getModel(),
                    aiResponse.getWordCount() // Use word count as token approximation
            );
            
            // Increment user's daily message count in database
            userService.incrementDailyMessageCount(userId);
            
            // Return response with v5.0 metadata
            ChatResponse response = new ChatResponse();
            response.setSessionId(session.getId());
            response.setContent(aiResponse.getContent());
            response.setModelUsed(aiResponse.getModel());
            response.setTokensUsed(aiResponse.getWordCount()); // Use word count as token approximation
            response.setMessageId(assistantMessage.getId());
            response.setProvider(aiResponse.getProvider());
            response.setWordCount(aiResponse.getWordCount());
            response.setCharCount(aiResponse.getCharCount());
            
            return ResponseEntity.ok(response);
            
        } catch (Exception e) {
            return ResponseEntity.badRequest().body(Map.of("error", e.getMessage()));
        }
    }
    
    /**
     * Send message and get AI response (streaming)
     */
    @PostMapping(value = "/message/stream", produces = MediaType.TEXT_EVENT_STREAM_VALUE)
    public Flux<ServerSentEvent<String>> sendMessageStream(
            Authentication authentication,
            @Valid @RequestBody ChatRequest request
    ) {
        String userId = authentication.getName();
        
        // Check rate limit (disabled by default)
        if (rateLimitEnabled && userService.hasReachedDailyLimit(userId, dailyLimit)) {
            return Flux.just(ServerSentEvent.<String>builder()
                    .data("{\"error\": \"Daily message limit reached\"}")
                    .build());
        }
        
        // Create or get session
        ChatSession session;
        if (request.getSessionId() != null) {
            session = chatService.getSessionById(request.getSessionId(), userId);
        } else {
            String title = request.getSessionTitle() != null 
                    ? request.getSessionTitle() 
                    : "New Chat";
            session = chatService.createSession(userId, title, request.getContentType());
        }
        
        // Save user message to database
        chatService.saveUserMessage(session.getId(), userId, request.getPrompt());
        
        // Get conversation history from database
        List<ChatMessage> conversationHistory = chatService.getLastNMessages(session.getId(), 5);
        
        // Call AI service with streaming
        AIRequest aiRequest = new AIRequest();
        aiRequest.setPrompt(request.getPrompt());
        aiRequest.setContentType(request.getContentType());
        aiRequest.setUserId(userId);
        aiRequest.setTone(request.getTone());
        aiRequest.setLength(request.getLength());
        aiRequest.setLanguage(request.getLanguage());
        aiRequest.setRegenerate(request.getRegenerate());
        aiRequest.setCustomInstructions(request.getCustomInstructions());
        aiRequest.setUploadedText(request.getUploadedText());
        
        // Increment daily message count in database
        userService.incrementDailyMessageCount(userId);
        
        return aiProxyService.generateContentStream(aiRequest, conversationHistory);
    }
    
    /**
     * Get all chat sessions for user from database
     */
    @GetMapping("/sessions")
    public ResponseEntity<?> getSessions(Authentication authentication) {
        try {
            String userId = authentication.getName();
            System.out.println("ChatController: Getting sessions for userId: " + userId);
            
            List<ChatSessionDTO> sessions = chatService.getUserSessions(userId);
            System.out.println("ChatController: Retrieved " + sessions.size() + " sessions");
            
            if (!sessions.isEmpty()) {
                System.out.println("ChatController: First session sample: " + sessions.get(0));
            }
            
            return ResponseEntity.ok(sessions);
        } catch (Exception e) {
            System.err.println("ChatController: Error getting sessions: " + e.getMessage());
            e.printStackTrace();
            return ResponseEntity.badRequest().body(Map.of("error", e.getMessage()));
        }
    }
    
    /**
     * Get session with messages from database
     */
    @GetMapping("/sessions/{sessionId}")
    public ResponseEntity<?> getSession(
            Authentication authentication,
            @PathVariable String sessionId
    ) {
        try {
            String userId = authentication.getName();
            ChatSessionDTO session = chatService.getSessionWithMessages(sessionId, userId);
            return ResponseEntity.ok(session);
        } catch (Exception e) {
            return ResponseEntity.badRequest().body(Map.of("error", e.getMessage()));
        }
    }
    
    /**
     * Create new chat session in database
     */
    @PostMapping("/sessions")
    public ResponseEntity<?> createSession(
            Authentication authentication,
            @RequestBody Map<String, String> body
    ) {
        try {
            String userId = authentication.getName();
            String title = body.getOrDefault("title", "New Chat");
            String contentType = body.getOrDefault("contentType", "general");
            
            ChatSession session = chatService.createSession(userId, title, contentType);
            return ResponseEntity.ok(session);
        } catch (Exception e) {
            return ResponseEntity.badRequest().body(Map.of("error", e.getMessage()));
        }
    }
    
    /**
     * Delete chat session from database
     */
    @DeleteMapping("/sessions/{sessionId}")
    public ResponseEntity<?> deleteSession(
            Authentication authentication,
            @PathVariable String sessionId
    ) {
        try {
            String userId = authentication.getName();
            chatService.deleteSession(sessionId, userId);
            return ResponseEntity.ok(Map.of("message", "Session deleted successfully"));
        } catch (Exception e) {
            return ResponseEntity.badRequest().body(Map.of("error", e.getMessage()));
        }
    }
    
    /**
     * Delete all sessions for user from database
     */
    @DeleteMapping("/sessions")
    public ResponseEntity<?> deleteAllSessions(Authentication authentication) {
        try {
            String userId = authentication.getName();
            chatService.deleteAllUserSessions(userId);
            return ResponseEntity.ok(Map.of("message", "All sessions deleted successfully"));
        } catch (Exception e) {
            return ResponseEntity.badRequest().body(Map.of("error", e.getMessage()));
        }
    }
}
