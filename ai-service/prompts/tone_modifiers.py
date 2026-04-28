"""
Tone and Length Modifiers
Injects tone, length, and language preferences into system prompts.
"""


def build_modifiers(tone: str = "professional", length: str = "auto", language: str = "English") -> str:
    """
    Build modifier string to inject into system prompt.
    Specifies tone, length, and language preferences.
    
    Args:
        tone: One of: professional, casual, formal, persuasive, friendly, witty, empathetic
        length: One of: short, medium, long, auto
        language: Output language (English, Hindi, Spanish, etc.)
    
    Returns:
        Modifier string to append to system prompt
    """
    
    tone_instructions = {
        "professional": "Use a professional, business-appropriate tone. Be clear, concise, and authoritative.",
        "casual": "Use a casual, conversational tone. Be friendly and approachable.",
        "formal": "Use a formal, academic tone. Be precise and sophisticated.",
        "persuasive": "Use a persuasive tone. Build compelling arguments and call to action.",
        "friendly": "Use a warm, friendly tone. Be personable and encouraging.",
        "witty": "Use a witty, humorous tone. Include clever wordplay and light humor where appropriate.",
        "empathetic": "Use an empathetic, understanding tone. Show compassion and emotional intelligence.",
    }
    
    length_instructions = {
        "short": "Keep the response concise and brief. Aim for 100-300 words.",
        "medium": "Provide a balanced response. Aim for 300-800 words.",
        "long": "Provide a comprehensive, detailed response. Aim for 800+ words.",
        "auto": "Adjust length based on the content type and complexity of the request.",
    }
    
    language_instructions = {
        "English": "Write in English.",
        "Hindi": "Write in Hindi (Devanagari script).",
        "Telugu": "Write in Telugu script.",
        "Spanish": "Write in Spanish.",
        "French": "Write in French.",
        "German": "Write in German.",
        "Portuguese": "Write in Portuguese.",
        "Arabic": "Write in Arabic.",
        "Japanese": "Write in Japanese.",
        "Chinese (Simplified)": "Write in Simplified Chinese.",
        "Korean": "Write in Korean.",
    }
    
    tone_text = tone_instructions.get(tone, tone_instructions["professional"])
    length_text = length_instructions.get(length, length_instructions["auto"])
    language_text = language_instructions.get(language, language_instructions["English"])
    
    return f"""
TONE & STYLE:
{tone_text}

LENGTH:
{length_text}

LANGUAGE:
{language_text}
""".strip()


def get_tone_description(tone: str) -> str:
    """Get human-readable description of a tone."""
    descriptions = {
        "professional": "Professional & authoritative",
        "casual": "Casual & conversational",
        "formal": "Formal & academic",
        "persuasive": "Persuasive & compelling",
        "friendly": "Warm & friendly",
        "witty": "Witty & humorous",
        "empathetic": "Empathetic & understanding",
    }
    return descriptions.get(tone, tone)


def get_length_description(length: str) -> str:
    """Get human-readable description of a length preference."""
    descriptions = {
        "short": "Short (100-300 words)",
        "medium": "Medium (300-800 words)",
        "long": "Long (800+ words)",
        "auto": "Auto (based on content type)",
    }
    return descriptions.get(length, length)
