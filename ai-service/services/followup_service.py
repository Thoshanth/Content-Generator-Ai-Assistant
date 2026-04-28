"""
Follow-up Questions Service
Generates intelligent follow-up questions that the AI bot asks the user.
The bot proactively asks these questions to gather more information.
"""

from typing import List, Dict, Any
from services.model_router import get_provider_chain
from services.ai_client import get_response_from_provider, RateLimitError, ProviderError


async def should_ask_followup_questions(
    content_type: str,
    user_message: str,
    conversation_history: List[Dict[str, str]] = None
) -> bool:
    """
    Determine if the bot should ask follow-up questions based on the user's message.
    
    Args:
        content_type: Type of content being generated
        user_message: User's latest message
        conversation_history: Previous conversation messages
    
    Returns:
        bool: True if bot should ask follow-up questions
    """
    # Don't ask follow-up for general chat
    if content_type == 'general':
        return False
    
    # Don't ask if conversation is already deep (more than 3 exchanges)
    if conversation_history and len(conversation_history) > 6:
        return False
    
    # Ask follow-up if user's message is vague or short for content creation
    if len(user_message.strip()) < 50:
        return True
    
    # Ask follow-up for specific content types that need detailed info
    content_needs_details = ['resume', 'cover_letter', 'blog_post', 'email']
    if content_type in content_needs_details:
        return True
    
    return False


async def generate_bot_followup_questions(
    content_type: str,
    user_message: str,
    conversation_history: List[Dict[str, str]] = None,
    user_id: str = ""
) -> str:
    """
    Generate follow-up questions that the bot will ask the user.
    Returns a formatted message with questions for the bot to send.
    
    Args:
        content_type: Type of content (resume, cover_letter, etc.)
        user_message: User's initial message
        conversation_history: Previous conversation
        user_id: User ID for tracking
    
    Returns:
        str: Formatted message with follow-up questions for the bot to ask
    """
    try:
        # Create system prompt for generating bot follow-up questions
        system_prompt = f"""You are an AI assistant helping users create {content_type.replace('_', ' ')} content.

The user just said: "{user_message}"

Your task is to ask 3-5 specific follow-up questions to gather the information you need to create excellent {content_type.replace('_', ' ')} content.

IMPORTANT RULES:
1. Ask questions directly as if you're having a conversation
2. Be friendly and conversational
3. Ask specific, actionable questions
4. Focus on missing information needed for {content_type.replace('_', ' ')}
5. Don't ask about information already provided
6. Number your questions (1., 2., 3., etc.)
7. End with encouragement

For {content_type}:
- Resume: Ask about name, contact, education, skills, experience, projects, achievements
- Cover letter: Ask about job details, company, qualifications, motivation
- Blog post: Ask about topic, audience, key points, tone, examples
- Email: Ask about recipient, purpose, action needed, context

Example format:
"I'd be happy to help you create a [content_type]! To make sure I create the best possible content for you, I need to gather some specific information. Let me ask you a few questions:

1. [Specific question about missing info]
2. [Another specific question]
3. [Third specific question]

Once I have these details, I'll be able to create exactly what you need!"

Generate your response now:"""

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Generate follow-up questions for: {user_message}"}
        ]
        
        # Get provider chain and try to generate questions
        provider_chain = get_provider_chain(content_type)
        
        for provider in provider_chain:
            try:
                response = await get_response_from_provider(provider, messages, temperature=0.7)
                
                if response and len(response.strip()) > 50:
                    return response.strip()
                    
            except (RateLimitError, ProviderError):
                continue
            except Exception:
                continue
        
        # Fallback to template-based questions if AI generation fails
        return generate_template_followup_message(content_type, user_message)
        
    except Exception:
        # Final fallback
        return generate_template_followup_message(content_type, user_message)


def generate_template_followup_message(content_type: str, user_message: str) -> str:
    """
    Generate template follow-up message when AI generation fails.
    """
    templates = {
        "resume": {
            "intro": "I'd be happy to help you create a professional resume! To make sure I create the best possible resume for you, I need to gather some specific information:",
            "questions": [
                "What is your full name and contact information (email, phone, location)?",
                "What is your current education level and field of study?",
                "What are your top 3-5 technical skills or areas of expertise?",
                "Can you describe your most recent work experience or internship?",
                "What are 2-3 significant projects or achievements you'd like to highlight?"
            ],
            "outro": "Once I have these details, I'll create a compelling resume that showcases your strengths!"
        },
        "cover_letter": {
            "intro": "I'd be happy to help you write a compelling cover letter! To create a personalized and effective letter, I need some key information:",
            "questions": [
                "What is the company name and specific position you're applying for?",
                "What are the key requirements or qualifications mentioned in the job posting?",
                "What specific skills or experiences make you a strong fit for this role?",
                "Why are you particularly interested in this company?",
                "What is one key achievement that demonstrates your qualifications?"
            ],
            "outro": "With these details, I'll craft a cover letter that makes you stand out!"
        },
        "blog_post": {
            "intro": "I'd love to help you create an engaging blog post! To write content that resonates with your audience, let me ask a few questions:",
            "questions": [
                "What is the main topic or title you have in mind?",
                "Who is your target audience for this post?",
                "What are the 3-5 key points you want to cover?",
                "What tone would you like (professional, casual, technical, conversational)?",
                "Do you have any specific examples, data, or personal experiences to include?"
            ],
            "outro": "With this information, I'll create a blog post that engages your readers!"
        },
        "email": {
            "intro": "I'll help you write an effective email! To ensure your message achieves its purpose, I need some context:",
            "questions": [
                "Who is the recipient of this email (their role/relationship to you)?",
                "What is the main purpose or goal of this email?",
                "What specific action do you want the recipient to take?",
                "What background information or context should I include?",
                "What tone is most appropriate (formal, casual, urgent, friendly)?"
            ],
            "outro": "With these details, I'll compose an email that gets results!"
        },
        "social_media": {
            "intro": "I'll help you create engaging social media content! To make sure it fits your brand and goals, let me ask:",
            "questions": [
                "What platform is this for (LinkedIn, Twitter, Instagram, Facebook)?",
                "What is your main message or call-to-action?",
                "Who is your target audience?",
                "What tone fits your brand (professional, fun, inspirational, educational)?",
                "Do you want to include hashtags, mentions, or links?"
            ],
            "outro": "I'll create content that engages your audience and drives results!"
        }
    }
    
    template = templates.get(content_type, {
        "intro": f"I'd be happy to help you create {content_type.replace('_', ' ')} content! To provide the best assistance, let me ask a few questions:",
        "questions": [
            "What is the main topic or subject?",
            "What is the purpose or goal?",
            "Who is your target audience?",
            "What key points should be included?",
            "What tone or style do you prefer?"
        ],
        "outro": "With this information, I'll create exactly what you need!"
    })
    
    # Format the message
    message_parts = [template["intro"], ""]
    
    for i, question in enumerate(template["questions"], 1):
        message_parts.append(f"{i}. {question}")
    
    message_parts.extend(["", template["outro"]])
    
    return "\n".join(message_parts)


# Keep the old function for backward compatibility but mark as deprecated
async def generate_followup_questions(
    content_type: str,
    initial_prompt: str = "",
    user_id: str = ""
) -> List[str]:
    """
    DEPRECATED: Use generate_bot_followup_questions instead.
    This function is kept for backward compatibility.
    """
    # Convert to new format and extract questions
    message = await generate_bot_followup_questions(content_type, initial_prompt, [], user_id)
    
    # Extract numbered questions from the message
    questions = []
    for line in message.split('\n'):
        line = line.strip()
        if line and (line[0].isdigit() or line.startswith('-')):
            question = line.lstrip('0123456789.-) ').strip()
            if question and len(question) > 10:
                questions.append(question)
    
    return questions[:8]  # Return max 8 questions
