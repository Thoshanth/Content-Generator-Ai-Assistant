#!/usr/bin/env python3
"""
Test script for the new multi-provider AI system.
Tests each provider individually and the fallback mechanism.
"""

import asyncio
import os
import sys
from dotenv import load_dotenv

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.ai_providers import generate_content, generate_content_stream, get_available_providers

load_dotenv()

async def test_providers():
    """Test all available providers."""
    print("🔍 Testing Multi-Provider AI System")
    print("=" * 50)
    
    # Check provider status
    providers = get_available_providers()
    print("\n📊 Provider Status:")
    for provider in providers:
        status = "✅ Available" if provider["available"] else "❌ No API Key"
        print(f"  {provider['name']}: {status}")
        if provider["available"]:
            print(f"    Models: {', '.join(provider['models'][:2])}...")  # Show first 2 models
    
    available_count = len([p for p in providers if p["available"]])
    print(f"\n📈 Summary: {available_count}/{len(providers)} providers available")
    
    if available_count == 0:
        print("\n⚠️  No providers available. Please set API keys in .env file:")
        print("   GROQ_API_KEY=your_groq_key")
        print("   GEMINI_API_KEY=your_gemini_key")
        print("   TOGETHER_API_KEY=your_together_key")
        print("   DEEPSEEK_API_KEY=your_deepseek_key")
        return
    
    # Test content generation
    print("\n🧪 Testing Content Generation...")
    test_prompt = "Write a short professional email about scheduling a meeting."
    
    try:
        content, model_used, tokens_used = await generate_content(
            prompt=test_prompt,
            content_type="email"
        )
        
        print(f"\n✅ Success!")
        print(f"   Model used: {model_used}")
        print(f"   Tokens used: {tokens_used}")
        print(f"   Content preview: {content[:100]}...")
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
    
    # Test streaming
    print("\n🌊 Testing Streaming...")
    try:
        chunks = []
        async for chunk in generate_content_stream(
            prompt="Write a very short greeting message.",
            content_type="general"
        ):
            if "error" in chunk:
                print(f"❌ Streaming error: {chunk['error']}")
                break
            elif "content" in chunk:
                chunks.append(chunk["content"])
                if len(chunks) <= 3:  # Show first few chunks
                    print(f"   Chunk: '{chunk['content']}'")
        
        if chunks and not any("error" in str(chunk) for chunk in chunks):
            print(f"✅ Streaming successful! Received {len(chunks)} chunks")
        
    except Exception as e:
        print(f"❌ Streaming error: {str(e)}")

async def test_fallback():
    """Test fallback mechanism when all providers fail."""
    print("\n🔄 Testing Fallback Mechanism...")
    
    # Temporarily break all API keys to test fallback
    original_keys = {}
    providers_module = __import__('services.ai_providers', fromlist=['PROVIDERS'])
    
    for provider in providers_module.PROVIDERS:
        original_keys[provider['name']] = provider['api_key']
        provider['api_key'] = None  # Break the API key
    
    try:
        content, model_used, tokens_used = await generate_content(
            prompt="Test fallback message",
            content_type="general"
        )
        
        if model_used == "fallback":
            print("✅ Fallback mechanism working correctly")
            print(f"   Fallback content preview: {content[:100]}...")
        else:
            print("⚠️  Expected fallback but got a real response")
            
    except Exception as e:
        print(f"❌ Fallback test error: {str(e)}")
    
    finally:
        # Restore original API keys
        for provider in providers_module.PROVIDERS:
            provider['api_key'] = original_keys[provider['name']]

async def main():
    """Run all tests."""
    await test_providers()
    await test_fallback()
    
    print("\n" + "=" * 50)
    print("🎯 Test Complete!")
    print("\nNext steps:")
    print("1. Add your API keys to ai-service/.env")
    print("2. Start the service: python main.py")
    print("3. Test the API: curl http://localhost:8000/chat/providers")

if __name__ == "__main__":
    asyncio.run(main())