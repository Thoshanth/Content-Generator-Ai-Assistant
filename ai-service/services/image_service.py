"""
Stable Diffusion Image Generation Service
Handles image generation using Stability AI API or local Stable Diffusion models.
"""

import httpx
import base64
import os
import time
import uuid
from typing import Dict, Optional
import logging

logger = logging.getLogger(__name__)

# Configuration
STABILITY_API_KEY = os.getenv("STABILITY_API_KEY")
STABILITY_API_URL = "https://api.stability.ai/v1/generation/stable-diffusion-xl-1024-v1-0/text-to-image"
IMAGE_STORAGE_PATH = os.getenv("IMAGE_STORAGE_PATH", "./generated_images")

# Style prompts to enhance generation
STYLE_PROMPTS = {
    "realistic": "photorealistic, high quality, detailed, professional photography",
    "artistic": "artistic, creative, expressive, masterpiece",
    "anime": "anime style, manga, japanese animation, cel shading",
    "digital_art": "digital art, concept art, artstation, trending",
    "oil_painting": "oil painting, traditional art, canvas, brushstrokes",
    "watercolor": "watercolor painting, soft colors, flowing, artistic",
    "sketch": "pencil sketch, drawing, black and white, artistic lines",
    "cyberpunk": "cyberpunk, neon lights, futuristic, sci-fi, dark atmosphere"
}

# Ensure image storage directory exists
os.makedirs(IMAGE_STORAGE_PATH, exist_ok=True)


async def generate_image(
    prompt: str,
    negative_prompt: Optional[str] = None,
    width: int = 512,
    height: int = 512,
    steps: int = 30,
    guidance_scale: float = 7.5,
    style: Optional[str] = None,
    user_id: Optional[str] = None
) -> Dict:
    """
    Generate image using Stable Diffusion.
    
    Args:
        prompt: Text description of the image to generate
        negative_prompt: What to avoid in the image
        width: Image width (must be multiple of 64)
        height: Image height (must be multiple of 64)
        steps: Number of inference steps (15-50)
        guidance_scale: How closely to follow the prompt (1-20)
        style: Style preset to apply
        user_id: User ID for tracking
    
    Returns:
        Dict with image_url, model_used, generation_time, and seed
    """
    start_time = time.time()
    
    try:
        # Enhance prompt with style
        enhanced_prompt = prompt
        if style and style in STYLE_PROMPTS:
            enhanced_prompt = f"{prompt}, {STYLE_PROMPTS[style]}"
        
        # Default negative prompt
        if not negative_prompt:
            negative_prompt = "blurry, low quality, distorted, deformed, ugly, bad anatomy, extra limbs"
        
        # Validate dimensions for SDXL model (must be specific ratios)
        # SDXL allowed dimensions: 1024x1024, 1152x896, 1216x832, 1344x768, 1536x640, 640x1536, 768x1344, 832x1216, 896x1152
        valid_dimensions = [
            (1024, 1024), (1152, 896), (1216, 832), (1344, 768), (1536, 640),
            (640, 1536), (768, 1344), (832, 1216), (896, 1152)
        ]
        
        # Find the closest valid dimension
        target_area = width * height
        best_match = min(valid_dimensions, key=lambda d: abs(d[0] * d[1] - target_area))
        width, height = best_match
        
        # Clamp values to reasonable ranges
        steps = max(10, min(50, steps))
        guidance_scale = max(1.0, min(20.0, guidance_scale))
        
        logger.info(f"Generating image: {enhanced_prompt[:100]}... ({width}x{height}, {steps} steps)")
        
        if STABILITY_API_KEY and STABILITY_API_KEY.strip():
            # Use Stability AI API
            logger.info("Using Stability AI API for image generation")
            result = await _generate_with_stability_ai(
                enhanced_prompt, negative_prompt, width, height, steps, guidance_scale
            )
        else:
            # Fallback to mock generation for development
            logger.warning("No Stability API key found or empty, using mock generation")
            result = await _generate_mock_image(
                enhanced_prompt, width, height
            )
        
        generation_time = time.time() - start_time
        
        return {
            "imageUrl": result["imageUrl"],
            "modelUsed": result["modelUsed"],
            "generationTime": round(generation_time, 2),
            "seed": result.get("seed"),
            "prompt_used": enhanced_prompt
        }
        
    except Exception as e:
        logger.error(f"Image generation failed: {str(e)}")
        raise Exception(f"Image generation failed: {str(e)}")


async def _generate_with_stability_ai(
    prompt: str,
    negative_prompt: str,
    width: int,
    height: int,
    steps: int,
    guidance_scale: float
) -> Dict:
    """Generate image using Stability AI API."""
    
    headers = {
        "Authorization": f"Bearer {STABILITY_API_KEY}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    
    payload = {
        "text_prompts": [
            {"text": prompt, "weight": 1.0},
            {"text": negative_prompt, "weight": -1.0}
        ],
        "cfg_scale": guidance_scale,
        "height": height,
        "width": width,
        "steps": steps,
        "samples": 1,
        "style_preset": "enhance"
    }
    
    async with httpx.AsyncClient(timeout=120.0) as client:
        response = await client.post(STABILITY_API_URL, headers=headers, json=payload)
        
        if response.status_code != 200:
            error_msg = f"Stability AI API error: {response.status_code} - {response.text}"
            logger.error(error_msg)
            raise Exception(error_msg)
        
        data = response.json()
        
        # Save the generated image
        image_data = data["artifacts"][0]
        image_base64 = image_data["base64"]
        seed = image_data.get("seed")
        
        # Generate unique filename
        image_id = str(uuid.uuid4())
        filename = f"{image_id}.png"
        filepath = os.path.join(IMAGE_STORAGE_PATH, filename)
        
        # Decode and save image
        image_bytes = base64.b64decode(image_base64)
        with open(filepath, "wb") as f:
            f.write(image_bytes)
        
        # Return relative URL (will be served by backend)
        image_url = f"/api/images/{filename}"
        
        return {
            "imageUrl": image_url,
            "modelUsed": "stable-diffusion-xl-1024-v1-0",
            "seed": seed
        }


async def _generate_mock_image(prompt: str, width: int, height: int) -> Dict:
    """Generate a mock image for development/testing."""
    
    # Create a simple colored rectangle as placeholder
    from PIL import Image, ImageDraw, ImageFont
    import hashlib
    
    # Generate consistent color based on prompt
    color_hash = hashlib.md5(prompt.encode()).hexdigest()
    r = int(color_hash[0:2], 16)
    g = int(color_hash[2:4], 16)
    b = int(color_hash[4:6], 16)
    
    # Create image
    image = Image.new('RGB', (width, height), color=(r, g, b))
    draw = ImageDraw.Draw(image)
    
    # Add text overlay
    try:
        # Try to use a default font
        font = ImageFont.load_default()
    except:
        font = None
    
    text = f"Mock Image\n{prompt[:50]}..."
    if font:
        draw.multiline_text((10, 10), text, fill=(255, 255, 255), font=font)
    
    # Save mock image
    image_id = str(uuid.uuid4())
    filename = f"{image_id}.png"
    filepath = os.path.join(IMAGE_STORAGE_PATH, filename)
    image.save(filepath)
    
    image_url = f"/api/images/{filename}"
    
    return {
        "imageUrl": image_url,
        "modelUsed": "mock-stable-diffusion",
        "seed": 12345
    }


def get_image_path(filename: str) -> str:
    """Get full path to generated image file."""
    return os.path.join(IMAGE_STORAGE_PATH, filename)


def cleanup_old_images(max_age_hours: int = 24):
    """Clean up old generated images to save disk space."""
    import glob
    import time
    
    cutoff_time = time.time() - (max_age_hours * 3600)
    
    for filepath in glob.glob(os.path.join(IMAGE_STORAGE_PATH, "*.png")):
        if os.path.getctime(filepath) < cutoff_time:
            try:
                os.remove(filepath)
                logger.info(f"Cleaned up old image: {filepath}")
            except Exception as e:
                logger.error(f"Failed to clean up image {filepath}: {e}")