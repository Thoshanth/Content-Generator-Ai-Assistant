package com.contentgen.repositories;

import com.contentgen.models.User;
import com.google.api.core.ApiFuture;
import com.google.cloud.Timestamp;
import com.google.cloud.firestore.*;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Repository;

import java.util.*;
import java.util.concurrent.ExecutionException;

@Repository
public class UserRepository {
    
    private static final String COLLECTION_NAME = "users";
    
    @Autowired
    private Firestore firestore;
    
    public User save(User user) throws ExecutionException, InterruptedException {
        if (user.getId() == null || user.getId().isEmpty()) {
            user.setId(UUID.randomUUID().toString());
            user.setCreatedAt(Timestamp.now());
        }
        user.setUpdatedAt(Timestamp.now());
        
        ApiFuture<WriteResult> future = firestore.collection(COLLECTION_NAME)
                .document(user.getId())
                .set(user);
        future.get();
        return user;
    }
    
    public Optional<User> findById(String id) throws ExecutionException, InterruptedException {
        DocumentSnapshot document = firestore.collection(COLLECTION_NAME)
                .document(id)
                .get()
                .get();
        
        if (document.exists()) {
            return Optional.of(document.toObject(User.class));
        }
        return Optional.empty();
    }
    
    public Optional<User> findByEmail(String email) throws ExecutionException, InterruptedException {
        QuerySnapshot querySnapshot = firestore.collection(COLLECTION_NAME)
                .whereEqualTo("email", email)
                .limit(1)
                .get()
                .get();
        
        if (!querySnapshot.isEmpty()) {
            return Optional.of(querySnapshot.getDocuments().get(0).toObject(User.class));
        }
        return Optional.empty();
    }
    
    public Optional<User> findByUsername(String username) throws ExecutionException, InterruptedException {
        QuerySnapshot querySnapshot = firestore.collection(COLLECTION_NAME)
                .whereEqualTo("username", username)
                .limit(1)
                .get()
                .get();
        
        if (!querySnapshot.isEmpty()) {
            return Optional.of(querySnapshot.getDocuments().get(0).toObject(User.class));
        }
        return Optional.empty();
    }
    
    public boolean existsByEmail(String email) throws ExecutionException, InterruptedException {
        QuerySnapshot querySnapshot = firestore.collection(COLLECTION_NAME)
                .whereEqualTo("email", email)
                .limit(1)
                .get()
                .get();
        
        return !querySnapshot.isEmpty();
    }
    
    public boolean existsByUsername(String username) throws ExecutionException, InterruptedException {
        QuerySnapshot querySnapshot = firestore.collection(COLLECTION_NAME)
                .whereEqualTo("username", username)
                .limit(1)
                .get()
                .get();
        
        return !querySnapshot.isEmpty();
    }
    
    public void deleteById(String id) throws ExecutionException, InterruptedException {
        firestore.collection(COLLECTION_NAME)
                .document(id)
                .delete()
                .get();
    }
    
    public List<User> findAll() throws ExecutionException, InterruptedException {
        QuerySnapshot querySnapshot = firestore.collection(COLLECTION_NAME)
                .get()
                .get();
        
        List<User> users = new ArrayList<>();
        for (DocumentSnapshot document : querySnapshot.getDocuments()) {
            users.add(document.toObject(User.class));
        }
        return users;
    }
}
