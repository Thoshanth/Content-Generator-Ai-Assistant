"""
Post Processor Service
Cleans and formats raw LLM output.
"""

import re
from typing import Optional


def clean_markdown(content: str) -> str:
    """
    Clean and normalize markdown content.
    Removes extra whitespace, fixes formatting issues.
    
    Args:
        content: Raw markdown content
    
    Returns:
        Cleaned markdown
    """
    # Remove leading/trailing whitespace
    content = content.strip()
    
    # Fix multiple blank lines (max 2)
    content = re.sub(r'\n\n\n+', '\n\n', content)
    
    # Fix spacing around headings
    content = re.sub(r'\n\n(#+\s)', r'\n\n\1', content)
    content = re.sub(r'(#+\s.*?)\n\n\n', r'\1\n\n', content)
    
    # Fix spacing around lists
    content = re.sub(r'\n\n(\*|-|\d+\.)\s', r'\n\1 ', content)
    
    # Fix spacing around code blocks
    content = re.sub(r'\n\n```', r'\n```', content)
    content = re.sub(r'```\n\n', r'```\n', content)
    
    return content


def remove_markdown_artifacts(content: str) -> str:
    """
    Remove common markdown artifacts and formatting errors.
    
    Args:
        content: Markdown content
    
    Returns:
        Cleaned content
    """
    # Remove markdown comments
    content = re.sub(r'<!--.*?-->', '', content, flags=re.DOTALL)
    
    # Remove HTML comments
    content = re.sub(r'<!--.*?-->', '', content, flags=re.DOTALL)
    
    # Remove YAML frontmatter
    if content.startswith('---'):
        content = re.sub(r'^---\n.*?\n---\n', '', content, flags=re.DOTALL)
    
    # Remove extra backticks
    content = re.sub(r'````+', '```', content)
    
    return content


def fix_common_errors(content: str) -> str:
    """
    Fix common LLM output errors.
    
    Args:
        content: Content with potential errors
    
    Returns:
        Fixed content
    """
    # Fix common typos and formatting issues
    replacements = {
        r'\[EDIT\]': '',
        r'\[NOTE\]': '',
        r'\[TODO\]': '',
        r'\*\*\*': '**',
        r'___': '__',
    }
    
    for pattern, replacement in replacements.items():
        content = re.sub(pattern, replacement, content)
    
    return content


def extract_main_content(content: str) -> str:
    """
    Extract main content, removing preamble and postamble.
    
    Args:
        content: Full response content
    
    Returns:
        Main content
    """
    # Remove common preambles
    preambles = [
        r'^Here\'s.*?:\n+',
        r'^I\'ve.*?:\n+',
        r'^Here are.*?:\n+',
        r'^Below.*?:\n+',
    ]
    
    for preamble in preambles:
        content = re.sub(preamble, '', content, flags=re.IGNORECASE)
    
    # Remove common postambles
    postambles = [
        r'\n+Feel free to.*?$',
        r'\n+Let me know.*?$',
        r'\n+Hope this.*?$',
        r'\n+Please let me.*?$',
    ]
    
    for postamble in postambles:
        content = re.sub(postamble, '', content, flags=re.IGNORECASE | re.DOTALL)
    
    return content.strip()


def format_for_content_type(content: str, content_type: str) -> str:
    """
    Apply content-type-specific formatting.
    
    Args:
        content: Raw content
        content_type: Type of content (email, resume, etc.)
    
    Returns:
        Formatted content
    """
    if content_type == "email":
        return format_email(content)
    elif content_type == "resume":
        return format_resume(content)
    elif content_type == "cover_letter":
        return format_cover_letter(content)
    elif content_type == "blog_post":
        return format_blog_post(content)
    else:
        return content


def format_email(content: str) -> str:
    """Format email content."""
    # Ensure proper email structure
    if not content.startswith("Subject:"):
        # Try to extract subject from first line
        lines = content.split('\n')
        if lines:
            content = f"Subject: {lines[0]}\n\n" + '\n'.join(lines[1:])
    
    return content


def format_resume(content: str) -> str:
    """Format resume content."""
    # Ensure proper resume structure with sections
    sections = ["CONTACT", "SUMMARY", "EXPERIENCE", "EDUCATION", "SKILLS"]
    
    for section in sections:
        if section not in content.upper():
            # Add missing section headers if needed
            pass
    
    return content


def format_cover_letter(content: str) -> str:
    """Format cover letter content."""
    # Ensure proper letter structure
    if not re.search(r'Dear\s+', content, re.IGNORECASE):
        content = "Dear Hiring Manager,\n\n" + content
    
    if not re.search(r'Sincerely|Best regards|Thank you', content, re.IGNORECASE):
        content = content.rstrip() + "\n\nSincerely,\n[Your Name]"
    
    return content


def format_blog_post(content: str) -> str:
    """Format blog post content."""
    # Ensure proper blog structure with title and sections
    lines = content.split('\n')
    
    # Ensure first line is a heading
    if lines and not lines[0].startswith('#'):
        lines[0] = f"# {lines[0]}"
    
    return '\n'.join(lines)


def post_process(content: str, content_type: str = "general") -> str:
    """
    Complete post-processing pipeline.
    
    Args:
        content: Raw LLM output
        content_type: Type of content
    
    Returns:
        Fully processed content
    """
    # Apply processing steps in order
    content = remove_markdown_artifacts(content)
    content = fix_common_errors(content)
    content = extract_main_content(content)
    content = clean_markdown(content)
    content = format_for_content_type(content, content_type)
    
    return content
