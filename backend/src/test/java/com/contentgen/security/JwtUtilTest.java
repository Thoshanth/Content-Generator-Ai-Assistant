package com.contentgen.security;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.test.util.ReflectionTestUtils;

import static org.junit.jupiter.api.Assertions.*;

class JwtUtilTest {
    
    private JwtUtil jwtUtil;
    
    @BeforeEach
    void setUp() {
        jwtUtil = new JwtUtil();
        ReflectionTestUtils.setField(jwtUtil, "secret", "test-secret-key-that-is-at-least-256-bits-long-for-security");
        ReflectionTestUtils.setField(jwtUtil, "expiration", 900000L); // 15 minutes
        ReflectionTestUtils.setField(jwtUtil, "refreshExpiration", 604800000L); // 7 days
    }
    
    @Test
    void testGenerateAndValidateAccessToken() {
        String userId = "test-user-id";
        String email = "test@example.com";
        
        String token = jwtUtil.generateToken(userId, email);
        
        assertNotNull(token);
        assertTrue(jwtUtil.validateAccessToken(token));
        assertEquals(userId, jwtUtil.extractUserId(token));
        assertEquals(email, jwtUtil.extractEmail(token));
        assertEquals("access", jwtUtil.extractTokenType(token));
    }
    
    @Test
    void testGenerateAndValidateRefreshToken() {
        String userId = "test-user-id";
        String email = "test@example.com";
        
        String refreshToken = jwtUtil.generateRefreshToken(userId, email);
        
        assertNotNull(refreshToken);
        assertTrue(jwtUtil.validateRefreshToken(refreshToken));
        assertEquals(userId, jwtUtil.extractUserId(refreshToken));
        assertEquals(email, jwtUtil.extractEmail(refreshToken));
        assertEquals("refresh", jwtUtil.extractTokenType(refreshToken));
    }
    
    @Test
    void testAccessTokenShouldNotValidateAsRefreshToken() {
        String userId = "test-user-id";
        String email = "test@example.com";
        
        String accessToken = jwtUtil.generateToken(userId, email);
        
        assertTrue(jwtUtil.validateAccessToken(accessToken));
        assertFalse(jwtUtil.validateRefreshToken(accessToken));
    }
    
    @Test
    void testRefreshTokenShouldNotValidateAsAccessToken() {
        String userId = "test-user-id";
        String email = "test@example.com";
        
        String refreshToken = jwtUtil.generateRefreshToken(userId, email);
        
        assertTrue(jwtUtil.validateRefreshToken(refreshToken));
        assertFalse(jwtUtil.validateAccessToken(refreshToken));
    }
}