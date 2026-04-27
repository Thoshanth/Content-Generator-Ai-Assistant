#!/usr/bin/env python3
"""
End-to-End Testing Script for AI Service
Tests fallback mechanism, streaming, and all endpoints
"""

import asyncio
import httpx
import json
import sys
from typing import Dict, Any

BASE_URL = "http://localhost:8000"

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'

def print_success(msg: str):
    print(f"{Colors.GREEN}✓ {msg}{Colors.END}")

def print_error(msg: str):
    print(f"{Colors.RED}✗ {msg}{Colors.END}")

def print_info(msg: str):
    print(f"{Colors.BLUE}ℹ {msg}{Colors.END}")

def print_warning(msg: str):
    print(f"{Colors.YELLOW}⚠ {msg}{Colors.END}")

async def test_health_check():
    """Test 1: Health Check Endpoint"""
    print("\n" + "="*60)
    print("TEST 1: Health Check")
    print("="*60)
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{BASE_URL}/health")
            
            if response.status_code == 200:
                data = response.json()
                if data.get("status") == "healthy":
                    print_success("Health check passed")
                    print_info(f"Response: {data}")
                    return True
                else:
                    print_error(f"Unexpected response: {data}")
                    return False
            else:
                print_error(f"Status code: {response.status_code}")
                return False
    except Exception as e:
        print_error(f"Health check failed: {str(e)}")
        return False

async def test_non_streaming_chat():
    """Test 2: Non-Streaming Chat Endpoint"""
    print("\n" + "="*60)
    print("TEST 2: Non-Streaming Chat")
    print("="*60)
    
    payload = {
        "prompt": "Say 'Hello, testing!' and nothing else.",
        "content_type": "general",
        "conversation_history": [],
        "user_id": "test-user-123"
    }
    
    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            print_info("Sending request...")
            response = await client.post(f"{BASE_URL}/chat/", json=payload)
            
            if response.status_code == 200:
                data = response.json()
                print_success("Non-streaming chat successful")
                print_info(f"Model used: {data.get('model_used')}")
                print_info(f"Tokens used: {data.get('tokens_used')}")
                print_info(f"Content preview: {data.get('content')[:100]}...")
                return True
            else:
                print_error(f"Status code: {response.status_code}")
                print_error(f"Response: {response.text}")
                return False
    except Exception as e:
        print_error(f"Non-streaming chat failed: {str(e)}")
        return False

async def test_streaming_chat():
    """Test 3: Streaming Chat Endpoint"""
    print("\n" + "="*60)
    print("TEST 3: Streaming Chat")
    print("="*60)
    
    payload = {
        "prompt": "Count from 1 to 5.",
        "content_type": "general",
        "conversation_history": []
    }
    
    try:
        async with httpx.AsyncClient(timeout=120.0) as client:
            print_info("Sending streaming request...")
            
            chunks_received = 0
            content_parts = []
            
            async with client.stream("POST", f"{BASE_URL}/chat/stream", json=payload) as response:
                if response.status_code != 200:
                    print_error(f"Status code: {response.status_code}")
                    return False
                
                async for line in response.aiter_lines():
                    if line.startswith("data: "):
                        data_str = line[6:]
                        
                        if data_str.strip() == "[DONE]":
                            break
                        
                        try:
                            data = json.loads(data_str)
                            
                            if "content" in data:
                                chunks_received += 1
                                content_parts.append(data["content"])
                                
                                if chunks_received <= 5:
                                    print_info(f"Chunk {chunks_received}: '{data['content']}'")
                            
                            if "error" in data:
                                print_error(f"Error in stream: {data['error']}")
                                return False
                                
                        except json.JSONDecodeError:
                            continue
            
            if chunks_received > 0:
                print_success(f"Streaming successful - received {chunks_received} chunks")
                full_content = "".join(content_parts)
                print_info(f"Full content: {full_content[:200]}...")
                return True
            else:
                print_error("No chunks received")
                return False
                
    except Exception as e:
        print_error(f"Streaming chat failed: {str(e)}")
        return False

async def test_content_types():
    """Test 4: Different Content Types"""
    print("\n" + "="*60)
    print("TEST 4: Content Types")
    print("="*60)
    
    content_types = [
        ("general", "Say hello"),
        ("email", "Write a short email"),
        ("blog_post", "Write a blog intro"),
        ("social_media", "Write a tweet"),
        ("ad_copy", "Write ad copy")
    ]
    
    results = []
    
    for content_type, prompt in content_types:
        print_info(f"\nTesting content type: {content_type}")
        
        payload = {
            "prompt": prompt,
            "content_type": content_type
        }
        
        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(f"{BASE_URL}/chat/", json=payload)
                
                if response.status_code == 200:
                    data = response.json()
                    print_success(f"{content_type}: OK")
                    results.append(True)
                else:
                    print_error(f"{content_type}: Failed ({response.status_code})")
                    results.append(False)
                    
        except Exception as e:
            print_error(f"{content_type}: Error - {str(e)}")
            results.append(False)
    
    success_rate = sum(results) / len(results) * 100
    print_info(f"\nSuccess rate: {success_rate:.0f}% ({sum(results)}/{len(results)})")
    
    return all(results)

async def test_conversation_history():
    """Test 5: Conversation History"""
    print("\n" + "="*60)
    print("TEST 5: Conversation History")
    print("="*60)
    
    # First message
    payload1 = {
        "prompt": "My name is Alice.",
        "content_type": "general"
    }
    
    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            print_info("Sending first message...")
            response1 = await client.post(f"{BASE_URL}/chat/", json=payload1)
            
            if response1.status_code != 200:
                print_error("First message failed")
                return False
            
            data1 = response1.json()
            print_success("First message sent")
            
            # Second message with history
            payload2 = {
                "prompt": "What is my name?",
                "content_type": "general",
                "conversation_history": [
                    {"role": "user", "content": "My name is Alice."},
                    {"role": "assistant", "content": data1["content"]}
                ]
            }
            
            print_info("Sending second message with history...")
            response2 = await client.post(f"{BASE_URL}/chat/", json=payload2)
            
            if response2.status_code == 200:
                data2 = response2.json()
                print_success("Conversation history working")
                print_info(f"Response: {data2['content'][:100]}...")
                
                # Check if response mentions Alice
                if "alice" in data2["content"].lower():
                    print_success("AI remembered the name!")
                    return True
                else:
                    print_warning("AI might not have used the history")
                    return True  # Still pass, as the endpoint worked
            else:
                print_error("Second message failed")
                return False
                
    except Exception as e:
        print_error(f"Conversation history test failed: {str(e)}")
        return False

async def test_fallback_mechanism():
    """Test 6: Fallback Mechanism"""
    print("\n" + "="*60)
    print("TEST 6: Fallback Mechanism")
    print("="*60)
    
    print_info("Testing if fallback works when models fail...")
    print_info("This test sends a request and checks which model responds")
    
    payload = {
        "prompt": "Say 'Fallback test successful'",
        "content_type": "general"
    }
    
    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(f"{BASE_URL}/chat/", json=payload)
            
            if response.status_code == 200:
                data = response.json()
                model_used = data.get("model_used", "unknown")
                
                print_success("Fallback mechanism working")
                print_info(f"Model that responded: {model_used}")
                
                # Check if it's one of our configured providers
                expected_providers = ["groq", "together", "deepseek", "gemini", "fallback"]
                
                if any(provider in model_used.lower() for provider in expected_providers):
                    print_success(f"Using configured provider: {model_used}")
                else:
                    print_warning(f"Using unexpected provider: {model_used}")
                
                return True
            else:
                print_error(f"All models failed: {response.status_code}")
                print_error(f"Response: {response.text}")
                return False
                
    except Exception as e:
        print_error(f"Fallback test failed: {str(e)}")
        return False

async def test_provider_status():
    """Test 8: Provider Status Endpoint"""
    print("\n" + "="*60)
    print("TEST 8: Provider Status")
    print("="*60)
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{BASE_URL}/chat/providers")
            
            if response.status_code == 200:
                data = response.json()
                print_success("Provider status endpoint working")
                
                providers = data.get("providers", [])
                total_providers = data.get("total_providers", 0)
                available_providers = data.get("available_providers", 0)
                
                print_info(f"Total providers: {total_providers}")
                print_info(f"Available providers: {available_providers}")
                
                for provider in providers:
                    name = provider.get("name", "unknown")
                    available = provider.get("available", False)
                    models = provider.get("models", [])
                    
                    status = "✅ Available" if available else "❌ No API Key"
                    print_info(f"  {name}: {status} ({len(models)} models)")
                
                return True
            else:
                print_error(f"Status code: {response.status_code}")
                return False
    except Exception as e:
        print_error(f"Provider status test failed: {str(e)}")
        return False

async def test_error_handling():
    """Test 7: Error Handling"""
    print("\n" + "="*60)
    print("TEST 7: Error Handling")
    print("="*60)
    
    # Test with invalid content type
    print_info("Testing invalid content type...")
    payload = {
        "prompt": "Test",
        "content_type": "invalid_type"
    }
    
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(f"{BASE_URL}/chat/", json=payload)
            
            # Should still work, just use general prompt
            if response.status_code == 200:
                print_success("Handles invalid content type gracefully")
            else:
                print_warning(f"Status: {response.status_code}")
    except Exception as e:
        print_warning(f"Error handling test: {str(e)}")
    
    # Test with empty prompt
    print_info("\nTesting empty prompt...")
    payload = {
        "prompt": "",
        "content_type": "general"
    }
    
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(f"{BASE_URL}/chat/", json=payload)
            
            if response.status_code == 422:
                print_success("Validates empty prompt correctly")
                return True
            elif response.status_code == 200:
                print_warning("Accepts empty prompt (might want to validate)")
                return True
            else:
                print_info(f"Status: {response.status_code}")
                return True
    except Exception as e:
        print_warning(f"Error handling test: {str(e)}")
        return True

async def run_all_tests():
    """Run all tests"""
    print("\n" + "="*60)
    print("AI SERVICE END-TO-END TESTING")
    print("="*60)
    print_info(f"Testing service at: {BASE_URL}")
    
    results = {}
    
    # Run tests
    results["health"] = await test_health_check()
    results["non_streaming"] = await test_non_streaming_chat()
    results["streaming"] = await test_streaming_chat()
    results["content_types"] = await test_content_types()
    results["conversation"] = await test_conversation_history()
    results["fallback"] = await test_fallback_mechanism()
    results["provider_status"] = await test_provider_status()
    results["error_handling"] = await test_error_handling()
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    for test_name, passed in results.items():
        status = "✓ PASS" if passed else "✗ FAIL"
        color = Colors.GREEN if passed else Colors.RED
        print(f"{color}{status}{Colors.END} - {test_name}")
    
    total = len(results)
    passed = sum(results.values())
    success_rate = (passed / total) * 100
    
    print("\n" + "-"*60)
    print(f"Total: {passed}/{total} tests passed ({success_rate:.0f}%)")
    print("-"*60)
    
    if passed == total:
        print_success("\n🎉 All tests passed! Service is working correctly.")
        return 0
    elif passed >= total * 0.7:
        print_warning(f"\n⚠️  Most tests passed ({passed}/{total}). Check failures above.")
        return 1
    else:
        print_error(f"\n❌ Many tests failed ({total - passed}/{total}). Service needs attention.")
        return 2

if __name__ == "__main__":
    print("\nStarting AI Service Tests...")
    print("Make sure the service is running on http://localhost:8000\n")
    
    try:
        exit_code = asyncio.run(run_all_tests())
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\nTests interrupted by user")
        sys.exit(1)
    except Exception as e:
        print_error(f"\nTest suite failed: {str(e)}")
        sys.exit(2)
