"""
Smart Model Routing Service
Routes content types to optimal AI providers based on complexity and strengths.
"""

from dataclasses import dataclass
from typing import List
import os
from dotenv import load_dotenv

load_dotenv()


@dataclass
class ProviderConfig:
    """Configuration for a single AI provider."""
    name: str           # Human label for logs
    api_key: str
    base_url: str
    model: str


def _load_providers() -> dict[str, ProviderConfig]:
    """Load all 4 provider configs from environment variables."""
    return {
        "groq": ProviderConfig(
            name="Groq",
            api_key=os.getenv("GROQ_API_KEY", ""),
            base_url=os.getenv("GROQ_BASE_URL", "https://api.groq.com/openai/v1"),
            model=os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")
        ),
        "gemini": ProviderConfig(
            name="Gemini",
            api_key=os.getenv("GEMINI_API_KEY", ""),
            base_url=os.getenv("GEMINI_BASE_URL",
                               "https://generativelanguage.googleapis.com/v1beta/openai"),
            model=os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
        ),
        "nvidia": ProviderConfig(
            name="NVIDIA NIM",
            api_key=os.getenv("NVIDIA_API_KEY", ""),
            base_url=os.getenv("NVIDIA_BASE_URL", "https://integrate.api.nvidia.com/v1"),
            model=os.getenv("NVIDIA_MODEL", "meta/llama-3.3-70b-instruct")
        ),
        "cerebras": ProviderConfig(
            name="Cerebras",
            api_key=os.getenv("CEREBRAS_API_KEY", ""),
            base_url=os.getenv("CEREBRAS_BASE_URL", "https://api.cerebras.ai/v1"),
            model=os.getenv("CEREBRAS_MODEL", "llama-3.3-70b")
        ),
    }


# Smart routing table: content_type → ordered provider keys
# Optimized routing based on provider strengths:
# - Groq: Speed/creative/chat (fastest LPU)
# - Gemini: Structured long-form (best at formatted multi-section output)
# - NVIDIA NIM: Technical/resume/code (100+ models, no token billing)
# - Cerebras: Universal final fallback (1M tokens/day, 2,600 TPS, ultra reliable)
ROUTING_TABLE: dict[str, List[str]] = {
    "general":        ["groq",    "gemini",  "nvidia",   "cerebras"],
    "blog_post":      ["gemini",  "groq",    "nvidia",   "cerebras"],
    "email":          ["gemini",  "groq",    "nvidia",   "cerebras"],
    "social_media":   ["groq",    "gemini",  "nvidia",   "cerebras"],
    "ad_copy":        ["groq",    "gemini",  "nvidia",   "cerebras"],
    "tweet_thread":   ["groq",    "gemini",  "nvidia",   "cerebras"],
    "resume":         ["nvidia",  "cerebras","gemini",   "groq"    ],
    "cover_letter":   ["gemini",  "nvidia",  "cerebras", "groq"    ],
    "youtube_script": ["gemini",  "groq",    "nvidia",   "cerebras"],
    "product_desc":   ["groq",    "gemini",  "nvidia",   "cerebras"],
    "essay":          ["gemini",  "nvidia",  "cerebras", "groq"    ],
    "code_explainer": ["nvidia",  "cerebras","gemini",   "groq"    ],
}


def get_provider_chain(content_type: str) -> List[ProviderConfig]:
    """
    Returns ordered list of ProviderConfig for the given content type.
    Always ends with DeepSeek as the universal final fallback.
    
    Args:
        content_type: Type of content (e.g., "email", "resume", "blog_post")
    
    Returns:
        List of ProviderConfig objects in priority order
    """
    providers = _load_providers()
    order = ROUTING_TABLE.get(content_type, ROUTING_TABLE["general"])
    
    # Filter out providers without API keys
    chain = [providers[key] for key in order if providers[key].api_key]
    
    # Ensure at least one provider is available
    if not chain:
        raise ValueError(f"No AI providers configured. Please set API keys in .env")
    
    return chain


def get_primary_provider(content_type: str) -> ProviderConfig:
    """Get the primary (first) provider for a content type."""
    chain = get_provider_chain(content_type)
    return chain[0] if chain else None


def get_all_available_providers() -> dict[str, ProviderConfig]:
    """Get all configured providers with API keys."""
    providers = _load_providers()
    return {key: config for key, config in providers.items() if config.api_key}
