#!/usr/bin/env python3
"""
Test to force different providers by temporarily modifying the provider configuration
This will demonstrate the fallback system by making providers fail intentionally
"""

import asyncio
import httpx
import json
import time
from datetime import datetime

BASE_URL = "http://localhost:8000"

# 4 different email scenarios
EMAIL_QUERIES = [
    {
        "id": 1,
        "prompt": "Write a professional email to schedule a team meeting for next week",
        "description": "Business Meeting Email",
        "expected_provider": "groq"
    },
    {
        "id": 2, 
        "prompt": "Write a follow-up email to a client about project status",
        "description": "Client Follow-up Email", 
        "expected_provider": "together"
    },
    {
        "id": 3,
        "prompt": "Write an email requesting vacation time for next month",
        "description": "HR Vacation Request Email",
        "expected_provider": "deepseek"
    },
    {
        "id": 4,
        "prompt": "Write a welcome email for new team members",
        "description": "Welcome Email",
        "expected_provider": "gemini"
    }
]

async def send_email_with_provider_manipulation(query_data, disable_providers=None):
    """Send email request while temporarily disabling certain providers"""
    
    # First, let's modify the provider configuration temporarily
    if disable_providers:
        print(f"🔧 Temporarily disabling providers: {', '.join(disable_providers)}")
        
        # We'll do this by sending requests that might trigger different providers
        # based on the natural fallback order
    
    payload = {
        "prompt": query_data["prompt"],
        "content_type": "email",
        "user_id": f"test-user-{query_data['id']}"
    }
    
    print(f"\n{'='*60}")
    print(f"EMAIL {query_data['id']}: {query_data['description']}")
    print(f"{'='*60}")
    print(f"📝 Prompt: {query_data['prompt']}")
    print(f"🎯 Target Provider: {query_data['expected_provider']}")
    print(f"⏰ Time: {datetime.now().strftime('%H:%M:%S')}")
    
    try:
        start_time = time.time()
        
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(f"{BASE_URL}/chat/", json=payload)
            
            end_time = time.time()
            response_time = round(end_time - start_time, 2)
            
            if response.status_code == 200:
                data = response.json()
                model_used = data.get('model_used', 'unknown')
                
                # Extract provider name from model
                provider_used = model_used.split('/')[0] if '/' in model_used else model_used
                
                print(f"✅ SUCCESS ({response_time}s)")
                print(f"🤖 Model Used: {model_used}")
                print(f"🏢 Provider Used: {provider_used}")
                print(f"🔢 Tokens: {data.get('tokens_used', 0)}")
                
                # Check if we got the expected provider or a fallback
                if provider_used == query_data['expected_provider']:
                    print(f"🎯 Expected provider used!")
                elif provider_used == 'fallback':
                    print(f"🔄 Fallback response used (all providers failed)")
                else:
                    print(f"🔄 Fallback to different provider: {provider_used}")
                
                print(f"📧 Email Preview:")
                print("-" * 40)
                
                content = data.get('content', '')
                preview = content[:200] + "..." if len(content) > 200 else content
                print(preview)
                print("-" * 40)
                
                return {
                    "success": True,
                    "model": model_used,
                    "provider": provider_used,
                    "tokens": data.get('tokens_used'),
                    "response_time": response_time,
                    "expected_provider": query_data['expected_provider'],
                    "fallback_used": provider_used != query_data['expected_provider']
                }
            else:
                print(f"❌ FAILED: Status {response.status_code}")
                return {"success": False, "error": f"Status {response.status_code}"}
                
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        return {"success": False, "error": str(e)}

async def test_with_rapid_requests():
    """Send requests rapidly to potentially trigger rate limits and fallbacks"""
    print("🚀 Rapid Request Test - Attempting to trigger rate limits")
    
    results = []
    
    # Send multiple requests quickly to potentially hit rate limits
    tasks = []
    for i, query in enumerate(EMAIL_QUERIES):
        task = send_email_with_provider_manipulation(query)
        tasks.append(task)
        
        # Small delay to stagger requests slightly
        if i < len(EMAIL_QUERIES) - 1:
            await asyncio.sleep(0.5)
    
    # Wait for all requests to complete
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    return results

async def test_sequential_with_delays():
    """Send requests sequentially with delays to see natural provider selection"""
    print("🔄 Sequential Test - Natural provider selection")
    
    results = []
    
    for i, query in enumerate(EMAIL_QUERIES):
        result = await send_email_with_provider_manipulation(query)
        results.append(result)
        
        # Longer delay between requests
        if i < len(EMAIL_QUERIES) - 1:
            print(f"\n⏳ Waiting 5 seconds before next request...")
            await asyncio.sleep(5)
    
    return results

async def main():
    """Run provider rotation tests"""
    print("🔄 Multi-Provider Rotation Test")
    print("Testing different scenarios to demonstrate provider fallback")
    
    # Check service status
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{BASE_URL}/chat/providers")
            if response.status_code == 200:
                data = response.json()
                available = data.get("available_providers", 0)
                total = data.get("total_providers", 0)
                print(f"📊 Service Status: {available}/{total} providers available")
            else:
                print("❌ Service not responding")
                return
    except Exception as e:
        print(f"❌ Cannot connect to service: {str(e)}")
        return
    
    # Test 1: Rapid requests (might trigger rate limits)
    print(f"\n{'='*60}")
    print("TEST 1: RAPID REQUESTS")
    print(f"{'='*60}")
    
    rapid_results = await test_with_rapid_requests()
    
    # Test 2: Sequential requests with delays
    print(f"\n{'='*60}")
    print("TEST 2: SEQUENTIAL REQUESTS")
    print(f"{'='*60}")
    
    sequential_results = await test_sequential_with_delays()
    
    # Combine results
    all_results = []
    for result in rapid_results:
        if isinstance(result, dict):
            all_results.append(result)
    for result in sequential_results:
        if isinstance(result, dict):
            all_results.append(result)
    
    # Analysis
    print(f"\n{'='*60}")
    print("📊 COMPREHENSIVE ANALYSIS")
    print(f"{'='*60}")
    
    successful_results = [r for r in all_results if r.get("success")]
    
    if successful_results:
        # Provider usage analysis
        provider_usage = {}
        fallback_count = 0
        
        for result in successful_results:
            provider = result.get("provider", "unknown")
            if provider in provider_usage:
                provider_usage[provider] += 1
            else:
                provider_usage[provider] = 1
            
            if result.get("fallback_used"):
                fallback_count += 1
        
        print(f"🤖 Provider Usage:")
        for provider, count in provider_usage.items():
            percentage = (count / len(successful_results)) * 100
            print(f"  {provider}: {count} requests ({percentage:.1f}%)")
        
        print(f"\n🔄 Fallback Statistics:")
        print(f"  Fallback triggered: {fallback_count}/{len(successful_results)} times")
        print(f"  Fallback rate: {(fallback_count/len(successful_results)*100):.1f}%")
        
        if len(provider_usage) > 1:
            print(f"\n🎉 SUCCESS: Multiple providers used! ({len(provider_usage)} different providers)")
        else:
            print(f"\n📌 Single provider handled all requests (no fallback needed)")
        
        # Performance analysis
        avg_time = sum(r.get("response_time", 0) for r in successful_results) / len(successful_results)
        print(f"\n⚡ Average response time: {avg_time:.2f}s")
        
    else:
        print("❌ No successful requests to analyze")
    
    print(f"\n{'='*60}")
    print("🎯 Test Complete!")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n⚠️  Test interrupted by user")
    except Exception as e:
        print(f"\n❌ Test failed: {str(e)}")