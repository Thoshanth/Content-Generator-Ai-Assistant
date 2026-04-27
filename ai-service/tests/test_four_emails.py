#!/usr/bin/env python3
"""
Test 4 different email queries to demonstrate multi-provider fallback
Each query will potentially use different providers/models
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

# 4 different email scenarios
EMAIL_QUERIES = [
    {
        "id": 1,
        "prompt": "Write a professional email to schedule a team meeting for next week to discuss Q1 project milestones",
        "description": "Business Meeting Email"
    },
    {
        "id": 2, 
        "prompt": "Write a follow-up email to a client thanking them for their feedback and addressing their concerns about delivery timeline",
        "description": "Client Follow-up Email"
    },
    {
        "id": 3,
        "prompt": "Write an email to HR requesting vacation time for a family wedding, including dates and coverage arrangements",
        "description": "HR Vacation Request Email"
    },
    {
        "id": 4,
        "prompt": "Write a welcome email for new team members joining our software development team, including onboarding information",
        "description": "Welcome/Onboarding Email"
    }
]

async def send_email_request(query_data):
    """Send a single email generation request"""
    payload = {
        "prompt": query_data["prompt"],
        "content_type": "email",
        "user_id": f"test-user-{query_data['id']}"
    }
    
    print(f"\n{'='*60}")
    print(f"EMAIL {query_data['id']}: {query_data['description']}")
    print(f"{'='*60}")
    print(f"📝 Prompt: {query_data['prompt']}")
    print(f"⏰ Time: {datetime.now().strftime('%H:%M:%S')}")
    
    try:
        start_time = time.time()
        
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(f"{BASE_URL}/chat/", json=payload)
            
            end_time = time.time()
            response_time = round(end_time - start_time, 2)
            
            if response.status_code == 200:
                data = response.json()
                
                print(f"✅ SUCCESS ({response_time}s)")
                print(f"🤖 Model Used: {data.get('model_used', 'unknown')}")
                print(f"🔢 Tokens: {data.get('tokens_used', 0)}")
                print(f"📧 Email Preview:")
                print("-" * 40)
                
                # Show first 300 characters of the email
                content = data.get('content', '')
                preview = content[:300] + "..." if len(content) > 300 else content
                print(preview)
                print("-" * 40)
                
                return {
                    "success": True,
                    "model": data.get('model_used'),
                    "tokens": data.get('tokens_used'),
                    "response_time": response_time,
                    "content_length": len(content)
                }
            else:
                print(f"❌ FAILED: Status {response.status_code}")
                print(f"Response: {response.text}")
                return {"success": False, "error": f"Status {response.status_code}"}
                
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        return {"success": False, "error": str(e)}

async def test_provider_status():
    """Check which providers are available before testing"""
    print("🔍 Checking Provider Status...")
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{BASE_URL}/chat/providers")
            
            if response.status_code == 200:
                data = response.json()
                providers = data.get("providers", [])
                
                print(f"📊 Provider Status:")
                for provider in providers:
                    status = "✅ Available" if provider["available"] else "❌ No API Key"
                    print(f"  {provider['name']}: {status} ({len(provider['models'])} models)")
                
                available_count = data.get("available_providers", 0)
                total_count = data.get("total_providers", 0)
                print(f"\n📈 Summary: {available_count}/{total_count} providers available")
                
                return available_count > 0
            else:
                print(f"❌ Failed to check provider status: {response.status_code}")
                return False
                
    except Exception as e:
        print(f"❌ Error checking providers: {str(e)}")
        return False

async def main():
    """Run all 4 email tests"""
    print("🚀 Multi-Provider Email Generation Test")
    print("Testing 4 different email scenarios to demonstrate fallback system")
    
    # Check if service is running
    service_available = await test_provider_status()
    if not service_available:
        print("\n❌ Service not available or no providers configured")
        print("Make sure:")
        print("1. Service is running: python main.py")
        print("2. At least one API key is set in .env")
        return
    
    # Run all 4 email tests
    results = []
    
    for i, query in enumerate(EMAIL_QUERIES):
        result = await send_email_request(query)
        results.append(result)
        
        # Add delay between requests to potentially trigger different providers
        if i < len(EMAIL_QUERIES) - 1:
            print(f"\n⏳ Waiting 2 seconds before next request...")
            await asyncio.sleep(2)
    
    # Summary
    print(f"\n{'='*60}")
    print("📊 TEST SUMMARY")
    print(f"{'='*60}")
    
    successful_tests = [r for r in results if r.get("success")]
    failed_tests = [r for r in results if not r.get("success")]
    
    print(f"✅ Successful: {len(successful_tests)}/{len(results)}")
    print(f"❌ Failed: {len(failed_tests)}/{len(results)}")
    
    if successful_tests:
        print(f"\n🤖 Models Used:")
        models_used = {}
        for i, result in enumerate(successful_tests):
            model = result.get("model", "unknown")
            if model in models_used:
                models_used[model].append(i + 1)
            else:
                models_used[model] = [i + 1]
        
        for model, email_numbers in models_used.items():
            emails = ", ".join([f"Email {n}" for n in email_numbers])
            print(f"  {model}: {emails}")
        
        print(f"\n⚡ Performance:")
        avg_time = sum(r.get("response_time", 0) for r in successful_tests) / len(successful_tests)
        avg_tokens = sum(r.get("tokens", 0) for r in successful_tests) / len(successful_tests)
        print(f"  Average response time: {avg_time:.2f}s")
        print(f"  Average tokens used: {avg_tokens:.0f}")
        
        # Check if different models were used (demonstrates fallback)
        unique_models = len(set(r.get("model") for r in successful_tests if r.get("model")))
        if unique_models > 1:
            print(f"\n🔄 Fallback Demonstrated: {unique_models} different models used!")
        else:
            print(f"\n📌 Consistent Provider: All requests used same model (no fallback needed)")
    
    if failed_tests:
        print(f"\n❌ Failures:")
        for i, result in enumerate(results):
            if not result.get("success"):
                print(f"  Email {i + 1}: {result.get('error', 'Unknown error')}")
    
    print(f"\n{'='*60}")
    print("🎯 Test Complete!")
    
    if len(successful_tests) == len(results):
        print("🎉 All email generation tests passed!")
    elif len(successful_tests) > 0:
        print("⚠️  Some tests passed - check failures above")
    else:
        print("❌ All tests failed - check service and API keys")

if __name__ == "__main__":
    print("Multi-Provider Email Generation Test")
    print("Make sure the AI service is running on http://localhost:8000\n")
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n⚠️  Test interrupted by user")
    except Exception as e:
        print(f"\n❌ Test failed: {str(e)}")