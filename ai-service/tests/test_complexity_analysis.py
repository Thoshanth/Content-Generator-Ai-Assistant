#!/usr/bin/env python3
"""
Test the complexity analysis function directly
"""

import asyncio
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.ai_providers import analyze_query_complexity, get_optimal_providers_for_complexity, PROVIDERS

def test_complexity_analysis():
    """Test the complexity analysis function"""
    
    test_cases = [
        {
            "prompt": "Hi",
            "content_type": "general",
            "expected_complexity": 1,
            "description": "Very simple greeting"
        },
        {
            "prompt": "Write a short email to confirm meeting time",
            "content_type": "email",
            "expected_complexity": 2,
            "description": "Simple email"
        },
        {
            "prompt": "Write a professional email to a client explaining project delays and proposing solutions with timeline adjustments",
            "content_type": "email",
            "expected_complexity": 3,
            "description": "Medium complexity email"
        },
        {
            "prompt": "Write a comprehensive blog post analyzing the impact of artificial intelligence on modern software development practices, including detailed technical examples and future predictions",
            "content_type": "blog",
            "expected_complexity": 4,
            "description": "Complex blog post"
        },
        {
            "prompt": "Create a detailed technical specification document for a distributed microservices architecture, including API design patterns, database schema optimization, security considerations, performance benchmarks, and comprehensive deployment strategies with monitoring and alerting systems",
            "content_type": "technical",
            "expected_complexity": 5,
            "description": "Very complex technical document"
        }
    ]
    
    print("🧠 Testing Complexity Analysis Function")
    print("=" * 60)
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\nTest {i}: {test_case['description']}")
        print(f"Prompt: {test_case['prompt'][:80]}{'...' if len(test_case['prompt']) > 80 else ''}")
        print(f"Content Type: {test_case['content_type']}")
        
        # Analyze complexity
        actual_complexity = analyze_query_complexity(
            test_case['prompt'], 
            test_case['content_type']
        )
        
        expected = test_case['expected_complexity']
        
        print(f"Expected Complexity: {expected}/5")
        print(f"Actual Complexity: {actual_complexity}/5")
        
        if actual_complexity == expected:
            print("✅ CORRECT complexity analysis")
        else:
            print(f"⚠️  DIFFERENT complexity (expected {expected}, got {actual_complexity})")
        
        # Get optimal providers
        optimal_providers = get_optimal_providers_for_complexity(actual_complexity)
        provider_names = [p['name'] for p in optimal_providers if p['api_key']]
        
        print(f"Optimal Providers: {provider_names}")
        
        # Show provider details
        for provider in optimal_providers[:2]:  # Show top 2
            if provider['api_key']:
                complexity_range = provider['complexity_range']
                strengths = provider['strengths']
                print(f"  {provider['name']}: Range {complexity_range[0]}-{complexity_range[1]}, Strengths: {strengths}")

def test_provider_configuration():
    """Test provider configuration"""
    print("\n" + "=" * 60)
    print("🔧 Provider Configuration Analysis")
    print("=" * 60)
    
    for provider in PROVIDERS:
        print(f"\n{provider['name'].upper()}:")
        print(f"  API Key: {'✅ Set' if provider['api_key'] else '❌ Not Set'}")
        print(f"  Complexity Range: {provider['complexity_range'][0]}-{provider['complexity_range'][1]}")
        print(f"  Strengths: {', '.join(provider['strengths'])}")
        print(f"  Models: {len(provider['models'])} available")
        print(f"  Max Efficient Tokens: {provider['max_tokens_efficient']}")

def main():
    """Run all tests"""
    test_complexity_analysis()
    test_provider_configuration()
    
    print("\n" + "=" * 60)
    print("🎯 Complexity Analysis Test Complete!")
    print("=" * 60)

if __name__ == "__main__":
    main()