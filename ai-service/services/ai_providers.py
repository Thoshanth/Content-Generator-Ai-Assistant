import httpx
import os
import asyncio
import json
from typing import List, Dict, Tuple, AsyncGenerator, Optional
from dotenv import load_dotenv
from prompts.templates import get_system_prompt

load_dotenv()

# API Keys
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")

# Provider configurations with intelligent routing
PROVIDERS = [
    {
        "name": "groq",
        "api_key": GROQ_API_KEY,
        "base_url": "https://api.groq.com/openai/v1/chat/completions",
        "models": [
            "llama-3.1-8b-instant",      # Fast for simple queries
            "mixtral-8x7b-32768",        # Medium complexity
            "gemma2-9b-it"               # Backup
        ],
        "headers_func": lambda key: {
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json"
        },
        "strengths": ["speed", "simple_queries", "real_time"],
        "complexity_range": (1, 3),  # Handles complexity 1-3
        "max_tokens_efficient": 500   # Most efficient under 500 tokens
    },
    {
        "name": "together",
        "api_key": TOGETHER_API_KEY,
        "base_url": "https://api.together.xyz/v1/chat/completions",
        "models": [
            "meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo",   # Medium queries
            "meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo",  # Complex queries
            "mistralai/Mixtral-8x7B-Instruct-v0.1",          # Alternative
            "NousResearch/Nous-Hermes-2-Mixtral-8x7B-DPO"    # Backup
        ],
        "headers_func": lambda key: {
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json"
        },
        "strengths": ["medium_complexity", "diverse_models", "balanced"],
        "complexity_range": (2, 4),  # Handles complexity 2-4
        "max_tokens_efficient": 1500  # Good for medium-length content
    },
    {
        "name": "deepseek",
        "api_key": DEEPSEEK_API_KEY,
        "base_url": "https://api.deepseek.com/chat/completions",
        "models": [
            "deepseek-chat",    # General complex queries
            "deepseek-coder"    # Technical/coding content
        ],
        "headers_func": lambda key: {
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json"
        },
        "strengths": ["technical_content", "coding", "complex_reasoning"],
        "complexity_range": (3, 5),  # Handles complexity 3-5
        "max_tokens_efficient": 2000  # Good for detailed content
    },
    {
        "name": "gemini",
        "api_key": GEMINI_API_KEY,
        "base_url": "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent",
        "models": [
            "gemini-1.5-flash",  # Fast for complex queries
            "gemini-1.5-pro"     # Most powerful for very complex tasks
        ],
        "headers_func": lambda key: {
            "Content-Type": "application/json"
        },
        "special_handling": True,
        "strengths": ["complex_reasoning", "long_content", "analysis"],
        "complexity_range": (4, 5),  # Handles complexity 4-5
        "max_tokens_efficient": 3000  # Best for long-form content
    }
]

def analyze_query_complexity(prompt: str, content_type: str, conversation_history: List[Dict[str, str]] = None) -> int:
    """
    Analyze query complexity to determine optimal provider.
    Returns complexity score 1-5:
    1 = Very simple (short responses, basic queries)
    2 = Simple (standard emails, basic content)
    3 = Medium (detailed content, some reasoning)
    4 = Complex (long-form content, analysis)
    5 = Very complex (deep reasoning, extensive content)
    """
    complexity = 1
    
    # Base complexity by content type
    content_complexity = {
        "general": 1,
        "email": 2,
        "social": 1,
        "blog": 4,
        "article": 4,
        "technical": 5,
        "analysis": 5,
        "code": 4
    }
    
    complexity = content_complexity.get(content_type, 2)
    
    # Adjust based on prompt length
    prompt_length = len(prompt.split())
    if prompt_length > 50:
        complexity += 1
    elif prompt_length > 100:
        complexity += 2
    
    # Adjust based on conversation history
    if conversation_history and len(conversation_history) > 3:
        complexity += 1
    
    # Look for complexity indicators in prompt
    complex_indicators = [
        "analyze", "compare", "detailed", "comprehensive", "in-depth",
        "explain", "research", "technical", "professional", "strategy",
        "plan", "proposal", "report", "documentation", "specification"
    ]
    
    simple_indicators = [
        "short", "brief", "quick", "simple", "basic", "hello", "hi",
        "yes", "no", "thanks", "ok", "sure"
    ]
    
    prompt_lower = prompt.lower()
    
    # Count complex indicators
    complex_count = sum(1 for indicator in complex_indicators if indicator in prompt_lower)
    simple_count = sum(1 for indicator in simple_indicators if indicator in prompt_lower)
    
    if complex_count > 2:
        complexity += 1
    elif simple_count > 0:
        complexity = max(1, complexity - 1)
    
    # Ensure complexity is within bounds
    return max(1, min(5, complexity))

def get_optimal_providers_for_complexity(complexity: int) -> List[Dict]:
    """
    Get providers ordered by suitability for the given complexity level.
    """
    suitable_providers = []
    
    for provider in PROVIDERS:
        if not provider["api_key"]:
            continue
            
        min_complexity, max_complexity = provider["complexity_range"]
        
        # Calculate suitability score
        if min_complexity <= complexity <= max_complexity:
            # Perfect match
            suitability = 10
        elif complexity < min_complexity:
            # Provider is overkill but can handle it
            suitability = 7 - (min_complexity - complexity)
        elif complexity > max_complexity:
            # Provider might struggle but could work
            suitability = 5 - (complexity - max_complexity)
        else:
            suitability = 0
        
        if suitability > 0:
            suitable_providers.append({
                "provider": provider,
                "suitability": suitability
            })
    
    # Sort by suitability (highest first)
    suitable_providers.sort(key=lambda x: x["suitability"], reverse=True)
    
    return [item["provider"] for item in suitable_providers]

def generate_fallback_content(prompt: str, content_type: str) -> str:
    """
    Generate a helpful fallback response when all AI models fail.
    """
    fallback_responses = {
        "email": f"""Subject: Re: {prompt[:50]}...

I apologize, but I'm currently experiencing technical difficulties with my AI models. 

Your request was: "{prompt}"

Please try again in a few minutes, or consider the following:
- Check if your request is clear and specific
- Try breaking complex requests into smaller parts
- Contact support if the issue persists

Best regards,
AI Content Generator

---
Note: This is a fallback response due to temporary service limitations.""",

        "blog": f"""# Content Generation Temporarily Unavailable

I apologize, but I'm currently unable to generate the requested blog content due to technical limitations with my AI models.

**Your request was:** {prompt}

**What you can do:**
- Try again in a few minutes
- Simplify your request
- Check back later when service is restored

**Alternative approach:**
Consider outlining your blog post with these sections:
1. Introduction
2. Main points (3-5 key ideas)
3. Supporting details and examples
4. Conclusion and call-to-action

---
*This is a temporary fallback response. Normal AI generation will resume shortly.*""",

        "social": f"""🚫 AI Service Temporarily Unavailable

Sorry, I can't generate social media content right now due to technical issues.

Your request: "{prompt[:100]}..."

💡 Quick tips while you wait:
- Keep posts engaging and authentic
- Use relevant hashtags
- Include a clear call-to-action
- Consider your audience's interests

Try again in a few minutes! 🔄

#TechnicalDifficulties #ComingSoon""",

        "general": f"""I apologize, but I'm currently experiencing technical difficulties and cannot process your request properly.

Your message: "{prompt}"

This is a temporary issue with my AI models. Please try again in a few minutes.

If the problem persists, you may want to:
- Simplify your request
- Try a different approach to your question
- Contact support for assistance

Thank you for your patience!"""
    }
    
    return fallback_responses.get(content_type, fallback_responses["general"])

async def call_gemini_api(
    model: str,
    prompt: str,
    content_type: str,
    conversation_history: List[Dict[str, str]] = None,
    api_key: str = None
) -> Tuple[str, int]:
    """
    Call Gemini API with its specific format.
    """
    system_prompt = get_system_prompt(content_type)
    
    # Combine system prompt with user prompt for Gemini
    full_prompt = f"{system_prompt}\n\nUser: {prompt}"
    
    # Add conversation history if available
    if conversation_history:
        context = "\n".join([f"{msg['role']}: {msg['content']}" for msg in conversation_history[-3:]])
        full_prompt = f"{system_prompt}\n\nConversation context:\n{context}\n\nUser: {prompt}"
    
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
    
    payload = {
        "contents": [{
            "parts": [{
                "text": full_prompt
            }]
        }],
        "generationConfig": {
            "temperature": 0.7,
            "maxOutputTokens": 2000,
        }
    }
    
    headers = {"Content-Type": "application/json"}
    
    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.post(url, json=payload, headers=headers)
        
        if response.status_code != 200:
            error_detail = response.text
            raise Exception(f"Gemini API error: {response.status_code} - {error_detail}")
        
        data = response.json()
        
        if "candidates" not in data or not data["candidates"]:
            raise Exception("No content generated by Gemini")
        
        content = data["candidates"][0]["content"]["parts"][0]["text"]
        
        # Estimate tokens (rough approximation)
        tokens_used = len(content.split()) + len(full_prompt.split())
        
        return content, tokens_used

async def call_standard_api(
    provider: Dict,
    model: str,
    prompt: str,
    content_type: str,
    conversation_history: List[Dict[str, str]] = None,
    stream: bool = False,
    retry_count: int = 0
) -> Tuple[str, int]:
    """
    Call standard OpenAI-compatible API (Groq, Together, DeepSeek).
    """
    system_prompt = get_system_prompt(content_type)
    
    messages = [{"role": "system", "content": system_prompt}]
    
    # Add conversation history (last 5 messages for context)
    if conversation_history:
        messages.extend(conversation_history[-5:])
    
    # Add current user prompt
    messages.append({"role": "user", "content": prompt})
    
    headers = provider["headers_func"](provider["api_key"])
    
    payload = {
        "model": model,
        "messages": messages,
        "stream": stream,
        "temperature": 0.7,
        "max_tokens": 2000
    }
    
    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                provider["base_url"],
                json=payload,
                headers=headers
            )
            
            if response.status_code == 429 and retry_count < 2:
                # Rate limited, wait and retry
                print(f"Rate limited on {provider['name']}/{model}, retrying in 2 seconds...")
                await asyncio.sleep(2)
                return await call_standard_api(provider, model, prompt, content_type, conversation_history, stream, retry_count + 1)
            
            if response.status_code != 200:
                error_detail = response.text
                raise Exception(f"{provider['name']} API error: {response.status_code} - {error_detail}")
            
            data = response.json()
            content = data["choices"][0]["message"]["content"]
            tokens_used = data.get("usage", {}).get("total_tokens", 0)
            
            return content, tokens_used
    except httpx.TimeoutException:
        raise Exception(f"Request timeout for {provider['name']}/{model}")
    except Exception as e:
        raise Exception(f"Error calling {provider['name']}/{model}: {str(e)}")

async def call_provider_stream(
    provider: Dict,
    model: str,
    prompt: str,
    content_type: str,
    conversation_history: List[Dict[str, str]] = None
) -> AsyncGenerator[Dict, None]:
    """
    Call provider API with streaming enabled.
    """
    if provider.get("special_handling"):
        # Gemini doesn't support streaming in the same way
        try:
            content, tokens = await call_gemini_api(model, prompt, content_type, conversation_history, provider["api_key"])
            # Simulate streaming by yielding chunks
            words = content.split()
            for i in range(0, len(words), 5):  # Yield 5 words at a time
                chunk = " ".join(words[i:i+5])
                if i + 5 < len(words):
                    chunk += " "
                yield {"content": chunk, "model": f"{provider['name']}/{model}"}
                await asyncio.sleep(0.1)  # Small delay to simulate streaming
        except Exception as e:
            raise Exception(f"Gemini streaming error: {str(e)}")
        return
    
    system_prompt = get_system_prompt(content_type)
    
    messages = [{"role": "system", "content": system_prompt}]
    
    if conversation_history:
        messages.extend(conversation_history[-5:])
    
    messages.append({"role": "user", "content": prompt})
    
    headers = provider["headers_func"](provider["api_key"])
    
    payload = {
        "model": model,
        "messages": messages,
        "stream": True,
        "temperature": 0.7,
        "max_tokens": 2000
    }
    
    async with httpx.AsyncClient(timeout=120.0) as client:
        async with client.stream(
            "POST",
            provider["base_url"],
            json=payload,
            headers=headers
        ) as response:
            if response.status_code != 200:
                error_text = await response.aread()
                raise Exception(f"{provider['name']} API error: {response.status_code} - {error_text.decode()}")
            
            async for line in response.aiter_lines():
                if line.startswith("data: "):
                    data_str = line[6:]  # Remove "data: " prefix
                    
                    if data_str.strip() == "[DONE]":
                        break
                    
                    try:
                        data = json.loads(data_str)
                        
                        if "choices" in data and len(data["choices"]) > 0:
                            delta = data["choices"][0].get("delta", {})
                            content = delta.get("content", "")
                            
                            if content:
                                yield {"content": content, "model": f"{provider['name']}/{model}"}
                    except json.JSONDecodeError:
                        continue

async def generate_content(
    prompt: str,
    content_type: str,
    conversation_history: List[Dict[str, str]] = None
) -> Tuple[str, str, int]:
    """
    Generate content with intelligent provider routing based on query complexity.
    Returns (content, model_used, tokens_used).
    """
    # Analyze query complexity
    complexity = analyze_query_complexity(prompt, content_type, conversation_history)
    
    # Get optimal providers for this complexity
    optimal_providers = get_optimal_providers_for_complexity(complexity)
    
    print(f"🧠 Query complexity: {complexity}/5")
    print(f"🎯 Optimal provider order: {[p['name'] for p in optimal_providers]}")
    
    last_error = None
    attempted_combinations = []
    
    for provider in optimal_providers:
        for model in provider["models"]:
            combination = f"{provider['name']}/{model}"
            attempted_combinations.append(combination)
            
            try:
                if provider.get("special_handling"):
                    # Handle Gemini API
                    content, tokens_used = await call_gemini_api(
                        model=model,
                        prompt=prompt,
                        content_type=content_type,
                        conversation_history=conversation_history,
                        api_key=provider["api_key"]
                    )
                else:
                    # Handle standard OpenAI-compatible APIs
                    content, tokens_used = await call_standard_api(
                        provider=provider,
                        model=model,
                        prompt=prompt,
                        content_type=content_type,
                        conversation_history=conversation_history,
                        stream=False
                    )
                
                print(f"✅ Successfully used: {combination} (complexity {complexity})")
                return content, combination, tokens_used
                
            except Exception as e:
                last_error = e
                error_msg = str(e)
                
                # Log specific errors
                if "404" in error_msg:
                    print(f"⚠️  {combination} not available (404)")
                elif "429" in error_msg:
                    print(f"⚠️  {combination} rate limited, trying next...")
                elif "401" in error_msg or "403" in error_msg:
                    print(f"❌ Authentication error for {combination}")
                else:
                    print(f"⚠️  {combination} failed: {error_msg[:100]}")
                continue
    
    # All optimal providers failed - try remaining providers as fallback
    remaining_providers = [p for p in PROVIDERS if p not in optimal_providers and p["api_key"]]
    
    if remaining_providers:
        print(f"🔄 Trying fallback providers: {[p['name'] for p in remaining_providers]}")
        
        for provider in remaining_providers:
            for model in provider["models"]:
                combination = f"{provider['name']}/{model}"
                attempted_combinations.append(combination)
                
                try:
                    if provider.get("special_handling"):
                        content, tokens_used = await call_gemini_api(
                            model=model,
                            prompt=prompt,
                            content_type=content_type,
                            conversation_history=conversation_history,
                            api_key=provider["api_key"]
                        )
                    else:
                        content, tokens_used = await call_standard_api(
                            provider=provider,
                            model=model,
                            prompt=prompt,
                            content_type=content_type,
                            conversation_history=conversation_history,
                            stream=False
                        )
                    
                    print(f"✅ Fallback success: {combination}")
                    return content, combination, tokens_used
                    
                except Exception as e:
                    last_error = e
                    print(f"⚠️  Fallback {combination} failed")
                    continue
    
    # All providers/models failed - provide a helpful fallback response
    print(f"❌ All {len(attempted_combinations)} provider/model combinations failed")
    
    # Generate a helpful fallback response based on content type
    fallback_content = generate_fallback_content(prompt, content_type)
    return fallback_content, "fallback", 0

async def generate_content_stream(
    prompt: str,
    content_type: str,
    conversation_history: List[Dict[str, str]] = None
) -> AsyncGenerator[Dict, None]:
    """
    Generate content with streaming and intelligent provider routing.
    Yields chunks as they arrive.
    """
    # Analyze query complexity
    complexity = analyze_query_complexity(prompt, content_type, conversation_history)
    
    # Get optimal providers for this complexity
    optimal_providers = get_optimal_providers_for_complexity(complexity)
    
    print(f"🧠 Streaming complexity: {complexity}/5")
    print(f"🎯 Optimal provider order: {[p['name'] for p in optimal_providers]}")
    
    last_error = None
    attempted_combinations = []
    
    for provider in optimal_providers:
        for model in provider["models"]:
            combination = f"{provider['name']}/{model}"
            attempted_combinations.append(combination)
            
            try:
                print(f"🔄 Trying streaming with: {combination}")
                async for chunk in call_provider_stream(
                    provider=provider,
                    model=model,
                    prompt=prompt,
                    content_type=content_type,
                    conversation_history=conversation_history
                ):
                    yield chunk
                print(f"✅ Streaming completed with: {combination}")
                return  # Success, exit
                
            except Exception as e:
                last_error = e
                error_msg = str(e)
                
                # Log specific errors
                if "404" in error_msg:
                    print(f"⚠️  {combination} not available for streaming")
                elif "429" in error_msg:
                    print(f"⚠️  {combination} rate limited for streaming, trying next...")
                else:
                    print(f"⚠️  Streaming failed for {combination}: {error_msg[:100]}")
                continue
    
    # Try remaining providers as fallback
    remaining_providers = [p for p in PROVIDERS if p not in optimal_providers and p["api_key"]]
    
    if remaining_providers:
        print(f"🔄 Trying fallback providers for streaming: {[p['name'] for p in remaining_providers]}")
        
        for provider in remaining_providers:
            for model in provider["models"]:
                combination = f"{provider['name']}/{model}"
                attempted_combinations.append(combination)
                
                try:
                    print(f"🔄 Fallback streaming with: {combination}")
                    async for chunk in call_provider_stream(
                        provider=provider,
                        model=model,
                        prompt=prompt,
                        content_type=content_type,
                        conversation_history=conversation_history
                    ):
                        yield chunk
                    print(f"✅ Fallback streaming completed with: {combination}")
                    return
                    
                except Exception as e:
                    print(f"⚠️  Fallback streaming failed for {combination}")
                    continue
    
    # All providers failed
    error_summary = f"Streaming failed for all {len(attempted_combinations)} combinations. Last error: {str(last_error)}"
    yield {"error": error_summary}

def get_available_providers() -> List[Dict]:
    """
    Get list of available providers with their status.
    """
    status = []
    for provider in PROVIDERS:
        status.append({
            "name": provider["name"],
            "available": bool(provider["api_key"]),
            "models": provider["models"]
        })
    return status