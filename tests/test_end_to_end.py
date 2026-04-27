#!/usr/bin/env python3
"""
End-to-End API Testing Script
Tests the complete flow: Frontend -> Backend -> AI Service
"""

import requests
import json
import time
import sys

def test_ai_service():
    """Test AI Service directly"""
    print("🔍 Testing AI Service (Python FastAPI)...")
    
    try:
        # Test health endpoint
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code == 200:
            print("✅ AI Service health check: OK")
        else:
            print(f"❌ AI Service health check failed: {response.status_code}")
            return False
            
        # Test chat endpoint
        payload = {
            "prompt": "write email to hr Anjali Nair that tomorrow at 1-2pm i wont be available because of pbl review in my class",
            "content_type": "email"
        }
        
        response = requests.post("http://localhost:8000/chat/", 
                               json=payload, 
                               timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ AI Service chat endpoint: OK")
            print(f"   Generated content length: {len(result.get('content', ''))}")
            return True
        else:
            print(f"❌ AI Service chat failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ AI Service error: {str(e)}")
        return False

def test_backend_auth():
    """Test Backend Authentication"""
    print("\n🔍 Testing Backend Authentication...")
    
    try:
        # Test registration (might fail if user exists)
        register_payload = {
            "email": "test@example.com",
            "username": "testuser",
            "password": "password123",
            "fullName": "Test User"
        }
        
        response = requests.post("http://localhost:8080/api/auth/register", 
                               json=register_payload, 
                               timeout=10)
        
        if response.status_code == 200:
            print("✅ Backend registration: OK")
        else:
            print(f"⚠️  Backend registration: {response.status_code} (user might already exist)")
        
        # Test login
        login_payload = {
            "email": "test@example.com",
            "password": "password123"
        }
        
        response = requests.post("http://localhost:8080/api/auth/login", 
                               json=login_payload, 
                               timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Backend login: OK")
            access_token = result.get('accessToken')
            if access_token:
                print("✅ Access token received")
                return access_token
            else:
                print("❌ No access token in response")
                return None
        else:
            print(f"❌ Backend login failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Backend auth error: {str(e)}")
        return None

def test_backend_chat(access_token):
    """Test Backend Chat with AI Service"""
    print("\n🔍 Testing Backend Chat Integration...")
    
    try:
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "prompt": "write email to hr Anjali Nair that tomorrow at 1-2pm i wont be available because of pbl review in my class",
            "contentType": "email"
        }
        
        response = requests.post("http://localhost:8080/api/chat/message", 
                               json=payload, 
                               headers=headers,
                               timeout=60)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Backend chat endpoint: OK")
            print(f"   Session ID: {result.get('sessionId')}")
            print(f"   Content length: {len(result.get('content', ''))}")
            print(f"   Model used: {result.get('modelUsed')}")
            return True
        else:
            print(f"❌ Backend chat failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Backend chat error: {str(e)}")
        return False

def test_frontend_connectivity():
    """Test Frontend Server"""
    print("\n🔍 Testing Frontend Server...")
    
    try:
        response = requests.get("http://localhost:5173", timeout=5)
        if response.status_code == 200:
            print("✅ Frontend server: OK")
            return True
        else:
            print(f"❌ Frontend server failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Frontend server error: {str(e)}")
        return False

def main():
    print("🚀 Starting End-to-End API Testing...\n")
    
    # Test each layer
    ai_ok = test_ai_service()
    frontend_ok = test_frontend_connectivity()
    
    if not ai_ok:
        print("\n❌ AI Service is not working. Check if Python service is running on port 8000.")
        sys.exit(1)
    
    access_token = test_backend_auth()
    if not access_token:
        print("\n❌ Backend authentication failed. Check if Java backend is running on port 8080.")
        sys.exit(1)
    
    chat_ok = test_backend_chat(access_token)
    if not chat_ok:
        print("\n❌ Backend-AI integration failed. Check logs for connection issues.")
        sys.exit(1)
    
    if not frontend_ok:
        print("\n⚠️  Frontend server is not responding. Check if Vite dev server is running on port 5173.")
    
    print("\n🎉 End-to-End Testing Complete!")
    print("✅ AI Service: Working")
    print("✅ Backend Auth: Working") 
    print("✅ Backend-AI Integration: Working")
    print(f"{'✅' if frontend_ok else '⚠️ '} Frontend Server: {'Working' if frontend_ok else 'Not responding'}")
    
    if ai_ok and access_token and chat_ok:
        print("\n🔥 All core APIs are working! The issue might be in the frontend JavaScript.")
        print("   Check browser console for errors and network requests.")

if __name__ == "__main__":
    main()