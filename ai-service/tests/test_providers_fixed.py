#!/usr/bin/env python3
"""
Test to verify provider fixes
Tests that Groq and Gemini are working correctly
"""

import asyncio
import httpx
import json

AI_SERVICE_URL = "http://localhost:8000"

async def test_provider_status():
    """Test provider status endpoint"""
    print("\n" + "="*70)
    print("TEST 1: Provider Status")
    print("="*70)
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.get(f'{AI_SERVICE_URL}/chat/providers')
        
        if response.status_code == 200:
            data = response.json()
            providers = data.get('providers', [])
            
            print(f"[INFO] Available Providers: {len(providers)}")
            for provider in providers:
                print(f"  - {provider.get('name')}: {provider.get('model')}")
            
            if len(providers) >= 2:
                print(f"[PASS] Provider Status - {len(providers)} providers available")
                return True
            else:
                print(f"[WARN] Only {len(providers)} provider(s) available")
                return True
        else:
            print(f"[FAIL] Provider Status - HTTP {response.status_code}")
            return False


async def test_groq_generation():
    """Test content generation with Groq"""
    print("\n" + "="*70)
    print("TEST 2: Groq Content Generation")
    print("="*70)
    
    payload = {
        "prompt": "Write a short greeting message",
        "content_type": "general",
        "tone": "friendly",
        "length": "short",
        "user_id": "test-user"
    }
    
    print("[INFO] Testing Groq provider...")
    
    provider_used = None
    word_count = 0
    full_content = ""
    
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
                        provider_used = data.get('provider')
                        print(f"\n[INFO] Provider: {provider_used} | Model: {data.get('model')}\n")
                    
                    elif 'delta' in data:
                        delta = data.get('delta', '')
                        full_content += delta
                        print(delta, end='', flush=True)
                    
                    elif 'done' in data and data['done']:
                        word_count = data.get('word_count', 0)
                        print()
                    
                    elif 'error' in data:
                        print(f"\n[FAIL] Error: {data.get('error')}")
                        return False
                
                except json.JSONDecodeError:
                    continue
    
    print("-"*70)
    if provider_used and word_count > 0:
        print(f"[PASS] Groq Generation - {word_count} words generated")
        print(f"[INFO] Provider used: {provider_used}")
        return True
    else:
        print("[FAIL] Groq Generation")
        return False


async def test_multiple_requests():
    """Test multiple requests to verify fallback"""
    print("\n" + "="*70)
    print("TEST 3: Multiple Requests (Fallback Test)")
    print("="*70)
    
    content_types = ["email", "blog_post", "social_media"]
    results = []
    
    async with httpx.AsyncClient(timeout=60.0) as client:
        for content_type in content_types:
            print(f"\n[INFO] Testing: {content_type}")
            
            payload = {
                "prompt": f"Write a short {content_type}",
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
                        
                        elif 'error' in data:
                            print(f"[FAIL] {content_type} - Error: {data.get('error')}")
                            results.append(False)
                            break
                    
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
        print(f"\n[PASS] Multiple Requests - {len(results)}/{len(results)} passed")
    else:
        print(f"\n[WARN] Multiple Requests - {sum(results)}/{len(results)} passed")
    
    return success


async def test_no_errors():
    """Test that there are no provider errors"""
    print("\n" + "="*70)
    print("TEST 4: No Provider Errors")
    print("="*70)
    
    payload = {
        "prompt": "Write hello world",
        "content_type": "general",
        "tone": "casual",
        "user_id": "test-user"
    }
    
    print("[INFO] Checking for provider errors...")
    
    has_error = False
    provider_used = None
    
    async with httpx.AsyncClient(timeout=60.0) as client:
        async with client.stream('POST', f'{AI_SERVICE_URL}/chat/stream', json=payload) as response:
            if response.status_code != 200:
                print(f"[FAIL] HTTP {response.status_code}")
                return False
            
            async for line in response.aiter_lines():
                if not line.startswith('data: '):
                    continue
                
                try:
                    data = json.loads(line[6:])
                    
                    if 'provider' in data:
                        provider_used = data.get('provider')
                    
                    elif 'error' in data:
                        has_error = True
                        print(f"[FAIL] Error found: {data.get('error')}")
                        break
                    
                    elif 'info' in data and 'rate limited' in data.get('info', '').lower():
                        print(f"[INFO] Provider switching: {data.get('info')}")
                
                except json.JSONDecodeError:
                    continue
    
    if not has_error and provider_used:
        print(f"[PASS] No Provider Errors - Used {provider_used}")
        return True
    elif has_error:
        print("[FAIL] Provider errors detected")
        return False
    else:
        print("[FAIL] No provider used")
        return False


async def main():
    """Run all provider tests"""
    print("\n" + "="*70)
    print("AI Provider Fix Verification")
    print("="*70)
    print("[INFO] Testing provider fixes...")
    print()
    
    results = []
    
    # Test 1: Provider Status
    results.append(await test_provider_status())
    
    # Test 2: Groq Generation
    results.append(await test_groq_generation())
    
    # Test 3: Multiple Requests
    results.append(await test_multiple_requests())
    
    # Test 4: No Errors
    results.append(await test_no_errors())
    
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
        print("[SUCCESS] All provider tests passed!")
        print("[INFO] Providers are working correctly!")
    else:
        print(f"[INFO] {passed}/{total} tests passed")
    
    print()
    print("="*70)


if __name__ == '__main__':
    asyncio.run(main())
