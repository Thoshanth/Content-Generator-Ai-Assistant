package com.contentgen.repositories;

import com.contentgen.models.ChatSession;
import com.google.api.core.ApiFuture;
import com.google.cloud.Timestamp;
import com.google.cloud.firestore.*;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Repository;

import java.util.*;
import java.util.concurrent.ExecutionException;
import java.util.stream.Collectors;

@Repository
public class ChatSessionRepository {
    
    private static final String COLLECTION_NAME = "chat_sessions";
    
    @Autowired
    private Firestore firestore;
    
    public ChatSession save(ChatSession session) throws ExecutionException, InterruptedException {
        if (session.getId() == null || session.getId().isEmpty()) {
            session.setId(UUID.randomUUID().toString());
            session.setCreatedAt(Timestamp.now());
        }
        session.setUpdatedAt(Timestamp.now());
        
        ApiFuture<WriteResult> future = firestore.collection(COLLECTION_NAME)
                .document(session.getId())
                .set(session);
        future.get();
        return session;
    }
    
    public Optional<ChatSession> findById(String id) throws ExecutionException, InterruptedException {
        DocumentSnapshot document = firestore.collection(COLLECTION_NAME)
                .document(id)
                .get()
                .get();
        
        if (document.exists()) {
            return Optional.of(document.toObject(ChatSession.class));
        }
        return Optional.empty();
    }
    
    public List<ChatSession> findByUserIdOrderByUpdatedAtDesc(String userId) throws ExecutionException, InterruptedException {
        QuerySnapshot querySnapshot = firestore.collection(COLLECTION_NAME)
                .whereEqualTo("userId", userId)
                .orderBy("updatedAt", Query.Direction.DESCENDING)
                .get()
                .get();
        
        return querySnapshot.getDocuments().stream()
                .map(doc -> doc.toObject(ChatSession.class))
                .collect(Collectors.toList());
    }
    
    public long countByUserId(String userId) throws ExecutionException, InterruptedException {
        QuerySnapshot querySnapshot = firestore.collection(COLLECTION_NAME)
                .whereEqualTo("userId", userId)
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
    
    public List<ChatSession> findAll() throws ExecutionException, InterruptedException {
        QuerySnapshot querySnapshot = firestore.collection(COLLECTION_NAME)
                .get()
                .get();
        
        return querySnapshot.getDocuments().stream()
                .map(doc -> doc.toObject(ChatSession.class))
                .collect(Collectors.toList());
    }
}
