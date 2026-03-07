# EMOTION CIPHER - Deployment Guide

## Quick Deploy to Vercel + Railway

### Option 1: Vercel (Frontend) + Railway (Backend) - RECOMMENDED

#### Step 1: Deploy Backend to Railway

1. Go to [Railway.app](https://railway.app)
2. Click "New Project" → "Deploy from GitHub repo"
3. Select your repository
4. Railway will auto-detect the Python backend
5. Add these environment variables in Railway:
   - No special env vars needed for basic deployment
6. Railway will provide a URL like: `https://your-app.railway.app`
7. Copy this URL - you'll need it for the frontend

#### Step 2: Deploy Frontend to Vercel

1. Go to [Vercel.com](https://vercel.com)
2. Click "New Project" → Import your GitHub repository
3. Configure the project:
   - **Framework Preset**: Next.js
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `.next`
4. Add Environment Variable:
   - **Name**: `NEXT_PUBLIC_API_URL`
   - **Value**: Your Railway backend URL (e.g., `https://your-app.railway.app`)
5. Click "Deploy"

Done! Your app will be live at `https://your-app.vercel.app`

---

### Option 2: All-in-One Vercel Deployment (Serverless)

For a simpler deployment, you can deploy both frontend and backend to Vercel using serverless functions.

#### Step 1: Create Vercel Serverless API

Create `frontend/api/` directory and convert Python endpoints to serverless functions.

**Note**: This requires significant refactoring and has limitations:
- Cold starts (slower first request)
- Limited to 50MB deployment size
- 10-second execution timeout
- May not work well with large ML models

#### Step 2: Deploy to Vercel

```bash
cd frontend
vercel
```

---

### Option 3: Render (Full-Stack)

1. Go to [Render.com](https://render.com)
2. Create a new "Web Service" for the backend
3. Create a new "Static Site" for the frontend
4. Connect them via environment variables

---

## Recommended: Railway + Vercel

**Why?**
- Railway handles Python/ML models perfectly
- Vercel optimizes Next.js deployment
- Both have generous free tiers
- Easy to set up and maintain

## Post-Deployment Checklist

- [ ] Backend is accessible at the Railway URL
- [ ] Frontend environment variable `NEXT_PUBLIC_API_URL` is set correctly
- [ ] Test encryption/decryption flow
- [ ] Check emotion detection is working
- [ ] Verify CORS is configured for your Vercel domain

## Troubleshooting

### CORS Errors
Update `backend/src/main.py` to include your Vercel domain:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:4000",
        "https://your-app.vercel.app",  # Add your Vercel domain
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Model Loading Issues on Railway
Railway should handle the HuggingFace model downloads automatically. If issues occur:
- Increase memory allocation in Railway settings
- Check logs for download errors

### Build Failures
- Ensure `frontend/package.json` has all dependencies
- Check Node version compatibility (use Node 18+)
- Verify `next.config.js` is properly configured

## Cost Estimates

**Free Tier Limits:**
- **Vercel**: 100GB bandwidth, unlimited deployments
- **Railway**: $5 free credit/month, ~500 hours
- **Total**: FREE for hackathon/demo purposes!

## Need Help?

Check the logs:
- **Vercel**: Dashboard → Your Project → Deployments → View Logs
- **Railway**: Dashboard → Your Service → Logs

---

**Pro Tip**: For hackathon demos, Railway + Vercel is the fastest and most reliable setup!
