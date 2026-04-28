# Follow-up Questions API Implementation

## Overview

Implemented a follow-up questions API that helps gather necessary information before generating content, especially for resumes and cover letters.

---

## Features Implemented

### 1. Follow-up Questions Service
**File**: `ai-service/services/followup_service.py`

- Generates intelligent follow-up questions based on content type
- Template-based questions for quick responses
- AI-powered contextual questions when initial prompt is provided
- Supports all content types (resume, cover_letter, blog_post, email, etc.)

### 2. API Endpoint
**File**: `ai-service/routers/tools.py`

**Endpoint**: `POST /tools/followup-questions`

**Request**:
```json
{
  "content_type": "resume",
  "content": "I want to create a resume for ML engineer",
  "user_id": "user-123"
}
```

**Response**:
```json
{
  "questions": [
    "What is your full name?",
    "What is your email address and phone number?",
    "What is your current education level and institution?",
    "What are your top 3-5 technical skills?",
    "Describe your most recent work experience",
    "What are 2-3 significant projects you've worked on?",
    "What certifications do you have?",
    "What is your LinkedIn or GitHub username?"
  ],
  "content_type": "resume"
}
```

### 3. Professional Resume Template
**File**: `ai-service/prompts/resume_template.py`

- ATS-friendly resume format
- Quantified achievements focus
- Professional structure matching the provided example
- Sections: Summary, Skills, Experience, Projects, Education, Certifications
- Emphasis on numbers, metrics, and measurable results

### 4. Frontend Integration
**File**: `frontend/src/services/api.js`

Added `getFollowUpQuestions()` method:
```javascript
export async function getFollowUpQuestions(contentType, initialContent = '', userId = '') {
  const response = await aiApi.post('/tools/followup-questions', {
    content_type: contentType,
    content: initialContent,
    user_id: userId
  })
  return response.data
}
```

---

## Resume Questions Template

When user selects "resume", the API returns these questions:

1. **What is your full name?**
2. **What is your email address and phone number?**
3. **What is your current education level and institution?**
4. **What are your top 3-5 technical skills or areas of expertise?**
5. **Describe your most recent work experience or internship** (company, role, duration, key achievements)
6. **What are 2-3 significant projects you've worked on?** Include technologies used and measurable results
7. **What certifications or additional training do you have?**
8. **What is your LinkedIn profile or GitHub username?**

---

## Resume Generation Format

The AI will generate resumes following this professional format:

```markdown
# FULL NAME
**Job Title/Role**

email@example.com | +phone | Location
LinkedIn: linkedin.com/in/username | GitHub: github.com/username

## SUMMARY

X-year [role] with Y months of [domain] experience across Z [projects/companies]. Built and deployed [technologies] achieving **X% accuracy** on Y dataset and **Z% metric** on W records.

## SKILLS

- **Languages**: Python, Java, SQL
- **ML Frameworks**: TensorFlow, PyTorch, Scikit-learn
- **Tools**: Git, Docker, AWS

## EXPERIENCE

### Job Title
**Company Name** | Duration
Location

- Deployed X [systems] using [technologies], cutting [metric] by ~Y% across Z [modules]
- Built [specific thing] with [technology] on X+ [items] — [techniques] — raising [metric] by Y%
- Documented [deliverable] for X releases; presented results to Y [stakeholders]

## PROJECTS

### Project Name
**Technologies**: Python, TensorFlow, OpenCV
Duration | Project Type

- Trained [model] on X [items] across Y classes achieving **Z% accuracy**
- Engineered [system] — [techniques] — delivering [performance metric]
- Built [feature] with [technology]; tested with X users, Y% success rate

## EDUCATION

### Institution Name
Degree in Major | CGPA: X.X/10
Duration | Location

- **Relevant Coursework**: Course1, Course2, Course3

## CERTIFICATIONS

- Certification Name | Platform: Date
- Certification Name | Platform: Date
```

---

## Usage Flow

### Step 1: Request Follow-up Questions
```bash
curl -X POST http://localhost:8000/tools/followup-questions \
  -H "Content-Type: application/json" \
  -d '{
    "content_type": "resume",
    "content": "I want to create a resume",
    "user_id": "user-123"
  }'
```

### Step 2: Collect User Answers
Frontend displays questions and collects answers from user.

### Step 3: Generate Resume
```bash
curl -X POST http://localhost:8000/chat/ \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Create a professional resume with this information: Name: John Doe, Email: john@example.com, ...",
    "content_type": "resume",
    "tone": "professional",
    "length": "medium",
    "language": "English"
  }'
```

---

## Testing

### Test Follow-up Questions API
```bash
cd ai-service
python test_followup_api.py
```

**Expected Output**:
```
✓ Success!
Content Type: resume
Number of Questions: 8

Follow-up Questions:
----------------------------------------------------------------------
1. What is your full name?
2. What is your email address and phone number?
3. What is your current education level and institution?
...
----------------------------------------------------------------------
```

### Test Resume Generation
```bash
cd ai-service
python -c "
from services.followup_service import get_resume_questions
questions = get_resume_questions()
for i, q in enumerate(questions, 1):
    print(f'{i}. {q}')
"
```

---

## Frontend Implementation (Next Steps)

### 1. Create Resume Wizard Component
```jsx
// components/ResumeWizard.jsx
import { useState, useEffect } from 'react';
import { getFollowUpQuestions } from '../services/api';

function ResumeWizard() {
  const [questions, setQuestions] = useState([]);
  const [answers, setAnswers] = useState({});
  const [currentStep, setCurrentStep] = useState(0);

  useEffect(() => {
    // Fetch follow-up questions
    getFollowUpQuestions('resume', '', userId)
      .then(data => setQuestions(data.questions))
      .catch(error => console.error(error));
  }, []);

  const handleNext = () => {
    if (currentStep < questions.length - 1) {
      setCurrentStep(currentStep + 1);
    } else {
      // Generate resume with collected answers
      generateResume(answers);
    }
  };

  return (
    <div className="resume-wizard">
      <h2>Create Your Resume</h2>
      <p>Question {currentStep + 1} of {questions.length}</p>
      
      <div className="question">
        <label>{questions[currentStep]}</label>
        <textarea
          value={answers[currentStep] || ''}
          onChange={(e) => setAnswers({
            ...answers,
            [currentStep]: e.target.value
          })}
          placeholder="Your answer..."
        />
      </div>

      <button onClick={handleNext}>
        {currentStep < questions.length - 1 ? 'Next' : 'Generate Resume'}
      </button>
    </div>
  );
}
```

### 2. Integrate with Chat Page
```jsx
// In ChatPage.jsx
import ResumeWizard from '../components/ResumeWizard';

// Show wizard when content type is 'resume'
{contentType === 'resume' && showWizard && (
  <ResumeWizard
    onComplete={(resumeContent) => {
      setMessages([...messages, {
        role: 'assistant',
        content: resumeContent
      }]);
      setShowWizard(false);
    }}
  />
)}
```

---

## API Documentation

### Endpoint: Get Follow-up Questions

**URL**: `POST /tools/followup-questions`

**Request Body**:
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| content_type | string | Yes | Type of content (resume, cover_letter, blog_post, etc.) |
| content | string | No | Initial user input (optional) |
| user_id | string | No | User ID for tracking (optional) |

**Response**:
```json
{
  "questions": ["string"],
  "content_type": "string"
}
```

**Status Codes**:
- `200`: Success
- `500`: Server error

---

## Files Created/Modified

### New Files
1. ✅ `ai-service/services/followup_service.py` - Follow-up questions service
2. ✅ `ai-service/prompts/resume_template.py` - Professional resume template
3. ✅ `ai-service/test_followup_api.py` - API test script
4. ✅ `FOLLOWUP_QUESTIONS_IMPLEMENTATION.md` - This documentation

### Modified Files
1. ✅ `ai-service/routers/tools.py` - Added follow-up questions endpoint
2. ✅ `ai-service/prompts/templates.py` - Added resume system prompt
3. ✅ `frontend/src/services/api.js` - Added getFollowUpQuestions method

---

## Next Steps

### Immediate
1. ✅ Test follow-up questions API
2. ⏳ Create frontend Resume Wizard component
3. ⏳ Integrate wizard with chat interface
4. ⏳ Test end-to-end resume generation flow

### Future Enhancements
1. Add progress indicator in wizard
2. Save partial answers (draft mode)
3. Allow editing previous answers
4. Add resume templates selection
5. Preview resume before final generation
6. Export to multiple formats (PDF, DOCX, TXT)

---

## Summary

✅ **Follow-up Questions API**: Implemented and working  
✅ **Resume Template**: Professional format with quantified achievements  
✅ **Frontend Integration**: API method added  
✅ **Testing**: Test script created  
⏳ **Frontend UI**: Needs Resume Wizard component  

**The API is ready to use! Just need to create the frontend wizard component.**
