package com.contentgen.services;

import com.contentgen.dto.ChatMessageDTO;
import com.contentgen.dto.ChatSessionDTO;
import com.contentgen.models.ChatMessage;
import com.contentgen.models.ChatSession;
import com.contentgen.repositories.ChatMessageRepository;
import com.contentgen.repositories.ChatSessionRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.concurrent.ExecutionException;
import java.util.stream.Collectors;

@Service
@RequiredArgsConstructor
public class ChatService {
    
    private final ChatSessionRepository chatSessionRepository;
    private final ChatMessageRepository chatMessageRepository;
    
    /**
     * Create new chat session in Firebase Firestore
     */
    public ChatSession createSession(String userId, String title, String contentType) {
        try {
            ChatSession session = new ChatSession();
            session.setUserId(userId);
            session.setTitle(title != null ? title : "New Chat");
            session.setContentType(contentType != null ? contentType : "general");
            
            return chatSessionRepository.save(session);
        } catch (ExecutionException | InterruptedException e) {
            throw new RuntimeException("Error creating session: " + e.getMessage(), e);
        }
    }
    
    /**
     * Get all sessions for a user from Firebase Firestore
     */
    public List<ChatSessionDTO> getUserSessions(String userId) {
        try {
            List<ChatSession> sessions = chatSessionRepository.findByUserIdOrderByUpdatedAtDesc(userId);
            
            return sessions.stream()
                    .map(this::convertToSessionDTO)
                    .collect(Collectors.toList());
        } catch (ExecutionException | InterruptedException e) {
            throw new RuntimeException("Error fetching user sessions: " + e.getMessage(), e);
        }
    }
    
    /**
     * Get session by ID from Firebase Firestore
     */
    public ChatSession getSessionById(String sessionId, String userId) {
        try {
            ChatSession session = chatSessionRepository.findById(sessionId)
                    .orElseThrow(() -> new RuntimeException("Session not found"));
            
            // Verify ownership
            if (!session.getUserId().equals(userId)) {
                throw new RuntimeException("Unauthorized access to session");
            }
            
            return session;
        } catch (ExecutionException | InterruptedException e) {
            throw new RuntimeException("Error fetching session: " + e.getMessage(), e);
        }
    }
    
    /**
     * Get session with all messages from Firebase Firestore
     */
    public ChatSessionDTO getSessionWithMessages(String sessionId, String userId) {
        try {
            ChatSession session = getSessionById(sessionId, userId);
            List<ChatMessage> messages = chatMessageRepository.findBySessionIdOrderByCreatedAtAsc(sessionId);
            
            ChatSessionDTO dto = convertToSessionDTO(session);
            dto.setMessages(messages.stream()
                    .map(this::convertToMessageDTO)
                    .collect(Collectors.toList()));
            
            return dto;
        } catch (ExecutionException | InterruptedException e) {
            throw new RuntimeException("Error fetching session with messages: " + e.getMessage(), e);
        }
    }
    
    /**
     * Save user message to Firebase Firestore
     */
    public ChatMessage saveUserMessage(String sessionId, String userId, String content) {
        try {
            ChatMessage message = new ChatMessage();
            message.setSessionId(sessionId);
            message.setUserId(userId);
            message.setRole("user");
            message.setContent(content);
            
            return chatMessageRepository.save(message);
        } catch (ExecutionException | InterruptedException e) {
            throw new RuntimeException("Error saving user message: " + e.getMessage(), e);
        }
    }
    
    /**
     * Save AI assistant message to Firebase Firestore
     */
    public ChatMessage saveAssistantMessage(
            String sessionId, 
            String userId, 
            String content, 
            String modelUsed, 
            Integer tokensUsed
    ) {
        try {
            ChatMessage message = new ChatMessage();
            message.setSessionId(sessionId);
            message.setUserId(userId);
            message.setRole("assistant");
            message.setContent(content);
            message.setModelUsed(modelUsed);
            message.setTokensUsed(tokensUsed);
            
            return chatMessageRepository.save(message);
        } catch (ExecutionException | InterruptedException e) {
            throw new RuntimeException("Error saving assistant message: " + e.getMessage(), e);
        }
    }
    
    /**
     * Get last N messages from session for context (from Firebase Firestore)
     */
    public List<ChatMessage> getLastNMessages(String sessionId, int limit) {
        try {
            List<ChatMessage> allMessages = chatMessageRepository.findBySessionIdOrderByCreatedAtAsc(sessionId);
            
            int size = allMessages.size();
            if (size <= limit) {
                return allMessages;
            }
            
            return allMessages.subList(size - limit, size);
        } catch (ExecutionException | InterruptedException e) {
            throw new RuntimeException("Error fetching messages: " + e.getMessage(), e);
        }
    }
    
    /**
     * Delete session and all its messages from Firebase Firestore
     */
    public void deleteSession(String sessionId, String userId) {
        try {
            ChatSession session = getSessionById(sessionId, userId);
            
            // Delete all messages in the session
            List<ChatMessage> messages = chatMessageRepository.findBySessionIdOrderByCreatedAtAsc(sessionId);
            for (ChatMessage message : messages) {
                chatMessageRepository.deleteById(message.getId());
            }
            
            // Delete the session
            chatSessionRepository.deleteById(session.getId());
        } catch (ExecutionException | InterruptedException e) {
            throw new RuntimeException("Error deleting session: " + e.getMessage(), e);
        }
    }
    
    /**
     * Update session title in Firebase Firestore
     */
    public ChatSession updateSessionTitle(String sessionId, String userId, String newTitle) {
        try {
            ChatSession session = getSessionById(sessionId, userId);
            session.setTitle(newTitle);
            return chatSessionRepository.save(session);
        } catch (ExecutionException | InterruptedException e) {
            throw new RuntimeException("Error updating session title: " + e.getMessage(), e);
        }
    }
    
    /**
     * Delete all sessions for a user from Firebase Firestore
     */
    public void deleteAllUserSessions(String userId) {
        try {
            List<ChatSession> sessions = chatSessionRepository.findByUserIdOrderByUpdatedAtDesc(userId);
            
            for (ChatSession session : sessions) {
                // Delete messages first
                List<ChatMessage> messages = chatMessageRepository.findBySessionIdOrderByCreatedAtAsc(session.getId());
                for (ChatMessage message : messages) {
                    chatMessageRepository.deleteById(message.getId());
                }
                
                // Delete session
                chatSessionRepository.deleteById(session.getId());
            }
        } catch (ExecutionException | InterruptedException e) {
            throw new RuntimeException("Error deleting all user sessions: " + e.getMessage(), e);
        }
    }
    
    // Helper methods to convert entities to DTOs
    
    private ChatSessionDTO convertToSessionDTO(ChatSession session) {
        ChatSessionDTO dto = new ChatSessionDTO();
        dto.setId(session.getId());
        dto.setUserId(session.getUserId());
        dto.setTitle(session.getTitle());
        dto.setContentType(session.getContentType());
        dto.setCreatedAt(session.getCreatedAt());
        dto.setUpdatedAt(session.getUpdatedAt());
        return dto;
    }
    
    private ChatMessageDTO convertToMessageDTO(ChatMessage message) {
        ChatMessageDTO dto = new ChatMessageDTO();
        dto.setId(message.getId());
        dto.setSessionId(message.getSessionId());
        dto.setRole(message.getRole());
        dto.setContent(message.getContent());
        dto.setModelUsed(message.getModelUsed());
        dto.setTokensUsed(message.getTokensUsed());
        dto.setCreatedAt(message.getCreatedAt());
        return dto;
    }
}
