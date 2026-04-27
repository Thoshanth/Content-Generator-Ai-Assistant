package com.contentgen.repositories;

import com.contentgen.models.ChatMessage;
import com.google.api.core.ApiFuture;
import com.google.cloud.Timestamp;
import com.google.cloud.firestore.*;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Repository;

import java.util.*;
import java.util.concurrent.ExecutionException;
import java.util.stream.Collectors;

@Repository
public class ChatMessageRepository {
    
    private static final String COLLECTION_NAME = "chat_messages";
    
    @Autowired
    private Firestore firestore;
    
    public ChatMessage save(ChatMessage message) throws ExecutionException, InterruptedException {
        if (message.getId() == null || message.getId().isEmpty()) {
            message.setId(UUID.randomUUID().toString());
            message.setCreatedAt(Timestamp.now());
        }
        
        ApiFuture<WriteResult> future = firestore.collection(COLLECTION_NAME)
                .document(message.getId())
                .set(message);
        future.get();
        return message;
    }
    
    public Optional<ChatMessage> findById(String id) throws ExecutionException, InterruptedException {
        DocumentSnapshot document = firestore.collection(COLLECTION_NAME)
                .document(id)
                .get()
                .get();
        
        if (document.exists()) {
            return Optional.of(document.toObject(ChatMessage.class));
        }
        return Optional.empty();
    }
    
    public List<ChatMessage> findBySessionIdOrderByCreatedAtAsc(String sessionId) throws ExecutionException, InterruptedException {
        QuerySnapshot querySnapshot = firestore.collection(COLLECTION_NAME)
                .whereEqualTo("sessionId", sessionId)
                .orderBy("createdAt", Query.Direction.ASCENDING)
                .get()
                .get();
        
        return querySnapshot.getDocuments().stream()
                .map(doc -> doc.toObject(ChatMessage.class))
                .collect(Collectors.toList());
    }
    
    public List<ChatMessage> findLastNMessagesBySessionId(String sessionId) throws ExecutionException, InterruptedException {
        QuerySnapshot querySnapshot = firestore.collection(COLLECTION_NAME)
                .whereEqualTo("sessionId", sessionId)
                .orderBy("createdAt", Query.Direction.DESCENDING)
                .get()
                .get();
        
        return querySnapshot.getDocuments().stream()
                .map(doc -> doc.toObject(ChatMessage.class))
                .collect(Collectors.toList());
    }
    
    public long countByUserId(String userId) throws ExecutionException, InterruptedException {
        QuerySnapshot querySnapshot = firestore.collection(COLLECTION_NAME)
                .whereEqualTo("userId", userId)
                .get()
                .get();
        
        return querySnapshot.size();
    }
    
    public long countByUserIdAndRole(String userId, String role) throws ExecutionException, InterruptedException {
        QuerySnapshot querySnapshot = firestore.collection(COLLECTION_NAME)
                .whereEqualTo("userId", userId)
                .whereEqualTo("role", role)
                .get()
                .get();
        
        return querySnapshot.size();
    }
    
    public void deleteById(String id) throws ExecutionException, InterruptedException {
        firestore.collection(COLLECTION_NAME)
                .document(id)
                .delete()
                .get();
    }
    
    public List<ChatMessage> findAll() throws ExecutionException, InterruptedException {
        QuerySnapshot querySnapshot = firestore.collection(COLLECTION_NAME)
                .get()
                .get();
        
        return querySnapshot.getDocuments().stream()
                .map(doc -> doc.toObject(ChatMessage.class))
                .collect(Collectors.toList());
    }
}
