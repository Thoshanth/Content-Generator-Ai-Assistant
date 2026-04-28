#!/usr/bin/env python3
"""
Comprehensive test suite for AI Service v5.0 features
Tests all new features: streaming, export, PDF, tone/length/language, etc.
"""

import asyncio
import httpx
import json
import sys
import os
from datetime import datetime

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

BASE_URL = "http://localhost:8000"

class Colors:
    """ANSI color codes for terminal output"""
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    END = '\033[0m'

def print_header(text):
    """Print a formatted header"""
    print(f"\n{Colors.CYAN}{'='*60}")
    print(f"{text}")
    print(f"{'='*60}{Colors.END}")

def print_success(text):
    """Print success message"""
    print(f"{Colors.GREEN}[PASS] {text}{Colors.END}")

def print_error(text):
    """Print error message"""
    print(f"{Colors.RED}[FAIL] {text}{Colors.END}")

def print_info(text):
    """Print info message"""
    print(f"{Colors.BLUE}[INFO] {text}{Colors.END}")

def print_test(text):
    """Print test name"""
    print(f"{Colors.YELLOW}[TEST] {text}{Colors.END}")

# ============================================================================
# TEST 1: Streaming Response
# ============================================================================

async def test_streaming_response():
    """Test streaming response with SSE"""
    print_test("Streaming Response (SSE)")
    
    payload = {
        "prompt": "Write a short professional email",
        "content_type": "email",
        "tone": "professional",
        "length": "short",
        "user_id": "test-streaming"
    }
    
    try:
        full_content = ""
        provider_info = None
        stats = None
        
        async with httpx.AsyncClient(timeout=90.0) as client:
            async with client.stream("POST", f"{BASE_URL}/chat/stream", json=payload) as response:
                
                if response.status_code != 200:
                    print_error(f"HTTP {response.status_code}")
                    return False
                
                print("  Streaming content: ", end="", flush=True)
                
                async for line in response.aiter_lines():
                    if not line.startswith("data: "):
                        continue
                    
                    try:
                        data = json.loads(line[6:])
                        
                        if "provider" in data:
                            provider_info = data
                            print(f"\n  Provider: {data.get('provider')} | Model: {data.get('model')}")
                        
                        elif "delta" in data:
                            delta = data.get("delta", "")
                            full_content += delta
                            print(".", end="", flush=True)
                        
                        elif "done" in data and data["done"]:
                            stats = data
                            print()
                    
                    except json.JSONDecodeError:
                        continue
        
        if full_content and provider_info and stats:
            print_success(f"Streaming works! Generated {stats.get('word_count', 0)} words")
            return True
        else:
            print_error("Incomplete streaming response")
            return False
            
    except Exception as e:
        print_error(f"Streaming failed: {str(e)}")
        return False

# ============================================================================
# TEST 2: Format Conversion (Export)
# ============================================================================

async def test_format_conversion():
    """Test format conversion: markdown -> plain text, HTML"""
    print_test("Format Conversion (Export)")
    
    markdown_content = """# Blog Post Title

## Introduction
This is a **bold** statement and this is *italic*.

## Main Content
- Point 1
- Point 2
- Point 3

[Link to example](https://example.com)
"""
    
    formats = ["plain_text", "html", "markdown"]
    results = {}
    
    for fmt in formats:
        try:
            payload = {
                "content": markdown_content,
                "format": fmt,
                "content_type": "blog_post"
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.post(f"{BASE_URL}/tools/export", json=payload)
                
                if response.status_code == 200:
                    data = response.json()
                    results[fmt] = {
                        "success": True,
                        "word_count": data.get("word_count", 0),
                        "char_count": data.get("char_count", 0)
                    }
                else:
                    results[fmt] = {"success": False, "error": f"HTTP {response.status_code}"}
        
        except Exception as e:
            results[fmt] = {"success": False, "error": str(e)}
    
    # Check results
    successful = sum(1 for r in results.values() if r.get("success"))
    
    if successful == len(formats):
        print_success(f"All {len(formats)} formats converted successfully")
        for fmt, result in results.items():
            print(f"    {fmt}: {result.get('word_count', 0)} words")
        return True
    else:
        print_error(f"Only {successful}/{len(formats)} formats converted")
        for fmt, result in results.items():
            if not result.get("success"):
                print(f"    {fmt}: {result.get('error')}")
        return False

# ============================================================================
# TEST 3: PDF Export
# ============================================================================

async def test_pdf_export():
    """Test PDF export for resume and cover letter"""
    print_test("PDF Export")
    
    test_cases = [
        {
            "name": "Resume",
            "content_type": "resume",
            "content": """# John Doe

## Experience
**Software Engineer** at Tech Company (2020-2024)
- Developed web applications
- Led team of 3 developers

## Skills
- Python, JavaScript, React
- AWS, Docker, Kubernetes
"""
        },
        {
            "name": "Cover Letter",
            "content_type": "cover_letter",
            "content": """Dear Hiring Manager,

I am writing to express my interest in the Software Engineer position.

With 5 years of experience in full-stack development, I am confident in my ability to contribute to your team.

Sincerely,
John Doe
"""
        }
    ]
    
    results = {}
    
    for test_case in test_cases:
        try:
            payload = {
                "content": test_case["content"],
                "content_type": test_case["content_type"],
                "candidate_name": "John Doe"
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.post(f"{BASE_URL}/tools/export-pdf", json=payload)
                
                if response.status_code == 200:
                    pdf_bytes = response.content
                    results[test_case["name"]] = {
                        "success": True,
                        "size": len(pdf_bytes)
                    }
                else:
                    results[test_case["name"]] = {"success": False, "error": f"HTTP {response.status_code}"}
        
        except Exception as e:
            results[test_case["name"]] = {"success": False, "error": str(e)}
    
    # Check results
    successful = sum(1 for r in results.values() if r.get("success"))
    
    if successful == len(test_cases):
        print_success(f"PDF export works for {len(test_cases)} content types")
        for name, result in results.items():
            print(f"    {name}: {result.get('size', 0)} bytes")
        return True
    else:
        print_error(f"Only {successful}/{len(test_cases)} PDFs generated")
        for name, result in results.items():
            if not result.get("success"):
                print(f"    {name}: {result.get('error')}")
        return False

# ============================================================================
# TEST 4: Tone Customization
# ============================================================================

async def test_tone_customization():
    """Test different tone options"""
    print_test("Tone Customization")
    
    tones = ["professional", "casual", "formal", "friendly"]
    results = {}
    
    for tone in tones:
        try:
            payload = {
                "prompt": "Write a short greeting",
                "content_type": "email",
                "tone": tone,
                "length": "short",
                "user_id": f"test-tone-{tone}"
            }
            
            full_content = ""
            
            async with httpx.AsyncClient(timeout=60.0) as client:
                async with client.stream("POST", f"{BASE_URL}/chat/stream", json=payload) as response:
                    
                    if response.status_code != 200:
                        results[tone] = {"success": False, "error": f"HTTP {response.status_code}"}
                        continue
                    
                    async for line in response.aiter_lines():
                        if not line.startswith("data: "):
                            continue
                        
                        try:
                            data = json.loads(line[6:])
                            
                            if "delta" in data:
                                full_content += data.get("delta", "")
                            elif "done" in data and data["done"]:
                                results[tone] = {
                                    "success": True,
                                    "word_count": data.get("word_count", 0)
                                }
                        
                        except json.JSONDecodeError:
                            continue
        
        except Exception as e:
            results[tone] = {"success": False, "error": str(e)}
    
    # Check results
    successful = sum(1 for r in results.values() if r.get("success"))
    
    if successful == len(tones):
        print_success(f"All {len(tones)} tones work correctly")
        for tone, result in results.items():
            print(f"    {tone}: {result.get('word_count', 0)} words")
        return True
    else:
        print_error(f"Only {successful}/{len(tones)} tones work")
        for tone, result in results.items():
            if not result.get("success"):
                print(f"    {tone}: {result.get('error')}")
        return False

# ============================================================================
# TEST 5: Length Customization
# ============================================================================

async def test_length_customization():
    """Test different length options"""
    print_test("Length Customization")
    
    lengths = ["short", "medium", "long"]
    results = {}
    
    for length in lengths:
        try:
            payload = {
                "prompt": "Write about artificial intelligence",
                "content_type": "blog_post",
                "tone": "professional",
                "length": length,
                "user_id": f"test-length-{length}"
            }
            
            full_content = ""
            
            async with httpx.AsyncClient(timeout=90.0) as client:
                async with client.stream("POST", f"{BASE_URL}/chat/stream", json=payload) as response:
                    
                    if response.status_code != 200:
                        results[length] = {"success": False, "error": f"HTTP {response.status_code}"}
                        continue
                    
                    async for line in response.aiter_lines():
                        if not line.startswith("data: "):
                            continue
                        
                        try:
                            data = json.loads(line[6:])
                            
                            if "delta" in data:
                                full_content += data.get("delta", "")
                            elif "done" in data and data["done"]:
                                results[length] = {
                                    "success": True,
                                    "word_count": data.get("word_count", 0)
                                }
                        
                        except json.JSONDecodeError:
                            continue
        
        except Exception as e:
            results[length] = {"success": False, "error": str(e)}
    
    # Check results and verify length progression
    successful = sum(1 for r in results.values() if r.get("success"))
    
    if successful == len(lengths):
        word_counts = [results[l].get("word_count", 0) for l in lengths]
        print_success(f"All {len(lengths)} lengths work correctly")
        for length, result in results.items():
            print(f"    {length}: {result.get('word_count', 0)} words")
        
        # Check if lengths are in expected order
        if word_counts[0] <= word_counts[1] <= word_counts[2]:
            print_success("Length progression is correct (short < medium < long)")
        else:
            print_info("Length progression may vary based on content")
        
        return True
    else:
        print_error(f"Only {successful}/{len(lengths)} lengths work")
        for length, result in results.items():
            if not result.get("success"):
                print(f"    {length}: {result.get('error')}")
        return False

# ============================================================================
# TEST 6: Language Support
# ============================================================================

async def test_language_support():
    """Test different language options"""
    print_test("Language Support")
    
    languages = ["English", "Spanish", "French", "German"]
    results = {}
    
    for language in languages:
        try:
            payload = {
                "prompt": "Say hello",
                "content_type": "general",
                "language": language,
                "user_id": f"test-lang-{language}"
            }
            
            full_content = ""
            
            async with httpx.AsyncClient(timeout=60.0) as client:
                async with client.stream("POST", f"{BASE_URL}/chat/stream", json=payload) as response:
                    
                    if response.status_code != 200:
                        results[language] = {"success": False, "error": f"HTTP {response.status_code}"}
                        continue
                    
                    async for line in response.aiter_lines():
                        if not line.startswith("data: "):
                            continue
                        
                        try:
                            data = json.loads(line[6:])
                            
                            if "delta" in data:
                                full_content += data.get("delta", "")
                            elif "done" in data and data["done"]:
                                results[language] = {
                                    "success": True,
                                    "word_count": data.get("word_count", 0)
                                }
                        
                        except json.JSONDecodeError:
                            continue
        
        except Exception as e:
            results[language] = {"success": False, "error": str(e)}
    
    # Check results
    successful = sum(1 for r in results.values() if r.get("success"))
    
    if successful == len(languages):
        print_success(f"All {len(languages)} languages work correctly")
        for language, result in results.items():
            print(f"    {language}: {result.get('word_count', 0)} words")
        return True
    else:
        print_error(f"Only {successful}/{len(languages)} languages work")
        for language, result in results.items():
            if not result.get("success"):
                print(f"    {language}: {result.get('error')}")
        return False

# ============================================================================
# TEST 7: Content Type Routing
# ============================================================================

async def test_content_type_routing():
    """Test different content types"""
    print_test("Content Type Routing")
    
    content_types = [
        ("email", "Write a professional email"),
        ("blog_post", "Write a blog post about technology"),
        ("resume", "Write a resume for a software engineer"),
        ("social_media", "Write a social media post"),
        ("code_explainer", "Explain what a for loop is")
    ]
    
    results = {}
    
    for content_type, prompt in content_types:
        try:
            payload = {
                "prompt": prompt,
                "content_type": content_type,
                "user_id": f"test-type-{content_type}"
            }
            
            full_content = ""
            provider_info = None
            
            async with httpx.AsyncClient(timeout=60.0) as client:
                async with client.stream("POST", f"{BASE_URL}/chat/stream", json=payload) as response:
                    
                    if response.status_code != 200:
                        results[content_type] = {"success": False, "error": f"HTTP {response.status_code}"}
                        continue
                    
                    async for line in response.aiter_lines():
                        if not line.startswith("data: "):
                            continue
                        
                        try:
                            data = json.loads(line[6:])
                            
                            if "provider" in data:
                                provider_info = data.get("provider")
                            elif "delta" in data:
                                full_content += data.get("delta", "")
                            elif "done" in data and data["done"]:
                                results[content_type] = {
                                    "success": True,
                                    "provider": provider_info,
                                    "word_count": data.get("word_count", 0)
                                }
                        
                        except json.JSONDecodeError:
                            continue
        
        except Exception as e:
            results[content_type] = {"success": False, "error": str(e)}
    
    # Check results
    successful = sum(1 for r in results.values() if r.get("success"))
    
    if successful == len(content_types):
        print_success(f"All {len(content_types)} content types work correctly")
        for content_type, result in results.items():
            print(f"    {content_type}: {result.get('provider', 'unknown')} ({result.get('word_count', 0)} words)")
        return True
    else:
        print_error(f"Only {successful}/{len(content_types)} content types work")
        for content_type, result in results.items():
            if not result.get("success"):
                print(f"    {content_type}: {result.get('error')}")
        return False

# ============================================================================
# TEST 8: Generate Endpoints
# ============================================================================

async def test_generate_endpoints():
    """Test convenience generate endpoints"""
    print_test("Generate Endpoints")
    
    endpoints = [
        "/generate/email",
        "/generate/blog-post",
        "/generate/resume",
        "/generate/social-media"
    ]
    
    results = {}
    
    for endpoint in endpoints:
        try:
            payload = {
                "prompt": "Generate content",
                "tone": "professional",
                "user_id": f"test-endpoint-{endpoint}"
            }
            
            async with httpx.AsyncClient(timeout=60.0) as client:
                async with client.stream("POST", f"{BASE_URL}{endpoint}", json=payload) as response:
                    
                    if response.status_code == 200:
                        # Just verify we get streaming response
                        got_data = False
                        async for line in response.aiter_lines():
                            if line.startswith("data: "):
                                got_data = True
                                break
                        
                        results[endpoint] = {"success": got_data}
                    else:
                        results[endpoint] = {"success": False, "error": f"HTTP {response.status_code}"}
        
        except Exception as e:
            results[endpoint] = {"success": False, "error": str(e)}
    
    # Check results
    successful = sum(1 for r in results.values() if r.get("success"))
    
    if successful == len(endpoints):
        print_success(f"All {len(endpoints)} generate endpoints work")
        for endpoint in endpoints:
            print(f"    {endpoint}")
        return True
    else:
        print_error(f"Only {successful}/{len(endpoints)} endpoints work")
        for endpoint, result in results.items():
            if not result.get("success"):
                print(f"    {endpoint}: {result.get('error')}")
        return False

# ============================================================================
# TEST 9: Provider Status
# ============================================================================

async def test_provider_status():
    """Test provider status endpoint"""
    print_test("Provider Status")
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{BASE_URL}/chat/providers")
            
            if response.status_code == 200:
                data = response.json()
                providers = data.get("providers", [])
                available = data.get("available_providers", 0)
                total = data.get("total_providers", 0)
                
                if available > 0:
                    print_success(f"Provider status: {available}/{total} available")
                    for provider in providers:
                        status = "[OK]" if provider.get("available") else "[NO KEY]"
                        print(f"    {status} {provider.get('name')}: {provider.get('model')}")
                    return True
                else:
                    print_error("No providers available")
                    return False
            else:
                print_error(f"HTTP {response.status_code}")
                return False
    
    except Exception as e:
        print_error(f"Failed to get provider status: {str(e)}")
        return False

# ============================================================================
# MAIN TEST RUNNER
# ============================================================================

async def main():
    """Run all feature tests"""
    print_header("AI Service v5.0 - Feature Test Suite")
    
    tests = [
        ("Streaming Response", test_streaming_response),
        ("Format Conversion", test_format_conversion),
        ("PDF Export", test_pdf_export),
        ("Tone Customization", test_tone_customization),
        ("Length Customization", test_length_customization),
        ("Language Support", test_language_support),
        ("Content Type Routing", test_content_type_routing),
        ("Generate Endpoints", test_generate_endpoints),
        ("Provider Status", test_provider_status),
    ]
    
    results = {}
    
    # Check provider status first
    print_info("Checking provider status...")
    provider_ok = await test_provider_status()
    
    if not provider_ok:
        print_error("No providers available. Please configure API keys in .env")
        return
    
    print()
    
    # Run all tests
    for test_name, test_func in tests:
        try:
            result = await test_func()
            results[test_name] = result
        except Exception as e:
            print_error(f"Test crashed: {str(e)}")
            results[test_name] = False
    
    # Summary
    print_header("Test Summary")
    
    passed = sum(1 for r in results.values() if r)
    total = len(results)
    
    print(f"Passed: {passed}/{total}")
    print()
    
    for test_name, result in results.items():
        status = f"{Colors.GREEN}[PASS]{Colors.END}" if result else f"{Colors.RED}[FAIL]{Colors.END}"
        print(f"  {status} - {test_name}")
    
    print()
    
    if passed == total:
        print_success(f"All {total} tests passed!")
    elif passed > 0:
        print_info(f"{passed}/{total} tests passed")
    else:
        print_error("All tests failed")
    
    print()

if __name__ == "__main__":
    print("AI Service v5.0 - Feature Test Suite")
    print("Make sure the AI service is running on http://localhost:8000\n")
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n⚠️  Tests interrupted by user")
    except Exception as e:
        print(f"\n❌ Tests failed: {str(e)}")
