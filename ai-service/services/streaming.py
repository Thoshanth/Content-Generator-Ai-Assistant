"""
Streaming Orchestrator
Orchestrates provider chain, fallback logic, and SSE output.
"""

import json
from typing import AsyncGenerator, Optional, List
from services.model_router import get_provider_chain
from services.ai_client import stream_from_provider, RateLimitError, ProviderError
from prompts.templates import get_system_prompt
from prompts.tone_modifiers import build_modifiers


def build_messages(
    prompt: str,
    content_type: str,
    tone: str = "professional",
    length: str = "auto",
    language: str = "English",
    history: Optional[List[dict]] = None,
    uploaded_text: Optional[str] = None,
    custom_instructions: Optional[str] = None
) -> list:
    """
    Build complete message list for API call.
    Includes system prompt, tone modifiers, conversation history, and user prompt.
    
    Args:
        prompt: User's current prompt
        content_type: Type of content (email, blog_post, etc.)
        tone: Tone modifier (professional, casual, etc.)
        length: Length preference (short, medium, long, auto)
        language: Output language
        history: Previous conversation messages
        uploaded_text: Text from uploaded document
        custom_instructions: Additional user instructions
    
    Returns:
        List of message dicts ready for API call
    """
    system = get_system_prompt(content_type)
    modifiers = build_modifiers(tone, length, language)
    full_system = f"{system}\n\n---\n{modifiers}"

    if custom_instructions:
        full_system += f"\n\nADDITIONAL INSTRUCTIONS:\n{custom_instructions}"

    messages = [{"role": "system", "content": full_system}]

    # Keep last 5 exchanges (10 messages) as context window
    if history:
        recent = history[-10:] if len(history) > 10 else history
        for msg in recent:
            messages.append({"role": msg.get("role", "user"), "content": msg.get("content", "")})

    # Build user content
    user_content = prompt
    if uploaded_text:
        user_content = (
            f"Document provided by user:\n\n"
            f"--- DOCUMENT START ---\n{uploaded_text[:12000]}\n--- DOCUMENT END ---\n\n"
            f"User request: {prompt}"
        )

    messages.append({"role": "user", "content": user_content})
    return messages


async def stream_response(
    prompt: str,
    content_type: str,
    tone: str = "professional",
    length: str = "auto",
    language: str = "English",
    history: Optional[List[dict]] = None,
    uploaded_text: Optional[str] = None,
    custom_instructions: Optional[str] = None,
    user_id: str = "",
    regenerate: bool = False
) -> AsyncGenerator[str, None]:
    """
    Stream AI response with intelligent provider fallback.
    Yields SSE-formatted JSON events.
    
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
    
    Yields:
        SSE-formatted JSON strings (e.g., "data: {...}\n\n")
    """
    if history is None:
        history = []

    messages = build_messages(
        prompt, content_type, tone, length,
        language, history, uploaded_text, custom_instructions
    )

    temperature = 0.9 if regenerate else 0.7
    provider_chain = get_provider_chain(content_type)

    for attempt, provider in enumerate(provider_chain):
        try:
            full_content = ""

            # Yield provider metadata as first SSE event
            yield f"data: {json.dumps({'provider': provider.name, 'model': provider.model, 'attempt': attempt + 1})}\n\n"

            async for line in stream_from_provider(provider, messages, temperature):
                if not line.startswith("data: "):
                    continue
                
                data = line[6:].strip()

                if data == "[DONE]":
                    # Final metadata event: word + char count
                    yield f"data: {json.dumps({'done': True, 'word_count': len(full_content.split()), 'char_count': len(full_content)})}\n\n"
                    return

                try:
                    chunk = json.loads(data)
                    delta = chunk["choices"][0]["delta"].get("content", "")
                    if delta:
                        full_content += delta
                        yield f"data: {json.dumps({'delta': delta})}\n\n"
                except (json.JSONDecodeError, KeyError, IndexError):
                    continue

            # Stream ended without [DONE] — treat as success
            if full_content:
                yield f"data: {json.dumps({'done': True, 'word_count': len(full_content.split()), 'char_count': len(full_content)})}\n\n"
                return

        except RateLimitError:
            print(f"[{provider.name}] Rate limited — trying next provider")
            yield f"data: {json.dumps({'info': f'{provider.name} rate limited, switching provider...'})}\n\n"
            continue

        except ProviderError as e:
            print(f"[{provider.name}] Provider error: {e}")
            continue

        except Exception as e:
            print(f"[{provider.name}] Unexpected error: {e}")
            continue

    # All providers exhausted
    yield f"data: {json.dumps({'error': 'All AI providers are currently unavailable. Please try again in a moment.', 'done': True})}\n\n"
