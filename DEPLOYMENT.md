# 🚀 Deployment Guide - AI Content Generator

Complete guide to deploy all services to free hosting platforms.

## 📋 Deployment Overview

| Service | Platform | Free Tier | Monthly Cost |
|---------|----------|-----------|--------------|
| React Frontend | Vercel | Unlimited | $0 |
| Spring Boot API | Render | 750 hours | $0 |
| Python AI Service | Render | 750 hours | $0 |
| PostgreSQL DB | Supabase | 500 MB | $0 |

**Total Monthly Cost: $0** 🎉

---

## 1️⃣ Deploy Database (Supabase)

### Already Done!
If you followed `database/SUPABASE_SETUP.md`, your database is already deployed and running.

### Verify Deployment
1. Go to [supabase.com](https://supabase.com)
2. Open your project
3. Check "Table Editor" - you should see 3 tables
4. Note your connection details from Settings → Database

---

## 2️⃣ Deploy Python AI Service (Render)

### Prerequisites
- GitHub account
- OpenRouter API key
- Code pushed to GitHub repository

### Steps

1. **Go to [Render](https://render.com)** and sign up

2. **Create New Web Service**
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Select your repository

3. **Configure Service**
   ```
   Name: ai-content-generator-service
   Region: Choose closest to you
   Branch: main
   Root Directory: ai-service
   Runtime: Python 3
   Build Command: pip install -r requirements.txt
   Start Command: uvicorn main:app --host 0.0.0.0 --port $PORT
   ```

4. **Add Environment Variables**
   - Click "Environment" tab
   - Add:
     ```
     OPENROUTER_API_KEY=your_actual_key_here
     ```

5. **Deploy**
   - Click "Create Web Service"
   - Wait 3-5 minutes for deployment
   - Note your service URL: `https://ai-content-generator-service.onrender.com`

6. **Test Deployment**
   ```bash
   curl https://your-service.onrender.com/health
   # Should return: {"status":"healthy"}
   ```

### Important Notes
- Free tier sleeps after 15 minutes of inactivity
- First request after sleep takes 30-60 seconds
- 750 hours/month free (enough for development)

---

## 3️⃣ Deploy Spring Boot Backend (Render)

### Prerequisites
- Python AI service deployed (from step 2)
- Supabase database running (from step 1)

### Steps

1. **Prepare for Deployment**
   
   Update `backend/src/main/resources/application.properties`:
   ```properties
   # Use environment variables for production
   spring.datasource.url=jdbc:postgresql://${SUPABASE_HOST}:5432/${SUPABASE_DB}
   spring.datasource.username=${SUPABASE_USER}
   spring.datasource.password=${SUPABASE_PASSWORD}
   jwt.secret=${JWT_SECRET}
   ai.service.url=${AI_SERVICE_URL}
   ```

2. **Create Render Web Service**
   - Go to Render dashboard
   - Click "New +" → "Web Service"
   - Connect your repository
   - Select your repository

3. **Configure Service**
   ```
   Name: ai-content-generator-backend
   Region: Same as Python service
   Branch: main
   Root Directory: backend
   Runtime: Java
   Build Command: ./mvnw clean package -DskipTests
   Start Command: java -jar target/ai-content-generator-1.0.0.jar
   ```

4. **Add Environment Variables**
   ```
   SUPABASE_HOST=db.xxxxx.supabase.co
   SUPABASE_DB=postgres
   SUPABASE_USER=postgres
   SUPABASE_PASSWORD=your_supabase_password
   JWT_SECRET=your-super-secret-256-bit-key-change-this
   AI_SERVICE_URL=https://your-python-service.onrender.com
   CORS_ORIGINS=https://your-frontend.vercel.app
   ```

5. **Deploy**
   - Click "Create Web Service"
   - Wait 5-10 minutes for first build
   - Note your backend URL: `https://ai-content-generator-backend.onrender.com`

6. **Test Deployment**
   ```bash
   # Test health
   curl https://your-backend.onrender.com/api/auth/validate
   
   # Register test user
   curl -X POST https://your-backend.onrender.com/api/auth/register \
     -H "Content-Type: application/json" \
     -d '{"email":"test@example.com","username":"test","password":"password123"}'
   ```

### Troubleshooting

**Build Fails**:
- Check Java version in `pom.xml` matches Render's Java version
- Ensure `mvnw` has execute permissions: `git update-index --chmod=+x mvnw`

**Database Connection Error**:
- Verify Supabase credentials
- Check if Supabase allows connections from Render IPs (should be allowed by default)

**Service Sleeps**:
- Free tier sleeps after 15 minutes
- Use a cron job to ping every 14 minutes (see below)

---

## 4️⃣ Deploy React Frontend (Vercel)

### Coming Soon
Frontend implementation is pending. Once built, deployment steps will be:

1. Push frontend code to GitHub
2. Go to [Vercel](https://vercel.com)
3. Import repository
4. Configure:
   ```
   Framework: Vite
   Root Directory: frontend
   Build Command: npm run build
   Output Directory: dist
   ```
5. Add environment variable:
   ```
   VITE_API_BASE_URL=https://your-backend.onrender.com/api
   ```
6. Deploy

---

## 🔄 Keep Free Services Awake

Free tier services sleep after 15 minutes of inactivity. Here's how to keep them awake:

### Option 1: Cron Job (Recommended)

Use [cron-job.org](https://cron-job.org) (free):

1. Sign up at cron-job.org
2. Create new cron job:
   - **URL**: `https://your-backend.onrender.com/api/auth/validate`
   - **Schedule**: Every 14 minutes
   - **Method**: GET
3. Create another for Python service:
   - **URL**: `https://your-python-service.onrender.com/health`
   - **Schedule**: Every 14 minutes

### Option 2: UptimeRobot

1. Go to [uptimerobot.com](https://uptimerobot.com)
2. Add monitors for both services
3. Set interval to 5 minutes

### Option 3: GitHub Actions

Create `.github/workflows/keep-alive.yml`:

```yaml
name: Keep Services Awake

on:
  schedule:
    - cron: '*/14 * * * *'  # Every 14 minutes
  workflow_dispatch:

jobs:
  ping:
    runs-on: ubuntu-latest
    steps:
      - name: Ping Python Service
        run: curl https://your-python-service.onrender.com/health
      
      - name: Ping Spring Boot Service
        run: curl https://your-backend.onrender.com/api/auth/validate
```

---

## 🔒 Security Checklist

Before going to production:

- [ ] Change JWT secret to strong random value
- [ ] Update CORS origins to your actual frontend domain
- [ ] Enable HTTPS only (Render does this automatically)
- [ ] Review Supabase security rules
- [ ] Set up database backups
- [ ] Add rate limiting at API gateway level
- [ ] Monitor API usage
- [ ] Set up error tracking (Sentry, etc.)
- [ ] Review and rotate API keys regularly

---

## 📊 Monitoring

### Render Dashboard
- View logs for each service
- Monitor CPU/memory usage
- Check deployment history

### Supabase Dashboard
- Monitor database size
- View query performance
- Check API usage

### Application Logs
- Spring Boot logs available in Render dashboard
- Python logs available in Render dashboard
- Set up log aggregation (optional)

---

## 🔄 CI/CD Setup

### Automatic Deployments

Render automatically deploys when you push to GitHub:

1. Push to `main` branch
2. Render detects changes
3. Builds and deploys automatically
4. Zero downtime deployment

### Manual Deployments

In Render dashboard:
1. Go to your service
2. Click "Manual Deploy"
3. Select branch
4. Click "Deploy"

---

## 💰 Cost Optimization

### Free Tier Limits

**Render**:
- 750 hours/month per service
- Services sleep after 15 minutes
- 100 GB bandwidth/month

**Supabase**:
- 500 MB database storage
- Unlimited API requests
- 2 GB file storage

### Upgrade Paths

When you outgrow free tier:

**Render**:
- Starter: $7/month (no sleep, more resources)
- Standard: $25/month (autoscaling)

**Supabase**:
- Pro: $25/month (8 GB storage, daily backups)

---

## 🐛 Troubleshooting

### Service Won't Start

1. Check logs in Render dashboard
2. Verify environment variables
3. Test locally first
4. Check build command output

### Database Connection Issues

1. Verify Supabase credentials
2. Check connection string format
3. Test with psql locally
4. Check Supabase project status

### CORS Errors

1. Update `CORS_ORIGINS` in backend
2. Redeploy backend
3. Clear browser cache
4. Check browser console for exact error

### Slow First Request

- This is normal for free tier (cold start)
- Service wakes up in 30-60 seconds
- Use keep-alive service to prevent sleep

---

## 📝 Environment Variables Summary

### Python AI Service
```bash
OPENROUTER_API_KEY=sk-or-...
```

### Spring Boot Backend
```bash
SUPABASE_HOST=db.xxxxx.supabase.co
SUPABASE_DB=postgres
SUPABASE_USER=postgres
SUPABASE_PASSWORD=your_password
JWT_SECRET=your-secret-key
AI_SERVICE_URL=https://your-python-service.onrender.com
CORS_ORIGINS=https://your-frontend.vercel.app
```

### React Frontend (Coming Soon)
```bash
VITE_API_BASE_URL=https://your-backend.onrender.com/api
```

---

## ✅ Deployment Checklist

- [ ] Supabase database created and schema executed
- [ ] Python AI service deployed to Render
- [ ] Spring Boot backend deployed to Render
- [ ] Environment variables configured
- [ ] Services tested with cURL
- [ ] CORS configured correctly
- [ ] Keep-alive service set up
- [ ] Monitoring enabled
- [ ] Backups configured
- [ ] Documentation updated with URLs

---

## 🎉 Success!

Your AI Content Generator is now live and accessible worldwide!

**Service URLs**:
- Backend API: `https://your-backend.onrender.com`
- AI Service: `https://your-python-service.onrender.com`
- Database: Supabase (internal)
- Frontend: Coming soon

**Next Steps**:
1. Test all endpoints
2. Build React frontend
3. Deploy frontend to Vercel
4. Share with users!

---

**Need Help?**
- Render Docs: https://render.com/docs
- Supabase Docs: https://supabase.com/docs
- Vercel Docs: https://vercel.com/docs
