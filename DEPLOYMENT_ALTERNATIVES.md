# Alternative Deployment Options for EMOTION CIPHER

Since you're having issues with Railway, here are the best alternatives:

## ✅ RECOMMENDED: Hugging Face Spaces + Vercel (100% FREE)

This is the BEST option for ML applications!

### Step 1: Deploy Backend to Hugging Face Spaces

1. Go to https://huggingface.co/spaces
2. Click "Create new Space"
3. Choose:
   - **Space name**: `emotion-cipher-backend`
   - **License**: MIT
   - **Space SDK**: Gradio (we'll use FastAPI)
   - **Visibility**: Public

4. Clone your space locally:
```bash
git clone https://huggingface.co/spaces/YOUR_USERNAME/emotion-cipher-backend
cd emotion-cipher-backend
```

5. Copy backend files:
```bash
# Copy all backend files
cp -r ../backend/* .
```

6. Create `app.py` in the space root:
```python
import uvicorn
from src.main import app

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=7860)
```

7. Create `requirements.txt` in space root (copy from backend/requirements.txt)

8. Push to Hugging Face:
```bash
git add .
git commit -m "Deploy EMOTION CIPHER backend"
git push
```

9. Your backend will be live at: `https://YOUR_USERNAME-emotion-cipher-backend.hf.space`

### Step 2: Update Vercel Frontend

1. In your Vercel project settings, add environment variable:
   - **Name**: `NEXT_PUBLIC_API_URL`
   - **Value**: `https://YOUR_USERNAME-emotion-cipher-backend.hf.space`

2. Redeploy your Vercel app

---

## Option 2: Render.com (Railway Alternative)

Render has better GitHub integration than Railway.

### Deploy Backend to Render

1. Go to https://render.com
2. Sign up with GitHub
3. Click "New +" → "Web Service"
4. Connect your GitHub repository
5. Configure:
   - **Name**: `emotion-cipher-backend`
   - **Root Directory**: `backend`
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn src.main:app --host 0.0.0.0 --port $PORT`
   - **Plan**: Free

6. Add environment variable:
   - **Key**: `ALLOWED_ORIGINS`
   - **Value**: `https://your-vercel-app.vercel.app`

7. Click "Create Web Service"

8. Copy your Render URL (e.g., `https://emotion-cipher-backend.onrender.com`)

9. Update Vercel environment variable:
   - `NEXT_PUBLIC_API_URL` = your Render URL

---

## Option 3: PythonAnywhere (Simplest for Python)

1. Go to https://www.pythonanywhere.com
2. Sign up for free account
3. Go to "Web" tab → "Add a new web app"
4. Choose "Manual configuration" → Python 3.10
5. Upload your backend files
6. Configure WSGI file to run FastAPI
7. Enable CORS for your Vercel domain

---

## Option 4: Fly.io (Modern Alternative)

1. Install Fly CLI:
```bash
curl -L https://fly.io/install.sh | sh
```

2. Login:
```bash
fly auth login
```

3. Create `fly.toml` in backend directory:
```toml
app = "emotion-cipher-backend"

[build]
  builder = "paketobuildpacks/builder:base"

[env]
  PORT = "8080"

[[services]]
  http_checks = []
  internal_port = 8080
  protocol = "tcp"

  [[services.ports]]
    force_https = true
    handlers = ["http"]
    port = 80

  [[services.ports]]
    handlers = ["tls", "http"]
    port = 443
```

4. Deploy:
```bash
cd backend
fly launch
fly deploy
```

---

## Option 5: Run Backend Locally (For Demo/Testing)

If you just need it for a demo or testing:

1. Keep backend running on your local machine:
```bash
cd backend
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

2. Use ngrok to expose it:
```bash
# Install ngrok from https://ngrok.com
ngrok http 8000
```

3. Copy the ngrok URL (e.g., `https://abc123.ngrok.io`)

4. Update Vercel environment variable:
   - `NEXT_PUBLIC_API_URL` = your ngrok URL

**Note**: ngrok URLs change each time, so this is only for temporary demos.

---

## Troubleshooting Railway

If you want to try Railway again:

1. **GitHub Permission Issue**:
   - Go to https://github.com/settings/installations
   - Find "Railway" in the list
   - Click "Configure"
   - Grant access to your repository

2. **Alternative**: Deploy without GitHub:
   - Install Railway CLI: `npm i -g @railway/cli`
   - Login: `railway login`
   - Link project: `railway link`
   - Deploy: `cd backend && railway up`

---

## My Recommendation

For a hackathon project, I recommend:

1. **Best for ML apps**: Hugging Face Spaces (free, designed for ML, no cold starts)
2. **Best for general apps**: Render.com (free tier, easy setup)
3. **Quick demo**: ngrok + local backend (instant, no deployment needed)

Choose based on your needs!
