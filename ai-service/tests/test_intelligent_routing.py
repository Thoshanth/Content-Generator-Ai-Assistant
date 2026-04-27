#!/usr/bin/env python3
"""
Test intelligent provider routing based on query complexity
Demonstrates how different queries are routed to optimal providers
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

# Test queries with different complexity levels
TEST_QUERIES = [
    {
        "id": 1,
        "prompt": "Hi",
        "content_type": "general",
        "description": "Very Simple Query",
        "expected_complexity": 1,
        "expected_provider": "groq"
    },
    {
        "id": 2,
        "prompt": "Write a short email to confirm meeting time",
        "content_type": "email", 
        "description": "Simple Email",
        "expected_complexity": 2,
        "expected_provider": "groq"
    },
    {
        "id": 3,
        "prompt": "Write a professional email to a client explaining project delays and proposing solutions with timeline adjustments",
        "content_type": "email",
        "description": "Medium Complexity Email", 
        "expected_complexity": 3,
        "expected_provider": "together"
    },
    {
        "id": 4,
        "prompt": "Write a comprehensive blog post analyzing the impact of artificial intelligence on modern software development practices, including detailed technical examples and future predictions",
        "content_type": "blog",
        "description": "Complex Blog Post",
        "expected_complexity": 4,
        "expected_provider": "gemini"
    },
    {
        "id": 5,
        "prompt": "Create a detailed technical specification document for a distributed microservices architecture, including API design patterns, database schema optimization, security considerations, performance benchmarks, and comprehensive deployment strategies with monitoring and alerting systems",
        "content_type": "technical",
        "description": "Very Complex Technical Document",
        "expected_complexity": 5,
        "expected_provider": "gemini"
    }
]

async def test_query_routing(query_data):
    """Test a single query and analyze the routing decision"""
    payload = {
        "prompt": query_data["prompt"],
        "content_type": query_data["content_type"],
        "user_id": f"test-routing-{query_data['id']}"
    }
    
    print(f"\n{'='*70}")
    print(f"TEST {query_data['id']}: {query_data['description']}")
    print(f"{'='*70}")
    print(f"📝 Prompt: {query_data['prompt'][:100]}{'...' if len(query_data['prompt']) > 100 else ''}")
    print(f"📊 Content Type: {query_data['content_type']}")
    print(f"🎯 Expected Complexity: {query_data['expected_complexity']}/5")
    print(f"🏢 Expected Provider: {query_data['expected_provider']}")
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
                provider_used = model_used.split('/')[0] if '/' in model_used else model_used
                
                print(f"\n✅ SUCCESS ({response_time}s)")
                print(f"🤖 Model Used: {model_used}")
                print(f"🏢 Provider Used: {provider_used}")
                print(f"🔢 Tokens: {data.get('tokens_used', 0)}")
                
                # Analyze routing decision
                if provider_used == query_data['expected_provider']:
                    print(f"🎯 ✅ OPTIMAL ROUTING: Used expected provider ({provider_used})")
                    routing_optimal = True
                elif provider_used == 'fallback':
                    print(f"🔄 ⚠️  FALLBACK: All providers failed, used fallback response")
                    routing_optimal = False
                else:
                    print(f"🔄 ⚠️  ALTERNATIVE ROUTING: Expected {query_data['expected_provider']}, got {provider_used}")
                    routing_optimal = False
                
                # Show content preview
                content = data.get('content', '')
                content_length = len(content)
                
                print(f"📄 Content Length: {content_length} characters")
                print(f"📖 Content Preview:")
                print("-" * 50)
                preview = content[:200] + "..." if len(content) > 200 else content
                print(preview)
                print("-" * 50)
                
                return {
                    "success": True,
                    "model": model_used,
                    "provider": provider_used,
                    "tokens": data.get('tokens_used', 0),
                    "response_time": response_time,
                    "content_length": content_length,
                    "routing_optimal": routing_optimal,
                    "expected_provider": query_data['expected_provider'],
                    "expected_complexity": query_data['expected_complexity']
                }
            else:
                print(f"❌ FAILED: Status {response.status_code}")
                print(f"Response: {response.text}")
                return {"success": False, "error": f"Status {response.status_code}"}
                
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        return {"success": False, "error": str(e)}

async def test_provider_status():
    """Check provider availability"""
    print("🔍 Checking Provider Status for Intelligent Routing...")
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{BASE_URL}/chat/providers")
            
            if response.status_code == 200:
                data = response.json()
                providers = data.get("providers", [])
                
                print(f"📊 Provider Status:")
                for provider in providers:
                    status = "✅ Available" if provider["available"] else "❌ No API Key"
                    print(f"  {provider['name']}: {status}")
                
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
    """Run intelligent routing tests"""
    print("🧠 Intelligent Provider Routing Test")
    print("Testing how queries of different complexity are routed to optimal providers")
    
    # Check service availability
    service_available = await test_provider_status()
    if not service_available:
        print("\n❌ Service not available or no providers configured")
        return
    
    # Run all routing tests
    results = []
    
    for query in TEST_QUERIES:
        result = await test_query_routing(query)
        results.append(result)
        
        # Small delay between requests
        if query != TEST_QUERIES[-1]:
            print(f"\n⏳ Waiting 2 seconds before next test...")
            await asyncio.sleep(2)
    
    # Comprehensive Analysis
    print(f"\n{'='*70}")
    print("📊 INTELLIGENT ROUTING ANALYSIS")
    print(f"{'='*70}")
    
    successful_results = [r for r in results if r.get("success")]
    failed_results = [r for r in results if not r.get("success")]
    
    print(f"✅ Successful Tests: {len(successful_results)}/{len(results)}")
    print(f"❌ Failed Tests: {len(failed_results)}/{len(results)}")
    
    if successful_results:
        # Routing Analysis
        optimal_routing_count = sum(1 for r in successful_results if r.get("routing_optimal"))
        routing_accuracy = (optimal_routing_count / len(successful_results)) * 100
        
        print(f"\n🎯 Routing Accuracy: {optimal_routing_count}/{len(successful_results)} ({routing_accuracy:.1f}%)")
        
        # Provider Usage by Complexity
        print(f"\n🏢 Provider Usage by Complexity:")
        complexity_routing = {}
        
        for result in successful_results:
            complexity = result.get("expected_complexity", 0)
            provider = result.get("provider", "unknown")
            
            if complexity not in complexity_routing:
                complexity_routing[complexity] = {}
            
            if provider in complexity_routing[complexity]:
                complexity_routing[complexity][provider] += 1
            else:
                complexity_routing[complexity][provider] = 1
        
        for complexity in sorted(complexity_routing.keys()):
            print(f"  Complexity {complexity}: ", end="")
            providers = complexity_routing[complexity]
            provider_list = [f"{provider}({count})" for provider, count in providers.items()]
            print(", ".join(provider_list))
        
        # Performance Analysis
        print(f"\n⚡ Performance by Complexity:")
        complexity_performance = {}
        
        for result in successful_results:
            complexity = result.get("expected_complexity", 0)
            response_time = result.get("response_time", 0)
            
            if complexity not in complexity_performance:
                complexity_performance[complexity] = []
            complexity_performance[complexity].append(response_time)
        
        for complexity in sorted(complexity_performance.keys()):
            times = complexity_performance[complexity]
            avg_time = sum(times) / len(times)
            print(f"  Complexity {complexity}: {avg_time:.2f}s average")
        
        # Content Length Analysis
        print(f"\n📄 Content Generation Analysis:")
        for i, result in enumerate(successful_results):
            query = TEST_QUERIES[i]
            content_length = result.get("content_length", 0)
            tokens = result.get("tokens", 0)
            provider = result.get("provider", "unknown")
            
            print(f"  {query['description']}: {content_length} chars, {tokens} tokens ({provider})")
        
        # Routing Recommendations
        print(f"\n💡 Routing Insights:")
        
        if routing_accuracy >= 80:
            print("  ✅ Excellent routing accuracy - system is working optimally")
        elif routing_accuracy >= 60:
            print("  ⚠️  Good routing accuracy - some optimization possible")
        else:
            print("  ❌ Poor routing accuracy - system needs adjustment")
        
        # Check if complexity scaling works
        providers_used = set(r.get("provider") for r in successful_results if r.get("provider") != "fallback")
        if len(providers_used) > 1:
            print("  ✅ Multiple providers used - complexity scaling working")
        else:
            print("  ⚠️  Only one provider used - check if others are available")
    
    if failed_results:
        print(f"\n❌ Failed Tests:")
        for i, result in enumerate(results):
            if not result.get("success"):
                query = TEST_QUERIES[i]
                print(f"  {query['description']}: {result.get('error', 'Unknown error')}")
    
    print(f"\n{'='*70}")
    print("🎯 Intelligent Routing Test Complete!")
    
    if len(successful_results) == len(results):
        print("🎉 All routing tests passed!")
    elif len(successful_results) > 0:
        print("⚠️  Some tests passed - check failures above")
    else:
        print("❌ All tests failed - check service and API keys")

if __name__ == "__main__":
    print("Intelligent Provider Routing Test")
    print("Make sure the AI service is running on http://localhost:8000\n")
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n⚠️  Test interrupted by user")
    except Exception as e:
        print(f"\n❌ Test failed: {str(e)}")