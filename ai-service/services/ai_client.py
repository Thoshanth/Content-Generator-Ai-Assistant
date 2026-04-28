"""
Unified AI Client
Handles streaming and non-streaming requests to all 4 providers using OpenAI-compatible API.
"""

import httpx
import json
from typing import AsyncGenerator, Optional
from services.model_router import ProviderConfig


class RateLimitError(Exception):
    """Raised when provider returns 429 rate limit error."""
    pass


class ProviderError(Exception):
    """Raised when provider returns error or connection fails."""
    pass


async def stream_from_provider(
    provider: ProviderConfig,
    messages: list,
    temperature: float = 0.7,
    max_tokens: int = 2500
) -> AsyncGenerator[str, None]:
    """
    Stream from a single provider using OpenAI-compatible /chat/completions.
    Yields raw SSE lines as strings.
    Raises exception on HTTP error or connection failure (caller tries next provider).
    
    Args:
        provider: ProviderConfig with API credentials
        messages: List of message dicts with 'role' and 'content'
        temperature: Sampling temperature (0.0-1.0)
        max_tokens: Maximum tokens in response
    
    Yields:
        Raw SSE lines (e.g., "data: {...}")
    
    Raises:
        RateLimitError: If provider returns 429
        ProviderError: If provider returns error or connection fails
    """
    headers = {
        "Authorization": f"Bearer {provider.api_key}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": provider.model,
        "messages": messages,
        "stream": True,
        "max_tokens": max_tokens,
        "temperature": temperature,
        "top_p": 0.9,
    }

    try:
        async with httpx.AsyncClient(timeout=90.0) as client:
            async with client.stream(
                "POST",
                f"{provider.base_url}/chat/completions",
                headers=headers,
                json=payload
            ) as response:

                if response.status_code == 429:
                    raise RateLimitError(f"{provider.name} rate limited")
                
                if response.status_code != 200:
                    body = await response.aread()
                    raise ProviderError(
                        f"{provider.name} HTTP {response.status_code}: {body.decode()[:200]}"
                    )

                async for line in response.aiter_lines():
                    yield line
    
    except httpx.TimeoutException:
        raise ProviderError(f"{provider.name} request timed out")
    except httpx.ConnectError as e:
        raise ProviderError(f"{provider.name} connection failed: {str(e)}")
    except RateLimitError:
        raise
    except ProviderError:
        raise
    except Exception as e:
        raise ProviderError(f"{provider.name} unexpected error: {str(e)}")


async def get_response_from_provider(
    provider: ProviderConfig,
    messages: list,
    temperature: float = 0.7,
    max_tokens: int = 2500
) -> str:
    """
    Get non-streaming response from provider.
    Collects all streamed chunks and returns complete response.
    
    Args:
        provider: ProviderConfig with API credentials
        messages: List of message dicts
        temperature: Sampling temperature
        max_tokens: Maximum tokens in response
    
    Returns:
        Complete response text
    
    Raises:
        RateLimitError: If provider returns 429
        ProviderError: If provider returns error
    """
    full_content = ""
    
    async for line in stream_from_provider(provider, messages, temperature, max_tokens):
        if not line.startswith("data: "):
            continue
        
        data = line[6:].strip()
        
        if data == "[DONE]":
            break
        
        try:
            chunk = json.loads(data)
            delta = chunk["choices"][0]["delta"].get("content", "")
            if delta:
                full_content += delta
        except (json.JSONDecodeError, KeyError, IndexError):
            continue
    
    return full_content


async def generate_content(
    prompt: str,
    content_type: str,
    tone: str = "professional",
    length: str = "auto",
    language: str = "English",
    history: Optional[list] = None,
    uploaded_text: Optional[str] = None,
    custom_instructions: Optional[str] = None,
    user_id: str = "",
    regenerate: bool = False
) -> dict:
    """
    Generate AI content with non-streaming response and provider fallback.
    Returns complete response with metadata.
    
    Args:
        prompt: User's prompt
        content_type: Type of content to generate
        tone: Tone of response
        length: Desired length
        language: Output language
        history: Conversation history
        uploaded_text: Uploaded document text
        custom_instructions: Custom instructions
        user_id: User ID for tracking
        regenerate: If True, use higher temperature for variety
    
    Returns:
        Dict with keys: content, provider, model, word_count, char_count
    
    Raises:
        Exception: If all providers fail
    """
    from services.model_router import get_provider_chain
    from services.streaming import build_messages
    
    if history is None:
        history = []
    
    messages = build_messages(
        prompt, content_type, tone, length,
        language, history, uploaded_text, custom_instructions
    )
    
    temperature = 0.9 if regenerate else 0.7
    provider_chain = get_provider_chain(content_type)
    
    for provider in provider_chain:
        try:
            content = await get_response_from_provider(provider, messages, temperature)
            
            if content:
                return {
                    "content": content,
                    "provider": provider.name,
                    "model": provider.model,
                    "word_count": len(content.split()),
                    "char_count": len(content)
                }
        
        except RateLimitError:
            print(f"[{provider.name}] Rate limited — trying next provider")
            continue
        
        except ProviderError as e:
            print(f"[{provider.name}] Provider error: {e}")
            continue
        
        except Exception as e:
            print(f"[{provider.name}] Unexpected error: {e}")
            continue
    
    # All providers exhausted
    raise Exception("All AI providers are currently unavailable. Please try again in a moment.")
