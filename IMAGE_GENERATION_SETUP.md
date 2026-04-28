# Image Generation with Stable Diffusion - Setup Guide

This guide explains how to set up and use the new image generation feature powered by Stable Diffusion in your AI Content Generator application.

## 🎨 Features Added

- **Stable Diffusion Integration**: Generate high-quality images from text prompts
- **Daily Limits**: 5 images per day for free users (configurable)
- **Multiple Styles**: Realistic, artistic, anime, digital art, oil painting, watercolor, sketch, cyberpunk
- **Size Presets**: Portrait, landscape, square, high quality, fast generation
- **Advanced Controls**: Negative prompts, steps, guidance scale, custom dimensions
- **Image Management**: Download generated images, view in chat history
- **Usage Tracking**: Real-time usage counter with daily reset

## 🏗️ Architecture Overview

### AI Service (Python FastAPI)
- **New Router**: `ai-service/routers/image.py` - Image generation endpoints
- **Service Layer**: `ai-service/services/image_service.py` - Stable Diffusion integration
- **Models**: Extended `ai-service/models/schemas.py` with image request/response schemas
- **Storage**: Local image storage with cleanup utilities

### Backend (Java Spring Boot)
- **Controller**: `ImageController.java` - REST API for image generation
- **Service**: `ImageService.java` - Business logic and AI service proxy
- **Models**: Extended `User.java` and `ChatMessage.java` for image tracking
- **Rate Limiting**: Daily image generation limits with automatic reset

### Frontend (React)
- **Components**: 
  - `ImageGenerator.jsx` - Modal for image generation with advanced options
  - Updated `MessageBubble.jsx` - Display generated images with download
  - Updated `InputBar.jsx` - Image generation button
- **Integration**: Seamless chat integration with image messages

## 🚀 Setup Instructions

### 1. AI Service Setup

1. **Install Dependencies**:
   ```bash
   cd ai-service
   pip install -r requirements.txt
   ```

2. **Configure Stability AI** (Optional - for production):
   - Get API key from [Stability AI](https://platform.stability.ai/)
   - Add to `ai-service/.env`:
   ```env
   STABILITY_API_KEY=your_stability_api_key_here
   IMAGE_STORAGE_PATH=./generated_images
   ```

3. **Create Storage Directory**:
   ```bash
   mkdir ai-service/generated_images
   ```

### 2. Backend Setup

1. **Update Configuration**:
   - Backend `.env` already configured with:
   ```env
   IMAGE_DAILY_LIMIT=5
   IMAGE_STORAGE_PATH=./generated_images
   ```

2. **Create Storage Directory**:
   ```bash
   mkdir backend/generated_images
   ```

3. **Database Migration**:
   - The `User` model now includes:
     - `dailyImageCount`: Track daily image generations
     - `lastImageDate`: Track last image generation date
   - The `ChatMessage` model now includes:
     - `messageType`: "text", "image", or "image_request"
     - `imageUrl`: URL to generated image
     - `imagePrompt`: Original prompt used
     - `imageModel`: Model used for generation
     - `imageParameters`: Generation parameters

### 3. Frontend Setup

No additional setup required - components are already integrated.

## 🎯 Usage Guide

### For Users

1. **Access Image Generation**:
   - Click the purple image button in the chat input area
   - Or use the image generation modal

2. **Generate Images**:
   - Enter a descriptive prompt (e.g., "A beautiful sunset over mountains")
   - Choose a style (realistic, artistic, anime, etc.)
   - Select size preset (portrait, landscape, square, etc.)
   - Optionally configure advanced settings
   - Click "Generate Image"

3. **Advanced Options**:
   - **Negative Prompt**: Specify what to avoid (e.g., "blurry, low quality")
   - **Steps**: Control generation quality (10-50, higher = better quality)
   - **Guidance Scale**: How closely to follow prompt (1-20, higher = more adherence)
   - **Custom Dimensions**: Set exact width/height (must be multiples of 64)

4. **Daily Limits**:
   - Free users: 5 images per day
   - Counter resets at midnight
   - Usage displayed in generation modal

5. **Image Management**:
   - Generated images appear in chat history
   - Hover over images to see download button
   - Images include generation metadata (model, time, dimensions)

### For Developers

#### API Endpoints

**Generate Image**:
```http
POST /api/images/generate
Authorization: Bearer <token>
Content-Type: application/json

{
  "prompt": "A beautiful sunset over mountains",
  "negativePrompt": "blurry, low quality",
  "width": 768,
  "height": 512,
  "steps": 30,
  "guidanceScale": 7.5,
  "style": "realistic"
}
```

**Get Usage**:
```http
GET /api/images/usage
Authorization: Bearer <token>
```

**Get Styles**:
```http
GET /api/images/styles
```

**Get Presets**:
```http
GET /api/images/presets
```

**Serve Images**:
```http
GET /api/images/{filename}
```

#### Configuration Options

**AI Service** (`ai-service/.env`):
```env
STABILITY_API_KEY=your_api_key_here
IMAGE_STORAGE_PATH=./generated_images
```

**Backend** (`backend/.env`):
```env
IMAGE_DAILY_LIMIT=5
IMAGE_STORAGE_PATH=./generated_images
```

## 🔧 Development Mode

Without a Stability AI API key, the system uses mock image generation:
- Creates colored placeholder images with prompt text
- Useful for development and testing
- Same API interface as production

## 🎨 Style Guide

### Available Styles
- **Realistic**: Photorealistic images
- **Artistic**: Creative and expressive
- **Anime**: Japanese animation style
- **Digital Art**: Modern digital artwork
- **Oil Painting**: Traditional oil painting
- **Watercolor**: Soft watercolor style
- **Sketch**: Pencil sketch style
- **Cyberpunk**: Futuristic sci-fi style

### Size Presets
- **Portrait**: 512×768 (2:3 ratio)
- **Landscape**: 768×512 (3:2 ratio)
- **Square**: 512×512 (1:1 ratio)
- **High Quality**: 768×768 (detailed)
- **Fast**: 512×512 (quick generation)

## 🛡️ Security & Limits

### Rate Limiting
- **Daily Limit**: 5 images per user per day
- **Automatic Reset**: Counters reset at midnight
- **Graceful Handling**: Clear error messages when limits reached

### Content Safety
- **Prompt Filtering**: Consider implementing content filters for prompts
- **Image Moderation**: Consider adding image content moderation
- **Storage Limits**: Automatic cleanup of old images (configurable)

### Performance
- **Image Storage**: Local filesystem storage (consider cloud storage for production)
- **Generation Time**: Typically 5-15 seconds per image
- **Concurrent Limits**: Consider adding queue system for high load

## 🚀 Production Deployment

### Stability AI Setup
1. Sign up at [Stability AI Platform](https://platform.stability.ai/)
2. Get API key and add to environment variables
3. Configure billing and usage limits

### Storage Considerations
- **Local Storage**: Good for development and small deployments
- **Cloud Storage**: Recommended for production (AWS S3, Google Cloud Storage)
- **CDN**: Consider CDN for image serving

### Monitoring
- **Usage Tracking**: Monitor daily image generation counts
- **Error Handling**: Log generation failures and API errors
- **Performance**: Monitor generation times and success rates

## 🎉 What's Next?

### Potential Enhancements
- **Image Editing**: Add image-to-image generation
- **Batch Generation**: Generate multiple variations
- **Custom Models**: Support for fine-tuned models
- **Image History**: Dedicated image gallery
- **Sharing**: Share generated images with others
- **Templates**: Pre-made prompt templates

### Integration Ideas
- **Content Generation**: Use images in blog posts and social media
- **Brand Assets**: Generate logos and marketing materials
- **Presentations**: Create custom illustrations
- **Social Media**: Generate post images automatically

## 📞 Support

If you encounter issues:
1. Check the console logs for detailed error messages
2. Verify API keys and configuration
3. Ensure storage directories exist and are writable
4. Check daily limits and usage counters

The image generation feature is now fully integrated and ready to use! 🎨✨