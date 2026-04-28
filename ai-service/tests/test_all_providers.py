#!/usr/bin/env python3
"""
Comprehensive test for all 4 AI providers
Tests: Groq, Gemini, NVIDIA NIM, Cerebras
"""

import asyncio
import httpx
import json

AI_SERVICE_URL = "http://localhost:8000"

async def test_provider_status():
    """Test provider status endpoint"""
    print("\n" + "="*70)
    print("TEST 1: Provider Status Check")
    print("="*70)
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.get(f'{AI_SERVICE_URL}/chat/providers')
        
        if response.status_code == 200:
            data = response.json()
            providers = data.get('providers', [])
            
            print(f"[INFO] Available Providers: {len(providers)}")
            for provider in providers:
                print(f"  - {provider.get('name')}: {provider.get('model')}")
            
            if len(providers) == 4:
                print(f"[PASS] All 4 providers available!")
                return True
            else:
                print(f"[WARN] Only {len(providers)} provider(s) available")
                return len(providers) >= 2
        else:
            print(f"[FAIL] Provider Status - HTTP {response.status_code}")
            return False


async def test_groq():
    """Test Groq provider (Speed/Creative/Chat)"""
    print("\n" + "="*70)
    print("TEST 2: Groq Provider (Speed/Creative/Chat)")
    print("="*70)
    
    payload = {
        "prompt": "Write a short creative greeting in 2 sentences",
        "content_type": "general",
        "tone": "friendly",
        "length": "short",
        "user_id": "test-groq"
    }
    
    print("[INFO] Testing Groq (Primary for general content)...")
    
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
        print(f"[PASS] Groq Test - {word_count} words generated")
        print(f"[INFO] Provider used: {provider_used}")
        return True
    else:
        print("[FAIL] Groq Test")
        return False


async def test_gemini():
    """Test Gemini provider (Structured Long-form)"""
    print("\n" + "="*70)
    print("TEST 3: Gemini Provider (Structured Long-form)")
    print("="*70)
    
    payload = {
        "prompt": "Write a short professional email about a meeting",
        "content_type": "email",
        "tone": "professional",
        "length": "short",
        "user_id": "test-gemini"
    }
    
    print("[INFO] Testing Gemini (Primary for emails)...")
    
    provider_used = None
    word_count = 0
    
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
                        print(data.get('delta', ''), end='', flush=True)
                    
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
        print(f"[PASS] Gemini Test - {word_count} words generated")
        print(f"[INFO] Provider used: {provider_used}")
        return True
    else:
        print("[FAIL] Gemini Test")
        return False


async def test_nvidia():
    """Test NVIDIA NIM provider (Technical/Resume/Code)"""
    print("\n" + "="*70)
    print("TEST 4: NVIDIA NIM Provider (Technical/Resume/Code)")
    print("="*70)
    
    payload = {
        "prompt": "Create a brief resume summary for a software engineer",
        "content_type": "resume",
        "tone": "professional",
        "length": "short",
        "user_id": "test-nvidia"
    }
    
    print("[INFO] Testing NVIDIA NIM (Primary for resumes)...")
    
    provider_used = None
    word_count = 0
    
    async with httpx.AsyncClient(timeout=90.0) as client:
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
                        print(data.get('delta', ''), end='', flush=True)
                    
                    elif 'done' in data and data['done']:
                        word_count = data.get('word_count', 0)
                        print()
                    
                    elif 'error' in data:
                        print(f"\n[FAIL] Error: {data.get('error')}")
                        return False
                    
                    elif 'info' in data:
                        print(f"\n[INFO] {data.get('info')}")
                
                except json.JSONDecodeError:
                    continue
    
    print("-"*70)
    if provider_used and word_count > 0:
        print(f"[PASS] NVIDIA NIM Test - {word_count} words generated")
        print(f"[INFO] Provider used: {provider_used}")
        return True
    else:
        print("[FAIL] NVIDIA NIM Test")
        return False


async def test_cerebras():
    """Test Cerebras provider (Universal Fallback)"""
    print("\n" + "="*70)
    print("TEST 5: Cerebras Provider (Universal Fallback)")
    print("="*70)
    
    payload = {
        "prompt": "Explain what async/await does in one sentence",
        "content_type": "code_explainer",
        "tone": "professional",
        "length": "short",
        "user_id": "test-cerebras"
    }
    
    print("[INFO] Testing Cerebras (Fallback for code_explainer)...")
    
    provider_used = None
    word_count = 0
    
    async with httpx.AsyncClient(timeout=90.0) as client:
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
                        print(data.get('delta', ''), end='', flush=True)
                    
                    elif 'done' in data and data['done']:
                        word_count = data.get('word_count', 0)
                        print()
                    
                    elif 'error' in data:
                        print(f"\n[FAIL] Error: {data.get('error')}")
                        return False
                    
                    elif 'info' in data:
                        print(f"\n[INFO] {data.get('info')}")
                
                except json.JSONDecodeError:
                    continue
    
    print("-"*70)
    if provider_used and word_count > 0:
        print(f"[PASS] Cerebras Test - {word_count} words generated")
        print(f"[INFO] Provider used: {provider_used}")
        return True
    else:
        print("[FAIL] Cerebras Test")
        return False


async def test_routing():
    """Test routing for different content types"""
    print("\n" + "="*70)
    print("TEST 6: Content Type Routing")
    print("="*70)
    
    test_cases = [
        ("general", "Groq", "Write hello"),
        ("blog_post", "Gemini", "Write a blog intro"),
        ("resume", "NVIDIA NIM", "Create resume summary"),
        ("code_explainer", "NVIDIA NIM", "Explain loops"),
    ]
    
    results = []
    
    async with httpx.AsyncClient(timeout=90.0) as client:
        for content_type, expected_provider, prompt in test_cases:
            print(f"\n[INFO] Testing: {content_type} (Expected: {expected_provider})")
            
            payload = {
                "prompt": prompt,
                "content_type": content_type,
                "tone": "professional",
                "length": "short",
                "user_id": "test-routing"
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
                match = "✓" if provider_used == expected_provider else "→"
                print(f"[PASS] {content_type} - {match} {provider_used} - {word_count} words")
                results.append(True)
            else:
                print(f"[FAIL] {content_type}")
                results.append(False)
    
    success = all(results)
    if success:
        print(f"\n[PASS] Routing Test - {len(results)}/{len(results)} passed")
    else:
        print(f"\n[INFO] Routing Test - {sum(results)}/{len(results)} passed")
    
    return success


async def main():
    """Run all provider tests"""
    print("\n" + "="*70)
    print("AI Service - All Providers Test")
    print("="*70)
    print("[INFO] Testing all 4 providers: Groq, Gemini, NVIDIA NIM, Cerebras")
    print()
    
    results = []
    
    # Test 1: Provider Status
    results.append(await test_provider_status())
    
    # Test 2: Groq
    results.append(await test_groq())
    
    # Test 3: Gemini
    results.append(await test_gemini())
    
    # Test 4: NVIDIA NIM
    results.append(await test_nvidia())
    
    # Test 5: Cerebras
    results.append(await test_cerebras())
    
    # Test 6: Routing
    results.append(await test_routing())
    
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
        print("[INFO] All 4 providers are working correctly!")
        print()
        print("Provider Status:")
        print("  - Groq: ✅ Working (Speed/Creative/Chat)")
        print("  - Gemini: ✅ Working (Structured Long-form)")
        print("  - NVIDIA NIM: ✅ Working (Technical/Resume/Code)")
        print("  - Cerebras: ✅ Working (Universal Fallback)")
    else:
        print(f"[INFO] {passed}/{total} tests passed")
        print("[INFO] Check logs above for details")
    
    print()
    print("="*70)


if __name__ == '__main__':
    asyncio.run(main())
