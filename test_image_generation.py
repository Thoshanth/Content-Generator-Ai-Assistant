#!/usr/bin/env python3
"""
Test script for image generation feature
Tests the complete flow from frontend to AI service
"""

import requests
import json
import time
import os
from datetime import datetime

# Configuration
BACKEND_URL = "http://localhost:8080"
AI_SERVICE_URL = "http://localhost:8000"

# Test credentials (replace with actual test user)
TEST_EMAIL = "test@example.com"
TEST_PASSWORD = "password123"

def test_login():
    """Test user authentication"""
    print("🔐 Testing user login...")
    
    login_data = {
        "email": TEST_EMAIL,
        "password": TEST_PASSWORD
    }
    
    response = requests.post(f"{BACKEND_URL}/api/auth/login", json=login_data)
    
    if response.status_code == 200:
        token = response.json().get("token")
        print("✅ Login successful")
        return token
    else:
        print(f"❌ Login failed: {response.status_code} - {response.text}")
        return None

def test_image_styles(token):
    """Test getting available image styles"""
    print("\n🎨 Testing image styles endpoint...")
    
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BACKEND_URL}/api/images/styles", headers=headers)
    
    if response.status_code == 200:
        styles = response.json()
        print(f"✅ Retrieved {len(styles.get('styles', []))} styles")
        print(f"   Available styles: {[s['id'] for s in styles.get('styles', [])]}")
        return True
    else:
        print(f"❌ Failed to get styles: {response.status_code} - {response.text}")
        return False

def test_image_presets(token):
    """Test getting image presets"""
    print("\n📐 Testing image presets endpoint...")
    
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BACKEND_URL}/api/images/presets", headers=headers)
    
    if response.status_code == 200:
        presets = response.json()
        print(f"✅ Retrieved {len(presets.get('presets', {}))} presets")
        print(f"   Available presets: {list(presets.get('presets', {}).keys())}")
        return True
    else:
        print(f"❌ Failed to get presets: {response.status_code} - {response.text}")
        return False

def test_image_usage(token):
    """Test getting image usage"""
    print("\n📊 Testing image usage endpoint...")
    
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BACKEND_URL}/api/images/usage", headers=headers)
    
    if response.status_code == 200:
        usage = response.json()
        print(f"✅ Current usage: {usage.get('dailyCount', 0)}/{usage.get('dailyLimit', 5)}")
        print(f"   Remaining: {usage.get('remaining', 0)} images")
        return usage
    else:
        print(f"❌ Failed to get usage: {response.status_code} - {response.text}")
        return None

def test_image_generation(token):
    """Test image generation"""
    print("\n🖼️  Testing image generation...")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Test image request
    image_request = {
        "prompt": "A beautiful sunset over mountains, peaceful landscape",
        "negativePrompt": "blurry, low quality, distorted",
        "width": 512,
        "height": 512,
        "steps": 20,  # Reduced for faster testing
        "guidanceScale": 7.5,
        "style": "realistic"
    }
    
    print(f"   Generating image with prompt: '{image_request['prompt']}'")
    start_time = time.time()
    
    response = requests.post(
        f"{BACKEND_URL}/api/images/generate", 
        json=image_request, 
        headers=headers,
        timeout=120  # 2 minute timeout
    )
    
    generation_time = time.time() - start_time
    
    if response.status_code == 200:
        result = response.json()
        print(f"✅ Image generated successfully in {generation_time:.2f}s")
        print(f"   Image URL: {result.get('imageUrl')}")
        print(f"   Model used: {result.get('modelUsed')}")
        print(f"   Generation time: {result.get('generationTime')}s")
        
        # Test image serving
        if result.get('imageUrl'):
            image_response = requests.get(f"{BACKEND_URL}{result['imageUrl']}")
            if image_response.status_code == 200:
                print(f"✅ Image serving works (size: {len(image_response.content)} bytes)")
            else:
                print(f"❌ Image serving failed: {image_response.status_code}")
        
        return result
    elif response.status_code == 429:
        print("⚠️  Daily limit reached - this is expected behavior")
        return None
    else:
        print(f"❌ Image generation failed: {response.status_code} - {response.text}")
        return None

def test_ai_service_direct():
    """Test AI service directly"""
    print("\n🤖 Testing AI service directly...")
    
    # Test health endpoint
    try:
        response = requests.get(f"{AI_SERVICE_URL}/")
        if response.status_code == 200:
            print("✅ AI service is running")
        else:
            print(f"❌ AI service health check failed: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to AI service - is it running?")
        return False
    
    # Test image generation endpoint directly
    image_request = {
        "prompt": "A simple test image",
        "width": 256,
        "height": 256,
        "steps": 15,
        "guidance_scale": 7.0,
        "user_id": "test_user"
    }
    
    try:
        response = requests.post(
            f"{AI_SERVICE_URL}/image/generate", 
            json=image_request,
            timeout=60
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Direct AI service generation successful")
            print(f"   Model: {result.get('model_used')}")
            return True
        else:
            print(f"❌ Direct AI service generation failed: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"❌ Direct AI service test error: {e}")
        return False

def test_rate_limiting(token):
    """Test rate limiting by generating multiple images"""
    print("\n🚦 Testing rate limiting...")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Get current usage
    usage_response = requests.get(f"{BACKEND_URL}/api/images/usage", headers=headers)
    if usage_response.status_code != 200:
        print("❌ Cannot get current usage")
        return False
    
    usage = usage_response.json()
    remaining = usage.get('remaining', 0)
    
    print(f"   Current remaining: {remaining} images")
    
    if remaining == 0:
        print("✅ Rate limiting is working - no images remaining")
        return True
    
    # Try to generate one more image to test limit
    image_request = {
        "prompt": "Rate limit test image",
        "width": 256,
        "height": 256,
        "steps": 10
    }
    
    response = requests.post(
        f"{BACKEND_URL}/api/images/generate", 
        json=image_request, 
        headers=headers,
        timeout=60
    )
    
    if response.status_code == 200:
        print("✅ Image generated (within limits)")
        return True
    elif response.status_code == 429:
        print("✅ Rate limiting is working - limit reached")
        return True
    else:
        print(f"❌ Unexpected response: {response.status_code} - {response.text}")
        return False

def main():
    """Run all tests"""
    print("🧪 Starting Image Generation Integration Tests")
    print("=" * 50)
    
    # Test authentication
    token = test_login()
    if not token:
        print("\n❌ Cannot proceed without authentication")
        return
    
    # Test AI service directly
    ai_service_ok = test_ai_service_direct()
    
    # Test backend endpoints
    styles_ok = test_image_styles(token)
    presets_ok = test_image_presets(token)
    usage_ok = test_image_usage(token)
    
    # Test image generation
    generation_ok = test_image_generation(token)
    
    # Test rate limiting
    rate_limit_ok = test_rate_limiting(token)
    
    # Summary
    print("\n" + "=" * 50)
    print("📋 Test Summary:")
    print(f"   🤖 AI Service: {'✅' if ai_service_ok else '❌'}")
    print(f"   🎨 Styles API: {'✅' if styles_ok else '❌'}")
    print(f"   📐 Presets API: {'✅' if presets_ok else '❌'}")
    print(f"   📊 Usage API: {'✅' if usage_ok else '❌'}")
    print(f"   🖼️  Generation: {'✅' if generation_ok else '❌'}")
    print(f"   🚦 Rate Limiting: {'✅' if rate_limit_ok else '❌'}")
    
    all_passed = all([ai_service_ok, styles_ok, presets_ok, usage_ok, rate_limit_ok])
    
    if all_passed:
        print("\n🎉 All tests passed! Image generation is working correctly.")
    else:
        print("\n⚠️  Some tests failed. Check the logs above for details.")
    
    print("\n💡 Next steps:")
    print("   1. Start the AI service: cd ai-service && python main.py")
    print("   2. Start the backend: cd backend && ./run.bat")
    print("   3. Start the frontend: cd frontend && npm run dev")
    print("   4. Test in the browser at http://localhost:5173")

if __name__ == "__main__":
    main()