"""
Follow-up Questions Service
Generates intelligent follow-up questions based on content type and initial input.
"""

from typing import List
from services.model_router import get_provider_chain
from services.ai_client import get_response_from_provider, RateLimitError, ProviderError


# Follow-up question templates for each content type
FOLLOWUP_TEMPLATES = {
    "resume": [
        "What is your full name?",
        "What is your email address and phone number?",
        "What is your current education level and institution?",
        "What are your top 3-5 technical skills or areas of expertise?",
        "Describe your most recent work experience or internship (company, role, duration, key achievements)",
        "What are 2-3 significant projects you've worked on? Include technologies used and measurable results",
        "What certifications or additional training do you have?",
        "What is your LinkedIn profile or GitHub username?"
    ],
    "cover_letter": [
        "What is the company name and position you're applying for?",
        "What specific skills or experiences make you a good fit for this role?",
        "Why are you interested in this company?",
        "What is a key achievement that demonstrates your qualifications?",
        "When are you available to start?"
    ],
    "blog_post": [
        "What is the main topic or title of your blog post?",
        "Who is your target audience?",
        "What are the key points you want to cover?",
        "What tone would you like (professional, casual, technical, etc.)?",
        "Do you have any specific examples or data to include?"
    ],
    "email": [
        "Who is the recipient of this email?",
        "What is the main purpose of this email?",
        "What action do you want the recipient to take?",
        "What is the context or background information?",
        "What tone is appropriate (formal, casual, urgent, etc.)?"
    ],
    "social_media": [
        "What platform is this for (Twitter, LinkedIn, Instagram, etc.)?",
        "What is the main message or call-to-action?",
        "Who is your target audience?",
        "Do you want to include hashtags or mentions?",
        "What tone fits your brand (professional, fun, inspirational, etc.)?"
    ],
    "general": [
        "What is the main topic or subject?",
        "What is the purpose of this content?",
        "Who is the intended audience?",
        "What key points should be included?",
        "What tone or style do you prefer?"
    ]
}


async def generate_followup_questions(
    content_type: str,
    initial_prompt: str = "",
    user_id: str = ""
) -> List[str]:
    """
    Generate intelligent follow-up questions based on content type and initial prompt.
    
    Args:
        content_type: Type of content (resume, cover_letter, blog_post, etc.)
        initial_prompt: User's initial input (optional)
        user_id: User ID for tracking (optional)
    
    Returns:
        List of 3-8 follow-up questions
    
    Raises:
        Exception: If question generation fails
    """
    # Get template questions for this content type
    template_questions = FOLLOWUP_TEMPLATES.get(content_type, FOLLOWUP_TEMPLATES["general"])
    
    # If no initial prompt, return template questions
    if not initial_prompt or len(initial_prompt.strip()) < 10:
        return template_questions[:5]  # Return first 5 questions
    
    # If there's an initial prompt, use AI to generate contextual questions
    try:
        system_prompt = f"""You are an expert assistant helping users create {content_type.replace('_', ' ')} content.

Based on the user's initial input, generate 5-8 specific follow-up questions that will help you gather all necessary information to create high-quality {content_type.replace('_', ' ')} content.

Rules:
1. Ask specific, actionable questions
2. Focus on missing information needed for the content type
3. Keep questions clear and concise
4. Number each question (1., 2., 3., etc.)
5. Don't ask questions about information already provided
6. For resumes: ask about education, experience, skills, projects, achievements
7. For cover letters: ask about the job, company, qualifications, motivation
8. For other content: ask about purpose, audience, key points, tone

User's initial input: "{initial_prompt}"

Generate 5-8 follow-up questions:"""

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Generate follow-up questions for creating a {content_type.replace('_', ' ')}."}
        ]
        
        # Get provider chain and try to generate questions
        provider_chain = get_provider_chain(content_type)
        
        for provider in provider_chain:
            try:
                response = await get_response_from_provider(provider, messages, temperature=0.7)
                
                if response:
                    # Parse questions from response
                    questions = []
                    for line in response.split('\n'):
                        line = line.strip()
                        # Match numbered questions (1., 2., etc.)
                        if line and (line[0].isdigit() or line.startswith('-') or line.startswith('•')):
                            # Remove numbering and clean up
                            question = line.lstrip('0123456789.-•) ').strip()
                            if question and len(question) > 10:
                                questions.append(question)
                    
                    # Return AI-generated questions if we got at least 3
                    if len(questions) >= 3:
                        return questions[:8]  # Max 8 questions
                    
            except (RateLimitError, ProviderError):
                continue
            except Exception:
                continue
        
        # Fallback to template questions if AI generation fails
        return template_questions[:5]
        
    except Exception:
        # Fallback to template questions
        return template_questions[:5]


def get_resume_questions() -> List[str]:
    """Get standard resume questions."""
    return FOLLOWUP_TEMPLATES["resume"]


def get_cover_letter_questions() -> List[str]:
    """Get standard cover letter questions."""
    return FOLLOWUP_TEMPLATES["cover_letter"]
