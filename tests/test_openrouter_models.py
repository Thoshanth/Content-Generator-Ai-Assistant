#!/usr/bin/env python3
"""
Test OpenRouter free models to find working ones
"""

import asyncio
import httpx
import os
from dotenv import load_dotenv

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1/chat/completions"

# Potential free models to test
TEST_MODELS = [
    "google/gemma-2-9b-it:free",
    "meta-llama/llama-3.1-8b-instruct:free", 
    "meta-llama/llama-3.2-3b-instruct:free",
    "mistralai/mistral-7b-instruct:free",
    "huggingfaceh4/zephyr-7b-beta:free",
    "openchat/openchat-7b:free",
    "gryphe/mythomist-7b:free",
    "undi95/toppy-m-7b:free",
    "openai/gpt-3.5-turbo",
    "anthropic/claude-3-haiku:beta",
    "google/gemma-7b-it:free",
    "microsoft/phi-3-mini-128k-instruct:free",
    "qwen/qwen-2-7b-instruct:free",
    "nvidia/nemotron-3-super-120b-a12b:free"
]

async def test_model(model: str) -> bool:
    """Test if a model is available and working"""
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost:5173",
        "X-Title": "AI Content Generator"
    }
    
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": "Hello"}],
        "max_tokens": 10
    }
    
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(
                OPENROUTER_BASE_URL,
                json=payload,
                headers=headers
            )
            
            if response.status_code == 200:
                return True
            elif response.status_code == 429:
                print(f"  ⚠️  {model}: Rate limited")
                return "rate_limited"
            else:
                print(f"  ❌ {model}: {response.status_code} - {response.text[:100]}")
                return False
                
    except Exception as e:
        print(f"  ❌ {model}: {str(e)}")
        return False

async def main():
    print("🔍 Testing OpenRouter free models...\n")
    
    working_models = []
    rate_limited_models = []
    
    for model in TEST_MODELS:
        print(f"Testing {model}...")
        result = await test_model(model)
        
        if result == True:
            print(f"  ✅ {model}: Working!")
            working_models.append(model)
        elif result == "rate_limited":
            rate_limited_models.append(model)
        
        await asyncio.sleep(1)  # Be nice to the API
    
    print(f"\n🎉 Results:")
    print(f"✅ Working models ({len(working_models)}):")
    for model in working_models:
        print(f"    \"{model}\",")
    
    print(f"\n⚠️  Rate limited models ({len(rate_limited_models)}):")
    for model in rate_limited_models:
        print(f"    \"{model}\",")
    
    if working_models:
        print(f"\n📝 Updated MODELS list for openrouter.py:")
        print("MODELS = [")
        for model in working_models:
            print(f"    \"{model}\",")
        print("]")

if __name__ == "__main__":
    asyncio.run(main())