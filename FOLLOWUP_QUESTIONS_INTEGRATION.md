# Follow-Up Questions Integration - Claude AI Style

## Overview
This integration adds dynamic follow-up questions to the chat interface, similar to Claude AI's conversational approach. The system intelligently suggests relevant questions based on the content type and user's initial input to gather comprehensive information.

## Features

### 🎯 Smart Question Generation
- **Context-Aware**: Questions adapt based on content type (resume, cover letter, blog post, etc.)
- **AI-Powered**: Uses AI providers to generate contextual questions from user's initial input
- **Template Fallback**: Falls back to curated templates if AI generation fails
- **Dynamic Display**: Shows 5-8 relevant questions in an elegant grid layout

### 🎨 Claude-Style Interface
- **Elegant Design**: Clean, modern UI with smooth animations
- **Interactive Cards**: Hover effects and click animations for better UX
- **Responsive Grid**: 2-column layout on desktop, single column on mobile
- **Visual Feedback**: Icons, gradients, and transitions for engaging experience

### 🔄 Smart Behavior
- **Auto-Show**: Appears when chat is empty or after first user message
- **Auto-Hide**: Disappears when user sends a message or AI responds
- **Content-Type Aware**: Only shows for specific content types (not for general chat)
- **Non-Intrusive**: Positioned between chat window and input bar

## Architecture

### Backend Components

#### 1. Follow-Up Service (`ai-service/services/followup_service.py`)
```python
async def generate_followup_questions(
    content_type: str,
    initial_prompt: str = "",
    user_id: str = ""
) -> List[str]
```
- Generates 5-8 contextual questions
- Uses AI providers with fallback chain
- Template-based fallback for reliability

#### 2. Follow-Up Router (`ai-service/routers/followup.py`)
```python
POST /followup/questions
{
    "content_type": "resume",
    "initial_prompt": "I need help creating a resume",
    "user_id": "user123"
}

Response:
{
    "questions": ["What is your full name?", ...],
    "content_type": "resume"
}
```

### Frontend Components

#### 1. FollowUpQuestions Component (`frontend/src/components/chat/FollowUpQuestions.jsx`)
```jsx
<FollowUpQuestions 
  questions={followUpQuestions}
  onQuestionClick={handleFollowUpClick}
  isLoading={loadingFollowUp}
/>
```

**Features:**
- Animated question cards with hover effects
- Click to auto-fill input
- Loading states
- Responsive grid layout

#### 2. API Service (`frontend/src/services/api.js`)
```javascript
export async function getFollowUpQuestions(contentType, initialPrompt, userId)
```

#### 3. ChatPage Integration (`frontend/src/pages/ChatPage.jsx`)
- Loads questions when content type changes
- Shows questions when chat is empty or has only one user message
- Hides questions when user sends message
- Auto-fills input when question is clicked

## User Flow

### 1. Initial State
```
User opens chat → Selects content type (e.g., "Resume")
↓
System loads follow-up questions
↓
Questions appear below empty chat window
```

### 2. Question Interaction
```
User clicks a question card
↓
Question text fills the input bar
↓
Message is sent automatically
↓
Questions disappear, AI responds
```

### 3. Conversation Flow
```
User: "I need a resume for software engineer"
↓
AI: "I'd be happy to help! Let me ask a few questions..."
↓
Follow-up questions appear:
  - What is your full name?
  - What is your email and phone?
  - What are your top skills?
  - Describe your recent work experience
  - etc.
```

## Content Type Templates

### Resume Questions
1. What is your full name?
2. What is your email address and phone number?
3. What is your current education level and institution?
4. What are your top 3-5 technical skills?
5. Describe your most recent work experience
6. What are 2-3 significant projects you've worked on?
7. What certifications do you have?
8. What is your LinkedIn profile or GitHub username?

### Cover Letter Questions
1. What is the company name and position?
2. What skills make you a good fit?
3. Why are you interested in this company?
4. What is a key achievement that demonstrates your qualifications?
5. When are you available to start?

### Blog Post Questions
1. What is the main topic or title?
2. Who is your target audience?
3. What are the key points to cover?
4. What tone would you like?
5. Do you have specific examples or data to include?

### Email Questions
1. Who is the recipient?
2. What is the main purpose?
3. What action do you want them to take?
4. What is the context or background?
5. What tone is appropriate?

## Styling & Design

### Color Scheme
- **Primary**: Peach (`#F9A8A8`)
- **Background**: Dark surface (`bg-surface-raised`)
- **Border**: Subtle white (`border-white/10`)
- **Hover**: Peach glow (`border-peach/50`)

### Animations
- **Entry**: Fade in + slide up (staggered)
- **Hover**: Scale up + glow effect
- **Click**: Scale down feedback
- **Exit**: Fade out + slide down

### Layout
```
┌─────────────────────────────────────┐
│  Chat Window (messages)             │
│                                     │
└─────────────────────────────────────┘
┌─────────────────────────────────────┐
│  ✨ Suggested questions              │
│  ┌──────────┐  ┌──────────┐        │
│  │ Question │  │ Question │        │
│  └──────────┘  └──────────┘        │
│  ┌──────────┐  ┌──────────┐        │
│  │ Question │  │ Question │        │
│  └──────────┘  └──────────┘        │
└─────────────────────────────────────┘
┌─────────────────────────────────────┐
│  Input Bar                          │
└─────────────────────────────────────┘
```

## Configuration

### Environment Variables
No additional environment variables needed. Uses existing AI service configuration.

### Content Type Mapping
Questions are automatically loaded for these content types:
- `resume`
- `cover_letter`
- `blog_post`
- `email`
- `social_media`
- `general` (fallback)

### Customization
To add new content types or modify questions:

1. **Backend**: Edit `ai-service/services/followup_service.py`
```python
FOLLOWUP_TEMPLATES = {
    "your_content_type": [
        "Question 1?",
        "Question 2?",
        # ...
    ]
}
```

2. **Frontend**: Questions load automatically based on content type

## Testing

### Manual Testing
1. Start AI service: `cd ai-service && python main.py`
2. Start frontend: `cd frontend && npm run dev`
3. Login and navigate to chat
4. Select a content type (e.g., Resume)
5. Verify questions appear
6. Click a question and verify it sends
7. Verify questions disappear after sending

### API Testing
```bash
# Test follow-up questions endpoint
curl -X POST http://localhost:8000/followup/questions \
  -H "Content-Type: application/json" \
  -d '{
    "content_type": "resume",
    "initial_prompt": "I need a resume",
    "user_id": "test123"
  }'
```

### Expected Response
```json
{
  "questions": [
    "What is your full name?",
    "What is your email address and phone number?",
    "What is your current education level and institution?",
    "What are your top 3-5 technical skills or areas of expertise?",
    "Describe your most recent work experience or internship"
  ],
  "content_type": "resume"
}
```

## Performance Considerations

### Optimization
- Questions load asynchronously (non-blocking)
- Cached templates for instant fallback
- Debounced API calls to prevent spam
- Lazy loading of AI-generated questions

### Error Handling
- Silent failure for question generation
- Automatic fallback to templates
- No impact on core chat functionality
- User can still type manually if questions fail

## Future Enhancements

### Planned Features
1. **Multi-turn Questions**: Sequential question flow
2. **Answer Validation**: Check if user answered the question
3. **Progress Tracking**: Show completion percentage
4. **Smart Suggestions**: Learn from user patterns
5. **Voice Input**: Click to speak answer
6. **Question Editing**: Modify questions before sending

### Potential Improvements
- Add question categories/grouping
- Support for conditional questions
- Integration with form builder
- Export question-answer pairs
- Analytics on question effectiveness

## Troubleshooting

### Questions Not Appearing
1. Check content type is not "general"
2. Verify AI service is running
3. Check browser console for errors
4. Ensure messages array is empty or has only one message

### Questions Not Sending
1. Check authentication status
2. Verify daily message limit not reached
3. Check network tab for API errors
4. Ensure input bar is not disabled

### Styling Issues
1. Clear browser cache
2. Check Tailwind CSS classes are compiled
3. Verify framer-motion is installed
4. Check for CSS conflicts

## API Reference

### POST /followup/questions
Generate follow-up questions based on content type and initial prompt.

**Request:**
```json
{
  "content_type": "resume",
  "initial_prompt": "I need help with my resume",
  "user_id": "user123"
}
```

**Response:**
```json
{
  "questions": ["Question 1?", "Question 2?", ...],
  "content_type": "resume"
}
```

**Status Codes:**
- `200`: Success
- `500`: Server error

### GET /followup/templates/{content_type}
Get template questions for a specific content type.

**Response:**
```json
{
  "content_type": "resume",
  "questions": ["Template question 1?", ...]
}
```

## Credits
- Inspired by Claude AI's conversational interface
- Built with React, Framer Motion, and FastAPI
- Icons from Lucide React

## License
Part of the Creo AI Content Generator project.
