from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import chat, tools, generate, followup, image
import uvicorn

app = FastAPI(
    title="AI Content Generator Service",
    description="Python FastAPI service for AI content generation using multiple providers (Groq, Gemini, TogetherAI, DeepSeek) and Stable Diffusion image generation",
    version="5.1.0"
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
app.include_router(tools.router, tags=["tools"])
app.include_router(generate.router, tags=["generate"])
app.include_router(followup.router, prefix="/followup", tags=["followup"])
app.include_router(image.router, prefix="/image", tags=["image"])

@app.get("/")
async def root():
    return {"message": "AI Content Generator Service is running with image generation support"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "ai-content-generator"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
