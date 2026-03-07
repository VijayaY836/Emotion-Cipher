# 🚀 Quick Deploy Guide - EMOTION CIPHER

## Fastest Way to Deploy (5 minutes)

### Step 1: Deploy Backend to Railway ⚡

1. **Sign up** at [railway.app](https://railway.app) (free, no credit card)

2. **Click "New Project"** → "Deploy from GitHub repo"

3. **Select this repository**

4. **Configure**:
   - Railway auto-detects Python
   - It will use `backend/requirements.txt`
   - No environment variables needed!

5. **Wait for deployment** (~3-5 minutes for first deploy)
   - Railway will download the ML model (~330MB)
   - Check logs to see progress

6. **Copy your Railway URL**:
   - Example: `https://emotion-cipher-production.up.railway.app`
   - You'll need this for the frontend!

---

### Step 2: Deploy Frontend to Vercel 🎨

1. **Sign up** at [vercel.com](https://vercel.com) (free, no credit card)

2. **Click "Add New Project"** → "Import Git Repository"

3. **Select this repository**

4. **Configure Project**:
   ```
   Framework Preset: Next.js
   Root Directory: frontend
   Build Command: npm run build (auto-detected)
   Output Directory: .next (auto-detected)
   Install Command: npm install (auto-detected)
   ```

5. **Add Environment Variable**:
   - Click "Environment Variables"
   - **Name**: `NEXT_PUBLIC_API_URL`
   - **Value**: Your Railway URL (from Step 1)
   - Example: `https://emotion-cipher-production.up.railway.app`

6. **Click "Deploy"** 🚀

7. **Wait ~2 minutes** for build to complete

8. **Done!** Your app is live at `https://your-app.vercel.app`

---

## Update CORS (Important!)

After deploying, update the backend to allow your Vercel domain:

1. Go to your Railway dashboard
2. Open the deployment
3. Edit `backend/src/main.py`
4. Add your Vercel URL to the CORS origins:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:4000",
        "https://your-app.vercel.app",  # ← Add your Vercel domain here
        "https://*.vercel.app",  # Allow all Vercel preview deployments
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

5. Commit and push - Railway will auto-redeploy

---

## Testing Your Deployment

1. Open your Vercel URL: `https://your-app.vercel.app`
2. Try encrypting a message: "I'm so excited about this hackathon!"
3. Check if emotions are detected
4. Copy the encrypted text
5. Try decrypting it

If everything works - **YOU'RE LIVE!** 🎉

---

## Troubleshooting

### ❌ "Failed to fetch" error
- Check if Railway backend is running (visit the Railway URL directly)
- Verify `NEXT_PUBLIC_API_URL` is set correctly in Vercel
- Make sure CORS is configured with your Vercel domain

### ❌ Backend takes long to respond (first request)
- This is normal! Railway has "cold starts"
- The ML model needs to load (~30 seconds first time)
- Subsequent requests will be fast

### ❌ Build fails on Vercel
- Check Node version (should be 18+)
- Verify all dependencies are in `frontend/package.json`
- Check build logs in Vercel dashboard

### ❌ Backend crashes on Railway
- Check if memory is sufficient (upgrade to 1GB if needed)
- View logs in Railway dashboard
- Model download might have failed - redeploy

---

## Free Tier Limits

✅ **Vercel Free Tier**:
- 100GB bandwidth/month
- Unlimited deployments
- Perfect for hackathons!

✅ **Railway Free Tier**:
- $5 credit/month
- ~500 hours of runtime
- Enough for demos and hackathons!

---

## Alternative: One-Click Deploy

### Deploy Backend to Render

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com)

1. Click the button above
2. Connect your GitHub
3. Select this repo
4. Choose "Web Service"
5. Set:
   - **Build Command**: `pip install -r backend/requirements.txt`
   - **Start Command**: `cd backend && uvicorn src.main:app --host 0.0.0.0 --port $PORT`

---

## Pro Tips 💡

1. **Use Railway for backend** - it handles Python/ML models perfectly
2. **Use Vercel for frontend** - optimized for Next.js
3. **Enable auto-deploy** - push to main branch = instant deployment
4. **Monitor logs** - both platforms have excellent logging
5. **Custom domain** - add your own domain in Vercel settings (free!)

---

## Need Help?

- Check `DEPLOYMENT.md` for detailed instructions
- View logs in Railway/Vercel dashboards
- Test locally first: `npm run dev` (frontend) + `uvicorn src.main:app` (backend)

---

**Ready to impress the judges?** Deploy now and share your live demo link! 🏆
