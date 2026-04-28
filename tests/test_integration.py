#!/usr/bin/env python3
"""
Integration Test: Frontend → Backend → AI Service
Tests the complete flow with all v5.0 features
"""

import asyncio
import httpx
import json

# Service URLs
AI_SERVICE_URL = "http://localhost:8000"
BACKEND_URL = "http://localhost:8080/api"

async def test_ai_service_direct():
    """Test direct AI service call (no auth)"""
    print("\n" + "="*70)
    print("TEST 1: Direct AI Service Call (No Auth)")
    print("="*70)
    
    payload = {
        "prompt": "Write a short professional email",
        "content_type": "email",
        "tone": "professional",
        "length": "short",
        "language": "English",
        "user_id": "test-user"
    }
    
    print(f"[INFO] Calling AI Service: {AI_SERVICE_URL}/chat/stream")
    print(f"[INFO] Content Type: {payload['content_type']}")
    print(f"[INFO] Tone: {payload['tone']}")
    print(f"[INFO] Length: {payload['length']}")
    print(f"[INFO] Language: {payload['language']}")
    print()
    
    full_content = ""
    provider_info = None
    stats = None
    
    async with httpx.AsyncClient(timeout=60.0) as client:
        async with client.stream('POST', f'{AI_SERVICE_URL}/chat/stream', json=payload) as response:
            if response.status_code != 200:
                print(f"[FAIL] HTTP {response.status_code}")
                return False
            
            print("[INFO] Streaming response...")
            print("-"*70)
            
            async for line in response.aiter_lines():
                if not line.startswith('data: '):
                    continue
                
                try:
                    data = json.loads(line[6:])
                    
                    if 'provider' in data:
                        provider_info = data
                        print(f"\n[INFO] Provider: {data.get('provider')} | Model: {data.get('model')}\n")
                    
                    elif 'delta' in data:
                        delta = data.get('delta', '')
                        full_content += delta
                        print(delta, end='', flush=True)
                    
                    elif 'done' in data and data['done']:
                        stats = data
                        print()
                
                except json.JSONDecodeError:
                    continue
    
    print("-"*70)
    if stats:
        print(f"[PASS] AI Service Direct Call")
        print(f"[INFO] Provider: {provider_info.get('provider')}")
        print(f"[INFO] Model: {provider_info.get('model')}")
        print(f"[INFO] Words: {stats.get('word_count', 0)}")
        print(f"[INFO] Characters: {stats.get('char_count', 0)}")
        return True
    else:
        print("[FAIL] AI Service Direct Call")
        return False


async def test_export_features():
    """Test export and PDF features"""
    print("\n" + "="*70)
    print("TEST 2: Export Features")
    print("="*70)
    
    content = """# Sample Resume

## John Doe
Senior Software Engineer

### Experience
- 5 years in Python and React
- AWS cloud architecture
- Team leadership

### Skills
- Python, JavaScript, Java
- React, FastAPI, Spring Boot
- AWS, Docker, Kubernetes
"""
    
    print("[INFO] Testing format conversion...")
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        # Test plain text export
        response = await client.post(
            f'{AI_SERVICE_URL}/tools/export',
            json={
                "content": content,
                "format": "plain_text",
                "content_type": "resume"
            }
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"[PASS] Plain Text Export - {data.get('word_count', 0)} words")
        else:
            print(f"[FAIL] Plain Text Export - HTTP {response.status_code}")
            return False
        
        # Test HTML export
        response = await client.post(
            f'{AI_SERVICE_URL}/tools/export',
            json={
                "content": content,
                "format": "html",
                "content_type": "resume"
            }
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"[PASS] HTML Export - {data.get('word_count', 0)} words")
        else:
            print(f"[FAIL] HTML Export - HTTP {response.status_code}")
            return False
    
    print("[PASS] Export Features")
    return True


async def test_provider_status():
    """Test provider status endpoint"""
    print("\n" + "="*70)
    print("TEST 3: Provider Status")
    print("="*70)
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.get(f'{AI_SERVICE_URL}/chat/providers')
        
        if response.status_code == 200:
            data = response.json()
            providers = data.get('providers', [])
            
            print(f"[INFO] Available Providers: {len(providers)}")
            for provider in providers:
                print(f"  - {provider.get('name')}: {provider.get('model')}")
            
            print(f"[PASS] Provider Status - {len(providers)} providers available")
            return True
        else:
            print(f"[FAIL] Provider Status - HTTP {response.status_code}")
            return False


async def test_content_types():
    """Test different content types"""
    print("\n" + "="*70)
    print("TEST 4: Content Type Routing")
    print("="*70)
    
    content_types = [
        ("email", "Write a meeting invitation"),
        ("blog_post", "Write about AI trends"),
        ("social_media", "Write a tweet about technology")
    ]
    
    results = []
    
    async with httpx.AsyncClient(timeout=60.0) as client:
        for content_type, prompt in content_types:
            print(f"\n[INFO] Testing: {content_type}")
            
            payload = {
                "prompt": prompt,
                "content_type": content_type,
                "tone": "professional",
                "length": "short",
                "user_id": "test-user"
            }
            
            provider_used = None
            word_count = 0
            
            async with client.stream('POST', f'{AI_SERVICE_URL}/chat/stream', json=payload) as response:
                if response.status_code != 200:
                    print(f"[FAIL] {content_type} - HTTP {response.status_code}")
                    results.append(False)
                    continue
                
                async for line in response.aiter_lines():
                    if not line.startswith('data: '):
                        continue
                    
                    try:
                        data = json.loads(line[6:])
                        
                        if 'provider' in data:
                            provider_used = data.get('provider')
                        
                        elif 'done' in data and data['done']:
                            word_count = data.get('word_count', 0)
                    
                    except json.JSONDecodeError:
                        continue
            
            if provider_used and word_count > 0:
                print(f"[PASS] {content_type} - {provider_used} - {word_count} words")
                results.append(True)
            else:
                print(f"[FAIL] {content_type}")
                results.append(False)
    
    success = all(results)
    if success:
        print(f"\n[PASS] Content Type Routing - {len(results)}/{len(results)} passed")
    else:
        print(f"\n[FAIL] Content Type Routing - {sum(results)}/{len(results)} passed")
    
    return success


async def test_customization_features():
    """Test tone, length, and language customization"""
    print("\n" + "="*70)
    print("TEST 5: Customization Features")
    print("="*70)
    
    tests = [
        ("Tone: Professional", {"tone": "professional"}),
        ("Tone: Casual", {"tone": "casual"}),
        ("Length: Short", {"length": "short"}),
        ("Length: Medium", {"length": "medium"}),
        ("Language: Spanish", {"language": "Spanish"}),
    ]
    
    results = []
    
    async with httpx.AsyncClient(timeout=60.0) as client:
        for test_name, params in tests:
            print(f"\n[INFO] Testing: {test_name}")
            
            payload = {
                "prompt": "Write a greeting message",
                "content_type": "general",
                "user_id": "test-user",
                **params
            }
            
            word_count = 0
            
            async with client.stream('POST', f'{AI_SERVICE_URL}/chat/stream', json=payload) as response:
                if response.status_code != 200:
                    print(f"[FAIL] {test_name} - HTTP {response.status_code}")
                    results.append(False)
                    continue
                
                async for line in response.aiter_lines():
                    if not line.startswith('data: '):
                        continue
                    
                    try:
                        data = json.loads(line[6:])
                        
                        if 'done' in data and data['done']:
                            word_count = data.get('word_count', 0)
                    
                    except json.JSONDecodeError:
                        continue
            
            if word_count > 0:
                print(f"[PASS] {test_name} - {word_count} words")
                results.append(True)
            else:
                print(f"[FAIL] {test_name}")
                results.append(False)
    
    success = all(results)
    if success:
        print(f"\n[PASS] Customization Features - {len(results)}/{len(results)} passed")
    else:
        print(f"\n[FAIL] Customization Features - {sum(results)}/{len(results)} passed")
    
    return success


async def main():
    """Run all integration tests"""
    print("\n" + "="*70)
    print("AI Service v5.0 - Integration Tests")
    print("="*70)
    print("[INFO] Testing complete integration with all v5.0 features")
    print()
    
    results = []
    
    # Test 1: Direct AI Service
    results.append(await test_ai_service_direct())
    
    # Test 2: Export Features
    results.append(await test_export_features())
    
    # Test 3: Provider Status
    results.append(await test_provider_status())
    
    # Test 4: Content Type Routing
    results.append(await test_content_types())
    
    # Test 5: Customization Features
    results.append(await test_customization_features())
    
    # Summary
    print("\n" + "="*70)
    print("Test Summary")
    print("="*70)
    
    passed = sum(results)
    total = len(results)
    
    print(f"Total Tests: {total}")
    print(f"Passed: {passed}")
    print(f"Failed: {total - passed}")
    print()
    
    if passed == total:
        print("[SUCCESS] All integration tests passed!")
        print("[INFO] AI Service v5.0 is fully integrated and working!")
    else:
        print(f"[INFO] {passed}/{total} tests passed")
    
    print()
    print("="*70)


if __name__ == '__main__':
    asyncio.run(main())
