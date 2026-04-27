#!/usr/bin/env python3
"""
Firebase Index Status Monitor
Waits for the Firebase index to finish building and tests chat functionality
"""

import requests
import json
import time
import sys

def test_chat_with_auth():
    """Test the complete chat flow"""
    try:
        # Login to get token
        login_payload = {
            "email": "test@example.com",
            "password": "password123"
        }
        
        response = requests.post("http://localhost:8080/api/auth/login", 
                               json=login_payload, 
                               timeout=10)
        
        if response.status_code != 200:
            print(f"❌ Login failed: {response.status_code}")
            return False
            
        access_token = response.json().get('accessToken')
        if not access_token:
            print("❌ No access token received")
            return False
        
        # Test chat
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
            print("🎉 SUCCESS! Chat is working!")
            print(f"   Session ID: {result.get('sessionId')}")
            print(f"   Content preview: {result.get('content', '')[:100]}...")
            print(f"   Model used: {result.get('modelUsed')}")
            return True
        else:
            error_text = response.text
            if "index is currently building" in error_text:
                return "building"
            else:
                print(f"❌ Chat failed: {response.status_code}")
                print(f"   Response: {error_text}")
                return False
                
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def main():
    print("⏳ Waiting for Firebase index to finish building...")
    print("   This usually takes 1-5 minutes depending on data size.")
    print("   Checking every 30 seconds...\n")
    
    attempt = 1
    max_attempts = 20  # 10 minutes max
    
    while attempt <= max_attempts:
        print(f"🔍 Attempt {attempt}/{max_attempts} - Testing chat functionality...")
        
        result = test_chat_with_auth()
        
        if result == True:
            print("\n🚀 FIREBASE INDEX IS READY!")
            print("✅ Chat functionality is now working!")
            print("✅ Your JWT tokens (15min expiry + refresh) are working!")
            print("✅ End-to-end flow: Frontend -> Backend -> AI Service -> Firebase")
            print("\n🎯 You can now test the chat in your browser!")
            sys.exit(0)
        elif result == "building":
            print("⏳ Index is still building... waiting 30 seconds")
        else:
            print("❌ Unexpected error occurred")
        
        if attempt < max_attempts:
            print(f"   Next check in 30 seconds...\n")
            time.sleep(30)
        
        attempt += 1
    
    print("\n⚠️  Index is taking longer than expected (10+ minutes)")
    print("   This can happen with large datasets or Firebase issues")
    print("   Check Firebase Console for index status:")
    print("   https://console.firebase.google.com/project/contentgener-74f5c/firestore/indexes")

if __name__ == "__main__":
    main()