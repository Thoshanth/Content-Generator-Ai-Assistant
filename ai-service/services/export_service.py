"""
Export Service
Converts AI markdown output to different formats: plain text, HTML, markdown.
"""

import re
from typing import Optional


def to_plain_text(markdown_content: str) -> str:
    """
    Convert markdown to plain text by removing all markdown syntax.
    
    Args:
        markdown_content: Markdown-formatted text
    
    Returns:
        Plain text without markdown symbols
    """
    text = markdown_content
    
    # Remove markdown links [text](url) → text
    text = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', text)
    
    # Remove markdown images ![alt](url)
    text = re.sub(r'!\[([^\]]*)\]\([^\)]+\)', '', text)
    
    # Remove bold **text** → text
    text = re.sub(r'\*\*([^\*]+)\*\*', r'\1', text)
    text = re.sub(r'__([^_]+)__', r'\1', text)
    
    # Remove italic *text* → text
    text = re.sub(r'\*([^\*]+)\*', r'\1', text)
    text = re.sub(r'_([^_]+)_', r'\1', text)
    
    # Remove strikethrough ~~text~~ → text
    text = re.sub(r'~~([^~]+)~~', r'\1', text)
    
    # Remove code blocks (triple backticks)
    text = re.sub(r'```[\s\S]*?```', '', text)
    
    # Remove inline code `text` → text
    text = re.sub(r'`([^`]+)`', r'\1', text)
    
    # Remove headings (# ## ### etc) but keep content
    text = re.sub(r'^#+\s+', '', text, flags=re.MULTILINE)
    
    # Remove horizontal rules
    text = re.sub(r'^[-*_]{3,}$', '', text, flags=re.MULTILINE)
    
    # Remove blockquotes > but keep content
    text = re.sub(r'^>\s+', '', text, flags=re.MULTILINE)
    
    # Clean up multiple blank lines
    text = re.sub(r'\n\n\n+', '\n\n', text)
    
    # Strip leading/trailing whitespace
    text = text.strip()
    
    return text


def to_html(markdown_content: str) -> str:
    """
    Convert markdown to HTML.
    Uses basic regex patterns for common markdown elements.
    
    Args:
        markdown_content: Markdown-formatted text
    
    Returns:
        HTML-formatted text
    """
    html = markdown_content
    
    # Escape HTML special characters (but not our own tags)
    # This is done selectively to avoid double-escaping
    
    # Convert headings
    html = re.sub(r'^### (.*?)$', r'<h3>\1</h3>', html, flags=re.MULTILINE)
    html = re.sub(r'^## (.*?)$', r'<h2>\1</h2>', html, flags=re.MULTILINE)
    html = re.sub(r'^# (.*?)$', r'<h1>\1</h1>', html, flags=re.MULTILINE)
    
    # Convert bold
    html = re.sub(r'\*\*([^\*]+)\*\*', r'<strong>\1</strong>', html)
    html = re.sub(r'__([^_]+)__', r'<strong>\1</strong>', html)
    
    # Convert italic
    html = re.sub(r'\*([^\*]+)\*', r'<em>\1</em>', html)
    html = re.sub(r'_([^_]+)_', r'<em>\1</em>', html)
    
    # Convert strikethrough
    html = re.sub(r'~~([^~]+)~~', r'<del>\1</del>', html)
    
    # Convert inline code
    html = re.sub(r'`([^`]+)`', r'<code>\1</code>', html)
    
    # Convert code blocks
    html = re.sub(
        r'```(.*?)\n([\s\S]*?)```',
        r'<pre><code class="language-\1">\2</code></pre>',
        html
    )
    
    # Convert links
    html = re.sub(r'\[([^\]]+)\]\(([^\)]+)\)', r'<a href="\2">\1</a>', html)
    
    # Convert unordered lists
    html = re.sub(r'^\* (.*?)$', r'<li>\1</li>', html, flags=re.MULTILINE)
    html = re.sub(r'^\- (.*?)$', r'<li>\1</li>', html, flags=re.MULTILINE)
    html = re.sub(r'((?:<li>.*?</li>\n?)+)', r'<ul>\1</ul>', html)
    
    # Convert ordered lists
    html = re.sub(r'^\d+\. (.*?)$', r'<li>\1</li>', html, flags=re.MULTILINE)
    
    # Convert blockquotes
    html = re.sub(r'^> (.*?)$', r'<blockquote>\1</blockquote>', html, flags=re.MULTILINE)
    
    # Convert line breaks to paragraphs
    paragraphs = html.split('\n\n')
    html = ''.join(f'<p>{p.strip()}</p>' if p.strip() and not p.strip().startswith('<') else p for p in paragraphs)
    
    # Wrap in basic HTML structure
    html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body {{ font-family: -apple-system, Helvetica, Arial, sans-serif; line-height: 1.6; max-width: 800px; margin: 0 auto; padding: 20px; }}
        h1, h2, h3 {{ color: #333; margin-top: 20px; }}
        code {{ background: #f4f4f4; padding: 2px 6px; border-radius: 3px; font-family: monospace; }}
        pre {{ background: #f4f4f4; padding: 12px; border-radius: 5px; overflow-x: auto; }}
        blockquote {{ border-left: 4px solid #ddd; padding-left: 16px; color: #666; margin: 0; }}
        a {{ color: #0066cc; text-decoration: none; }}
        a:hover {{ text-decoration: underline; }}
    </style>
</head>
<body>
{html}
</body>
</html>"""
    
    return html


def to_markdown(content: str) -> str:
    """
    Return content as-is (already markdown).
    Useful for consistency in export pipeline.
    
    Args:
        content: Content (already in markdown)
    
    Returns:
        Same content
    """
    return content


def word_count(text: str) -> int:
    """Count words in text."""
    return len(text.split())


def char_count(text: str) -> int:
    """Count characters in text."""
    return len(text)
