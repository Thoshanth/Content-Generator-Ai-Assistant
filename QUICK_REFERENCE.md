# Quick Reference: Frontend API Usage

**All APIs are already connected!** ✅

---

## 🚀 Quick Start

### 1. Import Methods
```javascript
import { 
  // Direct AI Service (no auth)
  streamAiResponse,
  generateContent,
  exportContent,
  exportPdf,
  getAiProviders,
  
  // Backend (with auth)
  sendChatMessage,
  sendChatMessageStream,
  getChatSessions,
  
  // Constants
  CONTENT_TYPES,
  TONES,
  LENGTHS,
  LANGUAGES
} from '@/services/api'
```

---

## 📝 Common Use Cases

### 1. Generate Resume (NVIDIA NIM Primary)
```javascript
const response = await sendChatMessage({
  prompt: 'Create a resume for a Senior Software Engineer with 5 years experience',
  contentType: CONTENT_TYPES.RESUME,
  tone: TONES.PROFESSIONAL,
  length: LENGTHS.MEDIUM,
  language: LANGUAGES.ENGLISH,
  sessionId: currentSessionId
})

console.log(response.provider)  // "NVIDIA NIM"
console.log(response.content)   // Resume content
console.log(response.wordCount) // Word count
```

### 2. Generate Blog Post (Gemini Primary)
```javascript
const response = await sendChatMessage({
  prompt: 'Write a blog post about AI trends in 2026',
  contentType: CONTENT_TYPES.BLOG_POST,
  tone: TONES.PROFESSIONAL,
  length: LENGTHS.LONG,
  sessionId: currentSessionId
})

console.log(response.provider)  // "Gemini"
```

### 3. Explain Code (NVIDIA NIM Primary)
```javascript
const response = await sendChatMessage({
  prompt: 'Explain how async/await works in JavaScript',
  contentType: CONTENT_TYPES.CODE_EXPLAINER,
  tone: TONES.PROFESSIONAL,
  length: LENGTHS.MEDIUM
})

console.log(response.provider)  // "NVIDIA NIM"
```

### 4. Generate Email (Gemini Primary)
```javascript
const response = await sendChatMessage({
  prompt: 'Write a professional email about a meeting',
  contentType: CONTENT_TYPES.EMAIL,
  tone: TONES.PROFESSIONAL,
  length: LENGTHS.SHORT
})

console.log(response.provider)  // "Gemini"
```

### 5. Social Media Post (Groq Primary)
```javascript
const response = await sendChatMessage({
  prompt: 'Write a tweet about our new product launch',
  contentType: CONTENT_TYPES.SOCIAL_MEDIA,
  tone: TONES.FRIENDLY,
  length: LENGTHS.SHORT
})

console.log(response.provider)  // "Groq"
```

---

## 🎬 Streaming Examples

### Stream with Callbacks
```javascript
await sendChatMessageStream(
  {
    prompt: 'Write a blog post about AI',
    contentType: CONTENT_TYPES.BLOG_POST,
    tone: TONES.PROFESSIONAL,
    length: LENGTHS.LONG,
    sessionId: currentSessionId
  },
  (data) => {
    // onMessage callback
    if (data.provider) {
      console.log('Using provider:', data.provider)
    }
    if (data.delta) {
      appendToEditor(data.delta)
    }
    if (data.done) {
      console.log('Complete!', data.wordCount, 'words')
    }
  },
  (error) => {
    // onError callback
    showError(error.message)
  },
  () => {
    // onComplete callback
    enableInput()
  }
)
```

### Direct Streaming (No Auth)
```javascript
const eventSource = streamAiResponse({
  prompt: 'Write a creative story',
  content_type: 'general',
  tone: 'creative',
  length: 'medium'
})

eventSource.onmessage = (event) => {
  const data = JSON.parse(event.data)
  
  if (data.provider) {
    console.log('Provider:', data.provider)
  }
  
  if (data.delta) {
    appendText(data.delta)
  }
  
  if (data.done) {
    console.log('Done!', data.word_count, 'words')
    eventSource.close()
  }
}

eventSource.onerror = (error) => {
  console.error('Error:', error)
  eventSource.close()
}
```

---

## 📤 Export Examples

### Export to HTML
```javascript
const htmlExport = await exportContent(
  content,
  'html',
  'resume'
)

console.log(htmlExport.content)  // HTML with styling
console.log(htmlExport.word_count)
```

### Export to PDF
```javascript
const pdfBlob = await exportPdf(
  content,
  'resume',
  'John_Doe'
)

// Download PDF
const url = URL.createObjectURL(pdfBlob)
const a = document.createElement('a')
a.href = url
a.download = 'John_Doe_Resume.pdf'
a.click()
URL.revokeObjectURL(url)
```

---

## 🎯 Content Types

```javascript
CONTENT_TYPES = {
  GENERAL: 'general',           // Groq primary
  BLOG_POST: 'blog_post',       // Gemini primary
  EMAIL: 'email',               // Gemini primary
  SOCIAL_MEDIA: 'social_media', // Groq primary
  AD_COPY: 'ad_copy',           // Groq primary
  TWEET_THREAD: 'tweet_thread', // Groq primary
  RESUME: 'resume',             // NVIDIA NIM primary ⭐
  COVER_LETTER: 'cover_letter', // Gemini primary
  YOUTUBE_SCRIPT: 'youtube_script', // Gemini primary
  PRODUCT_DESC: 'product_desc', // Groq primary
  ESSAY: 'essay',               // Gemini primary
  CODE_EXPLAINER: 'code_explainer' // NVIDIA NIM primary ⭐
}
```

---

## 🎨 Tones

```javascript
TONES = {
  PROFESSIONAL: 'professional',
  CASUAL: 'casual',
  FORMAL: 'formal',
  PERSUASIVE: 'persuasive',
  FRIENDLY: 'friendly',
  WITTY: 'witty',
  EMPATHETIC: 'empathetic'
}
```

---

## 📏 Lengths

```javascript
LENGTHS = {
  SHORT: 'short',     // 100-300 words
  MEDIUM: 'medium',   // 300-800 words
  LONG: 'long',       // 800+ words
  AUTO: 'auto'        // AI decides
}
```

---

## 🌍 Languages

```javascript
LANGUAGES = {
  ENGLISH: 'English',
  HINDI: 'Hindi',
  TELUGU: 'Telugu',
  SPANISH: 'Spanish',
  FRENCH: 'French',
  GERMAN: 'German',
  PORTUGUESE: 'Portuguese',
  ARABIC: 'Arabic',
  JAPANESE: 'Japanese',
  CHINESE: 'Chinese (Simplified)',
  KOREAN: 'Korean'
}
```

---

## 🔍 Provider Status

```javascript
const providers = await getAiProviders()

console.log(providers)
// {
//   "providers": [
//     {"name": "Groq", "model": "llama-3.1-8b-instant"},
//     {"name": "Gemini", "model": "gemini-1.5-flash"},
//     {"name": "NVIDIA NIM", "model": "meta/llama-3.3-70b-instruct"},
//     {"name": "Cerebras", "model": "llama-3.3-70b"}
//   ]
// }
```

---

## 💾 Session Management

```javascript
// Get all sessions
const sessions = await getChatSessions()

// Get specific session
const session = await getChatSession(sessionId)

// Create new session
const newSession = await createChatSession('My Chat', 'general')

// Delete session
await deleteChatSession(sessionId)

// Delete all sessions
await deleteAllChatSessions()
```

---

## 🎯 Provider Routing

| Content Type | Primary Provider | Why |
|---|---|---|
| resume | **NVIDIA NIM** | Technical content, 70B model |
| code_explainer | **NVIDIA NIM** | Technical content, 70B model |
| blog_post | **Gemini** | Best formatting |
| email | **Gemini** | Structured output |
| general | **Groq** | Fastest |
| social_media | **Groq** | Quick & creative |

---

## ⚡ Quick Tips

1. **Use CONTENT_TYPES constants** instead of strings
2. **Always close EventSource** after streaming
3. **Check provider in response** to see which was used
4. **Use appropriate content types** for better results
5. **Streaming is faster** than non-streaming for long content
6. **NVIDIA NIM is best** for technical/resume/code content
7. **Gemini is best** for structured long-form content
8. **Groq is fastest** for short creative content

---

## 🚀 Complete Example

```javascript
import { 
  sendChatMessage,
  sendChatMessageStream,
  exportPdf,
  CONTENT_TYPES,
  TONES,
  LENGTHS
} from '@/services/api'

async function generateAndExportResume() {
  try {
    // 1. Generate resume with streaming
    let fullContent = ''
    
    await sendChatMessageStream(
      {
        prompt: 'Create a resume for a Senior Software Engineer',
        contentType: CONTENT_TYPES.RESUME,
        tone: TONES.PROFESSIONAL,
        length: LENGTHS.MEDIUM,
        sessionId: currentSessionId
      },
      (data) => {
        if (data.provider) {
          console.log('Using:', data.provider)  // "NVIDIA NIM"
        }
        if (data.delta) {
          fullContent += data.delta
          updateEditor(fullContent)
        }
        if (data.done) {
          console.log('Generated:', data.word_count, 'words')
        }
      },
      (error) => {
        showError(error.message)
      },
      async () => {
        // 2. Export as PDF when complete
        const pdfBlob = await exportPdf(
          fullContent,
          'resume',
          'John_Doe'
        )
        
        // 3. Download PDF
        const url = URL.createObjectURL(pdfBlob)
        const a = document.createElement('a')
        a.href = url
        a.download = 'John_Doe_Resume.pdf'
        a.click()
        URL.revokeObjectURL(url)
        
        showSuccess('Resume generated and downloaded!')
      }
    )
  } catch (error) {
    showError(error.message)
  }
}
```

---

**Status:** ✅ ALL APIS CONNECTED  
**Providers:** ✅ 4/4 WORKING  
**Ready:** ✅ START USING NOW!

**Just import and use!** 🚀
