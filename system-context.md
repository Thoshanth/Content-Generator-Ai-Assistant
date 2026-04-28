# System Context - AI Content Generator

This document provides a high-level overview of the AI Content Generator project, its architecture, components, and data flow.

## 🤖 Project Overview
The AI Content Generator is a full-stack platform designed to help users generate high-quality AI content like blog posts, emails, social media copy, and more. It features real-time streaming, persistent chat history, and an intelligent multi-provider AI routing system.

## 🏗️ System Architecture

### 1. Frontend (React)
- **Technology Stack**: Vite, React 18, Tailwind CSS, SF Pro font.
- **Key Responsibilities**:
    - User Interface for content generation and chat.
    - Real-time streaming response handling using Server-Sent Events (SSE).
    - Client-side format conversion and PDF export management.
    - Authentication state management (JWT).
- **Port**: 5173

### 2. Backend API (Java Spring Boot)
- **Technology Stack**: Java 17, Spring Boot 3.2, Spring Data JPA, Spring Security.
- **Key Responsibilities**:
    - **Authentication**: JWT-based auth with BCrypt password hashing.
    - **User Management**: Profile management and usage statistics.
    - **Persistence**: Managing chat sessions and message history in PostgreSQL.
    - **Rate Limiting**: Enforcing a 10 messages/day limit for free users.
    - **Orchestration**: Proxying requests between the frontend and the AI Service.
- **Port**: 8080

### 3. AI Service (Python FastAPI)
- **Technology Stack**: Python 3.10+, FastAPI, WeasyPrint, PyPDF2.
- **Key Responsibilities**:
    - **Smart Routing**: Mapping content types to the best LLM provider (Groq, Gemini, Together AI, DeepSeek).
    - **Intelligent Fallback**: Automatic provider switching on rate limits or failures.
    - **Content Processing**: Tone, length, and language customization.
    - **Advanced Tools**: Server-side PDF generation and text extraction from uploaded files.
- **Port**: 8000

### 4. Database (PostgreSQL)
- **Hosting**: Supabase.
- **Schema**:
    - `users`: Credentials, profile, and daily message counts.
    - `chat_sessions`: Grouping conversations by content type.
    - `chat_messages`: Storing the full history of user and AI interactions.

## 🔄 Data Flow
1. **User Input**: User submits a prompt via the React frontend.
2. **Auth & Rate Limit**: Spring Boot validates the JWT and checks the user's daily rate limit.
3. **History Retrieval**: Spring Boot fetches the last 5 messages from the database for context.
4. **AI Processing**: Spring Boot calls the Python AI Service.
5. **Smart Routing**: The AI Service selects the optimal LLM provider and streams the response back.
6. **Persistence**: Spring Boot saves the completed AI response and the user's message to the database.
7. **Updates**: The daily message count is incremented for the user.

## 📁 Key Directories
- `/frontend`: React application source code.
- `/backend`: Java Spring Boot application source code.
- `/ai-service`: Python FastAPI application source code.
- `/database`: SQL schema (`schema.sql`) and setup documentation.
- `/docs`: (Implicit) Various markdown files in the root providing implementation details.

## 🛠️ Environment Configuration
Each service requires its own `.env` or configuration file:
- **Frontend**: `VITE_API_BASE_URL`, `VITE_AI_SERVICE_URL`.
- **Backend**: `spring.datasource.url`, `jwt.secret`, `ai.service.url`.
- **AI Service**: `GROQ_API_KEY`, `GEMINI_API_KEY`, `TOGETHER_API_KEY`, `DEEPSEEK_API_KEY`.

---
*Last Updated: 2026-04-28*
