#!/usr/bin/env python3
"""
Final demonstration of intelligent routing system
Shows how different complexity queries are routed to optimal providers
"""

import asyncio
import httpx
import json
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.ai_providers import analyze_query_complexity, get_optimal_providers_for_complexity

BASE_URL = "http://localhost:8000"

# Carefully crafted queries to demonstrate routing
DEMO_QUERIES = [
    {
        "prompt": "Hello",
        "content_type": "general",
        "description": "Simple Greeting (Complexity 1)",
        "note": "Should route to Groq (fast for simple queries)"
    },
    {
        "prompt": "Write a brief email confirming tomorrow's 2 PM meeting",
        "content_type": "email", 
        "description": "Basic Email (Complexity 2)",
        "note": "Should route to Groq or Together (good for standard emails)"
    },
    {
        "prompt": "Create a comprehensive technical blog post about microservices architecture patterns, including code examples, best practices, and performance considerations for enterprise applications",
        "content_type": "blog",
        "description": "Complex Technical Blog (Complexity 5)",
        "note": "Should route to DeepSeek or Gemini (best for technical content)"
    },
    {
        "prompt": "Write a detailed analysis comparing different machine learning frameworks, including TensorFlow, PyTorch, and JAX, with specific focus on performance benchmarks, ease of use, community support, and deployment strategies for production environments",
        "content_type": "technical",
        "description": "Very Complex Analysis (Complexity 5)",
        "note": "Should route to DeepSeek or Gemini (specialized for complex reasoning)"
    }
]

async def demonstrate_routing():
    """Demonstrate the intelligent routing system"""
    
    print("🧠 Intelligent Routing System Demonstration")
    print("=" * 70)
    print("This demo shows how queries are analyzed and routed to optimal providers")
    
    for i, query in enumerate(DEMO_QUERIES, 1):
        print(f"\n{'='*70}")
        print(f"DEMO {i}: {query['description']}")
        print(f"{'='*70}")
        
        # Analyze complexity locally first
        complexity = analyze_query_complexity(query['prompt'], query['content_type'])
        optimal_providers = get_optimal_providers_for_complexity(complexity)
        
        print(f"📝 Query: {query['prompt'][:100]}{'...' if len(query['prompt']) > 100 else ''}")
        print(f"📊 Content Type: {query['content_type']}")
        print(f"🧠 Analyzed Complexity: {complexity}/5")
        print(f"🎯 Optimal Provider Order: {[p['name'] for p in optimal_providers if p['api_key']]}")
        print(f"💡 Expected Behavior: {query['note']}")
        
        # Send request to service
        payload = {
            "prompt": query['prompt'],
            "content_type": query['content_type'],
            "user_id": f"demo-{i}"
        }
        
        try:
            print(f"\n🚀 Sending request to service...")
            
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(f"{BASE_URL}/chat/", json=payload)
                
                if response.status_code == 200:
                    data = response.json()
                    model_used = data.get('model_used', 'unknown')
                    provider_used = model_used.split('/')[0] if '/' in model_used else model_used
                    tokens = data.get('tokens_used', 0)
                    
                    print(f"✅ SUCCESS!")
                    print(f"🤖 Model Used: {model_used}")
                    print(f"🏢 Provider Used: {provider_used}")
                    print(f"🔢 Tokens Generated: {tokens}")
                    
                    # Check if routing was optimal
                    expected_providers = [p['name'] for p in optimal_providers[:2] if p['api_key']]
                    
                    if provider_used in expected_providers:
                        print(f"🎯 ✅ OPTIMAL ROUTING: Used {provider_used} (as expected)")
                    elif provider_used == 'fallback':
                        print(f"🔄 ⚠️  FALLBACK: All providers failed")
                    else:
                        print(f"🔄 ⚠️  ALTERNATIVE: Used {provider_used} (expected {expected_providers})")
                    
                    # Show content sample
                    content = data.get('content', '')
                    print(f"\n📄 Generated Content ({len(content)} characters):")
                    print("-" * 50)
                    preview = content[:300] + "..." if len(content) > 300 else content
                    print(preview)
                    print("-" * 50)
                    
                else:
                    print(f"❌ Request failed: {response.status_code}")
                    print(f"Error: {response.text}")
                    
        except Exception as e:
            print(f"❌ Error: {str(e)}")
        
        # Wait between requests
        if i < len(DEMO_QUERIES):
            print(f"\n⏳ Waiting 3 seconds before next demo...")
            await asyncio.sleep(3)
    
    print(f"\n{'='*70}")
    print("🎯 Intelligent Routing Demonstration Complete!")
    print("=" * 70)
    
    print("\n📊 Summary of Intelligent Routing System:")
    print("✅ Complexity Analysis: Automatically analyzes query difficulty (1-5)")
    print("✅ Provider Optimization: Routes to best provider for each complexity level")
    print("✅ Fallback System: Gracefully handles provider failures")
    print("✅ Performance Tuning: Uses fastest providers for simple queries")
    print("✅ Quality Optimization: Uses powerful providers for complex tasks")
    
    print(f"\n🏢 Provider Specializations:")
    print("  • Groq: Simple queries (1-3) - Speed optimized")
    print("  • Together: Medium queries (2-4) - Balanced performance") 
    print("  • DeepSeek: Complex queries (3-5) - Technical content")
    print("  • Gemini: Very complex queries (4-5) - Advanced reasoning")

async def main():
    """Run the routing demonstration"""
    
    # Check service status first
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{BASE_URL}/chat/providers")
            if response.status_code == 200:
                data = response.json()
                available = data.get("available_providers", 0)
                total = data.get("total_providers", 0)
                print(f"🔍 Service Status: {available}/{total} providers available\n")
            else:
                print("❌ Service not responding - make sure it's running on http://localhost:8000")
                return
    except Exception as e:
        print(f"❌ Cannot connect to service: {str(e)}")
        print("Make sure the AI service is running: python main.py")
        return
    
    await demonstrate_routing()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n⚠️  Demo interrupted by user")
    except Exception as e:
        print(f"\n❌ Demo failed: {str(e)}")