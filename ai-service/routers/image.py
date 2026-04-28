from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from models.schemas import ImageRequest, ImageResponse
from services.image_service import generate_image
import logging

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/generate")
async def generate_image_endpoint(request: ImageRequest):
    """
    Generate image using Stable Diffusion.
    
    Supports:
    - Text-to-image generation
    - Multiple image sizes
    - Style presets
    - Negative prompts
    """
    try:
        logger.info(f"Image generation request for user {request.user_id}: {request.prompt[:100]}...")
        
        # Generate image using Stable Diffusion
        result = await generate_image(
            prompt=request.prompt,
            negative_prompt=request.negative_prompt,
            width=request.width,
            height=request.height,
            steps=request.steps,
            guidance_scale=request.guidance_scale,
            style=request.style,
            user_id=request.user_id
        )
        
        return ImageResponse(
            imageUrl=result["imageUrl"],
            prompt=request.prompt,
            modelUsed=result["modelUsed"],
            generationTime=result["generationTime"],
            seed=result.get("seed"),
            parameters={
                "width": request.width,
                "height": request.height,
                "steps": request.steps,
                "guidance_scale": request.guidance_scale,
                "style": request.style,
                "negative_prompt": request.negative_prompt
            }
        )
        
    except Exception as e:
        logger.error(f"Image generation failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Image generation failed: {str(e)}")


@router.get("/styles")
async def get_available_styles():
    """Get list of available image styles."""
    styles = [
        {"id": "realistic", "name": "Realistic", "description": "Photorealistic images"},
        {"id": "artistic", "name": "Artistic", "description": "Artistic and creative style"},
        {"id": "anime", "name": "Anime", "description": "Anime and manga style"},
        {"id": "digital_art", "name": "Digital Art", "description": "Digital artwork style"},
        {"id": "oil_painting", "name": "Oil Painting", "description": "Traditional oil painting style"},
        {"id": "watercolor", "name": "Watercolor", "description": "Watercolor painting style"},
        {"id": "sketch", "name": "Sketch", "description": "Pencil sketch style"},
        {"id": "cyberpunk", "name": "Cyberpunk", "description": "Futuristic cyberpunk style"}
    ]
    
    return {"styles": styles}


@router.get("/presets")
async def get_image_presets():
    """Get predefined image generation presets."""
    presets = {
        "portrait": {
            "width": 512,
            "height": 768,
            "steps": 30,
            "guidance_scale": 7.5,
            "description": "Portrait orientation (2:3 ratio)"
        },
        "landscape": {
            "width": 768,
            "height": 512,
            "steps": 30,
            "guidance_scale": 7.5,
            "description": "Landscape orientation (3:2 ratio)"
        },
        "square": {
            "width": 512,
            "height": 512,
            "steps": 25,
            "guidance_scale": 7.0,
            "description": "Square format (1:1 ratio)"
        },
        "high_quality": {
            "width": 768,
            "height": 768,
            "steps": 50,
            "guidance_scale": 8.0,
            "description": "High quality, more detailed generation"
        },
        "fast": {
            "width": 512,
            "height": 512,
            "steps": 15,
            "guidance_scale": 6.0,
            "description": "Fast generation with fewer steps"
        }
    }
    
    return {"presets": presets}