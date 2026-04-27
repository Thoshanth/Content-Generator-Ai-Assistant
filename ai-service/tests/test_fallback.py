#!/usr/bin/env python3
"""
Specific test for multi-provider fallback mechanism
Tests what happens when providers/models fail
"""

import asyncio
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.ai_providers import generate_content, PROVIDERS, get_available_providers

async def test_fallback():
    print("="*60)
    print("MULTI-PROVIDER FALLBACK MECHANISM TEST")
    print("="*60)
    
    # Show available providers
    providers = get_available_providers()
    print(f"\nConfigured providers:")
    for provider in providers:
        status = "✅ Available" if provider["available"] else "❌ No API Key"
        print(f"  {provider['name']}: {status} ({len(provider['models'])} models)")
    
    available_count = len([p for p in providers if p["available"]])
    if available_count == 0:
        print("\n❌ No providers available! Set API keys in .env file:")
        print("   GROQ_API_KEY=your_groq_key")
        print("   GEMINI_API_KEY=your_gemini_key")
        print("   TOGETHER_API_KEY=your_together_key")
        print("   DEEPSEEK_API_KEY=your_deepseek_key")
        return False
    
    print("\n" + "-"*60)
    print("Testing with simple prompt...")
    print("-"*60)
    
    try:
        content, model_used, tokens = await generate_content(
            prompt="Say 'Hello from multi-provider fallback test'",
            content_type="general",
            conversation_history=None
        )
        
        print(f"\n✓ SUCCESS!")
        print(f"  Provider/Model used: {model_used}")
        print(f"  Tokens: {tokens}")
        print(f"  Content: {content[:100]}...")
        
        # Check which provider was used
        if model_used == "fallback":
            print(f"\n⚠ All providers failed - using fallback response")
        else:
            provider_name = model_used.split('/')[0] if '/' in model_used else model_used
            print(f"\n✓ Successfully used provider: {provider_name}")
        
        return True
        
    except Exception as e:
        print(f"\n✗ FAILED: {str(e)}")
        print("\nAll providers failed. This could mean:")
        print("  1. API keys are invalid")
        print("  2. All providers are rate-limited")
        print("  3. Network connectivity issues")
        print("  4. Provider services are down")
        return False

async def test_each_provider():
    print("\n" + "="*60)
    print("TESTING EACH PROVIDER INDIVIDUALLY")
    print("="*60)
    
    from services.ai_providers import call_standard_api, call_gemini_api
    
    for provider in PROVIDERS:
        if not provider["api_key"]:
            print(f"\n❌ {provider['name']}: No API key set")
            continue
            
        print(f"\n🔄 Testing {provider['name']}...")
        
        # Test first model for each provider
        model = provider["models"][0]
        
        try:
            if provider.get("special_handling"):
                # Gemini API
                content, tokens = await call_gemini_api(
                    model=model,
                    prompt="Say 'test'",
                    content_type="general",
                    conversation_history=None,
                    api_key=provider["api_key"]
                )
            else:
                # Standard OpenAI-compatible API
                content, tokens = await call_standard_api(
                    provider=provider,
                    model=model,
                    prompt="Say 'test'",
                    content_type="general",
                    conversation_history=None,
                    stream=False
                )
            
            print(f"   ✓ SUCCESS - {tokens} tokens")
            print(f"   Model: {model}")
            print(f"   Response: {content[:50]}...")
            
        except Exception as e:
            error_msg = str(e)
            if "404" in error_msg:
                print(f"   ✗ Model not found (404)")
            elif "429" in error_msg:
                print(f"   ✗ Rate limited (429)")
            elif "401" in error_msg or "403" in error_msg:
                print(f"   ✗ Authentication error")
            else:
                print(f"   ✗ Error: {error_msg[:100]}")

async def test_forced_fallback():
    """Test what happens when we force all providers to fail"""
    print("\n" + "="*60)
    print("TESTING FORCED FALLBACK (All Providers Fail)")
    print("="*60)
    
    # Temporarily break all API keys
    original_keys = {}
    for provider in PROVIDERS:
        original_keys[provider['name']] = provider['api_key']
        provider['api_key'] = None  # Break the API key
    
    try:
        print("🔄 Forcing all providers to fail...")
        
        content, model_used, tokens = await generate_content(
            prompt="This should trigger fallback",
            content_type="general"
        )
        
        if model_used == "fallback":
            print("✓ Fallback mechanism working correctly!")
            print(f"   Fallback content: {content[:100]}...")
            success = True
        else:
            print(f"⚠ Expected fallback but got: {model_used}")
            success = False
            
    except Exception as e:
        print(f"✗ Forced fallback test failed: {str(e)}")
        success = False
    
    finally:
        # Restore original API keys
        for provider in PROVIDERS:
            provider['api_key'] = original_keys[provider['name']]
    
    return success

if __name__ == "__main__":
    print("\nMulti-Provider Fallback Mechanism Test")
    print("Make sure .env file has at least one API key set\n")
    
    try:
        # Test normal fallback
        success1 = asyncio.run(test_fallback())
        
        # Test each provider
        asyncio.run(test_each_provider())
        
        # Test forced fallback
        success2 = asyncio.run(test_forced_fallback())
        
        print("\n" + "="*60)
        if success1 and success2:
            print("✓ Multi-provider fallback mechanism is working!")
        else:
            print("✗ Some fallback tests failed - check providers")
        print("="*60)
        
    except KeyboardInterrupt:
        print("\n\nTest interrupted")
    except Exception as e:
        print(f"\n✗ Test failed: {str(e)}")