#!/usr/bin/env python3
"""
Test 4 different email queries with streaming to demonstrate multi-provider fallback
Each query will potentially use different providers/models with real-time streaming
"""

import asyncio
import httpx
import json
import time
import sys
import os
from datetime import datetime

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

BASE_URL = "http://localhost:8000"

# 4 different email scenarios with tone variations
EMAIL_QUERIES = [
    {
        "id": 1,
        "prompt": "Write a professional email to schedule a team meeting for next week to discuss Q1 project milestones",
        "description": "Business Meeting Email",
        "tone": "professional",
        "length": "medium"
    },
    {
        "id": 2, 
        "prompt": "Write a follow-up email to a client thanking them for their feedback and addressing their concerns about delivery timeline",
        "description": "Client Follow-up Email",
        "tone": "professional",
        "length": "medium"
    },
    {
        "id": 3,
        "prompt": "Write an email to HR requesting vacation time for a family wedding, including dates and coverage arrangements",
        "description": "HR Vacation Request Email",
        "tone": "formal",
        "length": "short"
    },
    {
        "id": 4,
        "prompt": "Write a welcome email for new team members joining our software development team, including onboarding information",
        "description": "Welcome/Onboarding Email",
        "tone": "friendly",
        "length": "medium"
    }
]

async def send_email_request_streaming(query_data):
    """Send a single email generation request with streaming"""
    payload = {
        "prompt": query_data["prompt"],
        "content_type": "email",
        "tone": query_data.get("tone", "professional"),
        "length": query_data.get("length", "medium"),
        "language": "English",
        "user_id": f"test-user-{query_data['id']}",
        "regenerate": False,
        "conversation_history": []
    }
    
    print(f"\n{'='*60}")
    print(f"EMAIL {query_data['id']}: {query_data['description']}")
    print(f"{'='*60}")
    print(f"[INFO] Prompt: {query_data['prompt']}")
    print(f"[INFO] Tone: {query_data.get('tone', 'professional')} | Length: {query_data.get('length', 'medium')}")
    print(f"[INFO] Time: {datetime.now().strftime('%H:%M:%S')}")
    
    try:
        start_time = time.time()
        full_content = ""
        provider_info = {}
        stats = {}
        
        async with httpx.AsyncClient(timeout=90.0) as client:
            async with client.stream("POST", f"{BASE_URL}/chat/stream", json=payload) as response:
                
                if response.status_code != 200:
                    print(f"[FAIL] FAILED: Status {response.status_code}")
                    return {"success": False, "error": f"Status {response.status_code}"}
                
                print(f"[INFO] Streaming response...")
                print("-" * 40)
                
                async for line in response.aiter_lines():
                    if not line.startswith("data: "):
                        continue
                    
                    try:
                        data = json.loads(line[6:])
                        
                        # Provider metadata (first event)
                        if "provider" in data:
                            provider_info = {
                                "provider": data.get("provider"),
                                "model": data.get("model"),
                                "attempt": data.get("attempt")
                            }
                            print(f"[INFO] Provider: {data.get('provider')} | Model: {data.get('model')} (Attempt {data.get('attempt')})")
                        
                        # Content delta (streaming)
                        elif "delta" in data:
                            delta = data.get("delta", "")
                            full_content += delta
                            print(delta, end="", flush=True)
                        
                        # Completion (final event)
                        elif "done" in data and data["done"]:
                            stats = {
                                "word_count": data.get("word_count", 0),
                                "char_count": data.get("char_count", 0)
                            }
                            print()  # New line after streaming
                        
                        # Error event
                        elif "error" in data:
                            print(f"\n[FAIL] Error: {data.get('error')}")
                            return {"success": False, "error": data.get("error")}
                        
                        # Info event (provider switching)
                        elif "info" in data:
                            print(f"\n[INFO] {data.get('info')}")
                    
                    except json.JSONDecodeError:
                        continue
                
                end_time = time.time()
                response_time = round(end_time - start_time, 2)
                
                print("-" * 40)
                print(f"[PASS] SUCCESS ({response_time}s)")
                print(f"[INFO] Stats: {stats.get('word_count', 0)} words, {stats.get('char_count', 0)} chars")
                
                return {
                    "success": True,
                    "provider": provider_info.get("provider"),
                    "model": provider_info.get("model"),
                    "attempt": provider_info.get("attempt"),
                    "word_count": stats.get("word_count", 0),
                    "char_count": stats.get("char_count", 0),
                    "response_time": response_time,
                    "content_length": len(full_content)
                }
                
    except Exception as e:
        print(f"[FAIL] ERROR: {str(e)}")
        return {"success": False, "error": str(e)}

async def test_provider_status():
    """Check which providers are available before testing"""
    print("[INFO] Checking Provider Status...")
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{BASE_URL}/chat/providers")
            
            if response.status_code == 200:
                data = response.json()
                providers = data.get("providers", [])
                
                print(f"[INFO] Provider Status:")
                for provider in providers:
                    status = "[OK]" if provider.get("available") else "[NO KEY]"
                    print(f"  {provider.get('name', 'Unknown')}: {status}")
                
                available_count = data.get("available_providers", 0)
                total_count = data.get("total_providers", 0)
                print(f"\n[INFO] Summary: {available_count}/{total_count} providers available")
                
                return available_count > 0
            else:
                print(f"[FAIL] Failed to check provider status: {response.status_code}")
                return False
                
    except Exception as e:
        print(f"[FAIL] Error checking providers: {str(e)}")
        # Continue anyway - service might still work
        return True

async def main():
    """Run all 4 email tests with streaming"""
    print("[TEST] Multi-Provider Email Generation Test (v5.0)")
    print("Testing 4 different email scenarios with streaming to demonstrate fallback system")
    
    # Check if service is running
    service_available = await test_provider_status()
    if not service_available:
        print("\n[FAIL] Service not available or no providers configured")
        print("Make sure:")
        print("1. Service is running: python main.py")
        print("2. At least one API key is set in .env")
        return
    
    # Run all 4 email tests with streaming
    results = []
    
    for i, query in enumerate(EMAIL_QUERIES):
        result = await send_email_request_streaming(query)
        results.append(result)
        
        # Add delay between requests to potentially trigger different providers
        if i < len(EMAIL_QUERIES) - 1:
            print(f"\n[INFO] Waiting 2 seconds before next request...")
            await asyncio.sleep(2)
    
    # Summary
    print(f"\n{'='*60}")
    print("[INFO] TEST SUMMARY")
    print(f"{'='*60}")
    
    successful_tests = [r for r in results if r.get("success")]
    failed_tests = [r for r in results if not r.get("success")]
    
    print(f"[PASS] Successful: {len(successful_tests)}/{len(results)}")
    print(f"[FAIL] Failed: {len(failed_tests)}/{len(results)}")
    
    if successful_tests:
        print(f"\n[INFO] Providers Used:")
        providers_used = {}
        for i, result in enumerate(successful_tests):
            provider = result.get("provider", "unknown")
            model = result.get("model", "unknown")
            if provider in providers_used:
                providers_used[provider].append(i + 1)
            else:
                providers_used[provider] = [i + 1]
        
        for provider, email_numbers in providers_used.items():
            emails = ", ".join([f"Email {n}" for n in email_numbers])
            print(f"  {provider}: {emails}")
        
        print(f"\n[INFO] Performance:")
        avg_time = sum(r.get("response_time", 0) for r in successful_tests) / len(successful_tests)
        avg_words = sum(r.get("word_count", 0) for r in successful_tests) / len(successful_tests)
        print(f"  Average response time: {avg_time:.2f}s")
        print(f"  Average words generated: {avg_words:.0f}")
        
        # Check if different providers were used (demonstrates fallback)
        unique_providers = len(set(r.get("provider") for r in successful_tests if r.get("provider")))
        if unique_providers > 1:
            print(f"\n[INFO] Fallback Demonstrated: {unique_providers} different providers used!")
        else:
            print(f"\n[INFO] Consistent Provider: All requests used same provider (no fallback needed)")
        
        # Show attempts (indicates fallback was triggered)
        max_attempts = max(r.get("attempt", 1) for r in successful_tests)
        if max_attempts > 1:
            print(f"[INFO] Some requests required fallback (max attempts: {max_attempts})")
    
    if failed_tests:
        print(f"\n[FAIL] Failures:")
        for i, result in enumerate(results):
            if not result.get("success"):
                print(f"  Email {i + 1}: {result.get('error', 'Unknown error')}")
    
    print(f"\n{'='*60}")
    print("[INFO] Test Complete!")
    
    if len(successful_tests) == len(results):
        print("[PASS] All email generation tests passed!")
    elif len(successful_tests) > 0:
        print("[INFO] Some tests passed - check failures above")
    else:
        print("[FAIL] All tests failed - check service and API keys")

if __name__ == "__main__":
    print("Multi-Provider Email Generation Test (v5.0)")
    print("Make sure the AI service is running on http://localhost:8000\n")
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n[INFO] Test interrupted by user")
    except Exception as e:
        print(f"\n[FAIL] Test failed: {str(e)}")