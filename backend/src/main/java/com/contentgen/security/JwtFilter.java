package com.contentgen.security;

import jakarta.servlet.FilterChain;
import jakarta.servlet.ServletException;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import lombok.RequiredArgsConstructor;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.security.web.authentication.WebAuthenticationDetailsSource;
import org.springframework.stereotype.Component;
import org.springframework.web.filter.OncePerRequestFilter;

import java.io.IOException;
import java.util.ArrayList;

@Component
@RequiredArgsConstructor
public class JwtFilter extends OncePerRequestFilter {
    
    private final JwtUtil jwtUtil;
    
    @Override
    protected void doFilterInternal(
            HttpServletRequest request,
            HttpServletResponse response,
            FilterChain filterChain
    ) throws ServletException, IOException {
        
        String authHeader = request.getHeader("Authorization");
        String requestURI = request.getRequestURI();
        String method = request.getMethod();
        
        // Debug logging for image endpoints
        if (requestURI.startsWith("/api/images")) {
            System.out.println("=== JWT Filter Debug for Image Request ===");
            System.out.println("Request Method: " + method);
            System.out.println("Request URI: " + requestURI);
            System.out.println("Authorization header: " + authHeader);
            System.out.println("Authorization header is null: " + (authHeader == null));
            if (authHeader != null) {
                System.out.println("Authorization header starts with 'Bearer ': " + authHeader.startsWith("Bearer "));
                System.out.println("Authorization header length: " + authHeader.length());
            }
        }
        
        // Handle OPTIONS requests (CORS preflight)
        if ("OPTIONS".equalsIgnoreCase(method)) {
            filterChain.doFilter(request, response);
            return;
        }
        
        String token = null;
        String userId = null;
        
        // Extract token from Authorization header
        if (authHeader != null && authHeader.startsWith("Bearer ")) {
            token = authHeader.substring(7);
            try {
                userId = jwtUtil.extractUserId(token);
                if (requestURI.startsWith("/api/images")) {
                    System.out.println("Extracted user ID: " + userId);
                }
            } catch (Exception e) {
                if (requestURI.startsWith("/api/images")) {
                    System.out.println("Error extracting user ID: " + e.getMessage());
                    e.printStackTrace();
                }
                logger.error("Error extracting user ID from token", e);
                // Don't return here, continue processing
            }
        } else if (requestURI.startsWith("/api/images")) {
            System.out.println("Authorization header missing or doesn't start with 'Bearer '");
        }
        
        // Validate token and set authentication
        if (userId != null && SecurityContextHolder.getContext().getAuthentication() == null) {
            // Specifically validate access token (not refresh token)
            if (jwtUtil.validateAccessToken(token)) {
                UsernamePasswordAuthenticationToken authToken = 
                        new UsernamePasswordAuthenticationToken(userId, null, new ArrayList<>());
                authToken.setDetails(new WebAuthenticationDetailsSource().buildDetails(request));
                SecurityContextHolder.getContext().setAuthentication(authToken);
                
                if (requestURI.startsWith("/api/images")) {
                    System.out.println("✅ Authentication set successfully for user: " + userId);
                }
            } else {
                if (requestURI.startsWith("/api/images")) {
                    System.out.println("❌ Token validation failed");
                }
                // Token is invalid or expired, clear any existing authentication
                SecurityContextHolder.clearContext();
                response.setStatus(HttpServletResponse.SC_UNAUTHORIZED);
                response.getWriter().write("{\"error\":\"Token expired or invalid\",\"code\":\"TOKEN_EXPIRED\"}");
                response.setContentType("application/json");
                return;
            }
        } else if (requestURI.startsWith("/api/images")) {
            System.out.println("❌ No user ID extracted or authentication already exists");
            System.out.println("   userId: " + userId);
            System.out.println("   Current authentication: " + SecurityContextHolder.getContext().getAuthentication());
        }
        
        filterChain.doFilter(request, response);
    }
}
