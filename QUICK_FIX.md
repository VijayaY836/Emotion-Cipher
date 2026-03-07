# QUICK FIX: Get Your Vercel App Working NOW

If you need your app working immediately for a demo, here's the fastest solution:

## Option 1: Use ngrok (5 minutes)

This exposes your local backend to the internet temporarily.

### Step 1: Install ngrok

**Windows:**
1. Download from https://ngrok.com/download
2. Extract the zip file
3. Move `ngrok.exe` to a folder in your PATH, or just run it from the download folder

**Or use Chocolatey:**
```bash
choco install ngrok
```

### Step 2: Sign up for ngrok (free)

1. Go to https://dashboard.ngrok.com/signup
2. Sign up (free account)
3. Copy your authtoken from https://dashboard.ngrok.com/get-started/your-authtoken

### Step 3: Configure ngrok

```bash
ngrok config add-authtoken YOUR_AUTH_TOKEN
```

### Step 4: Start Your Backend

```bash
cd backend
venv\Scripts\activate
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

### Step 5: Expose with ngrok (in a NEW terminal)

```bash
ngrok http 8000
```

You'll see output like:
```
Forwarding   https://abc123.ngrok-free.app -> http://localhost:8000
```

### Step 6: Update Vercel

1. Copy the `https://abc123.ngrok-free.app` URL
2. Go to Vercel project → Settings → Environment Variables
3. Update `NEXT_PUBLIC_API_URL` to your ngrok URL
4. Redeploy your Vercel app

### Done! Your app works now! 🎉

**Note**: The ngrok URL changes every time you restart ngrok (unless you have a paid plan). This is perfect for demos and testing!

---

## Option 2: Use Render.com (15 minutes)

Render is easier than Railway and has better GitHub integration.

### Step 1: Sign Up

1. Go to https://render.com
2. Click "Get Started for Free"
3. Sign up with GitHub

### Step 2: Grant GitHub Access

1. During signup, Render will ask for GitHub permissions
2. Click "Authorize Render"
3. Select "All repositories" or just your emotion-cipher repo

### Step 3: Create Web Service

1. Click "New +" → "Web Service"
2. Click "Connect" next to your emotion-cipher repository
3. Configure:
   - **Name**: `emotion-cipher-backend`
   - **Region**: Oregon (US West)
   - **Branch**: main
   - **Root Directory**: `backend`
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn src.main:app --host 0.0.0.0 --port $PORT`
   - **Instance Type**: Free

4. Click "Advanced" and add environment variable:
   - **Key**: `ALLOWED_ORIGINS`
   - **Value**: `https://your-vercel-app.vercel.app,https://*.vercel.app`

5. Click "Create Web Service"

### Step 4: Wait for Deploy

- First deploy takes 5-10 minutes
- Watch the logs to see progress
- When done, you'll see your URL (e.g., `https://emotion-cipher-backend.onrender.com`)

### Step 5: Update Vercel

1. Copy your Render URL
2. Go to Vercel → Settings → Environment Variables
3. Update `NEXT_PUBLIC_API_URL` to your Render URL
4. Redeploy

### Step 6: Update CORS

Update `backend/src/main.py`:
```python
origins = [
    "http://localhost:4000",
    "https://your-vercel-app.vercel.app",
    "https://*.vercel.app",
]
```

Commit and push to GitHub. Render will auto-deploy.

---

## Option 3: Use Hugging Face Spaces (Best for ML)

See [DEPLOY_HUGGINGFACE.md](DEPLOY_HUGGINGFACE.md) for detailed instructions.

This is the BEST long-term solution for ML apps!

---

## Which Should You Choose?

| Solution | Setup Time | Cost | Best For |
|----------|------------|------|----------|
| **ngrok** | 5 min | Free | Quick demos, testing |
| **Render** | 15 min | Free | Production, easy setup |
| **HF Spaces** | 20 min | Free | ML apps, no cold starts |

**My recommendation:**
- **Right now for demo**: Use ngrok
- **For hackathon submission**: Use Render or Hugging Face Spaces

---

## Troubleshooting

### "Cannot connect to backend"

1. Check if backend is running (visit backend URL in browser)
2. Check Vercel environment variable is set correctly
3. Check CORS settings in backend
4. Check browser console for errors

### "CORS error"

Update `backend/src/main.py` to include your Vercel domain in allowed origins.

### "502 Bad Gateway" on Render

Backend is still starting up. Wait 2-3 minutes and try again.

---

Need help? Check the logs:
- **ngrok**: Terminal where ngrok is running
- **Render**: Logs tab in Render dashboard
- **Vercel**: Deployments → Click deployment → View Function Logs
