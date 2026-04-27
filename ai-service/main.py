from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import chat
import uvicorn

app = FastAPI(
    title="AI Content Generator Service",
    description="Python FastAPI service for AI content generation using multiple providers (Groq, Gemini, TogetherAI, DeepSeek)",
    version="2.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(chat.router, prefix="/chat", tags=["chat"])

@app.get("/")
async def root():
    return {"message": "AI Content Generator Service is running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "ai-content-generator"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
