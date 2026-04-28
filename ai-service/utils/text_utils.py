"""
Text Utilities
Helper functions for text processing and analysis.
"""


def word_count(text: str) -> int:
    """
    Count words in text.
    
    Args:
        text: Input text
    
    Returns:
        Number of words
    """
    if not text:
        return 0
    return len(text.split())


def char_count(text: str) -> int:
    """
    Count characters in text (including spaces).
    
    Args:
        text: Input text
    
    Returns:
        Number of characters
    """
    return len(text)


def char_count_no_spaces(text: str) -> int:
    """
    Count characters in text (excluding spaces).
    
    Args:
        text: Input text
    
    Returns:
        Number of characters without spaces
    """
    return len(text.replace(" ", ""))


def estimate_reading_time(text: str, words_per_minute: int = 200) -> int:
    """
    Estimate reading time in minutes.
    
    Args:
        text: Input text
        words_per_minute: Average reading speed (default 200)
    
    Returns:
        Estimated reading time in minutes
    """
    words = word_count(text)
    return max(1, round(words / words_per_minute))


def truncate_text(text: str, max_length: int, suffix: str = "...") -> str:
    """
    Truncate text to maximum length with suffix.
    
    Args:
        text: Input text
        max_length: Maximum length including suffix
        suffix: Suffix to add if truncated (default "...")
    
    Returns:
        Truncated text
    """
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix


def extract_first_paragraph(text: str) -> str:
    """
    Extract first paragraph from text.
    
    Args:
        text: Input text
    
    Returns:
        First paragraph
    """
    paragraphs = text.split("\n\n")
    return paragraphs[0] if paragraphs else ""


def extract_summary(text: str, max_words: int = 50) -> str:
    """
    Extract first N words as summary.
    
    Args:
        text: Input text
        max_words: Maximum words in summary
    
    Returns:
        Summary text
    """
    words = text.split()[:max_words]
    summary = " ".join(words)
    if len(text.split()) > max_words:
        summary += "..."
    return summary
