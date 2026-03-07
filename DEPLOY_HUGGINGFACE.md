# Deploy EMOTION CIPHER Backend to Hugging Face Spaces

Hugging Face Spaces is PERFECT for ML applications and it's 100% FREE!

## Why Hugging Face Spaces?

- ✅ **FREE forever** (no credit card needed)
- ✅ **Designed for ML models** (your emotion detection model will work perfectly)
- ✅ **No cold starts** (unlike Render/Railway free tiers)
- ✅ **Easy deployment** (just git push)
- ✅ **Persistent storage** for models
- ✅ **Great for hackathons** (judges love HF!)

## Step-by-Step Deployment

### 1. Create Hugging Face Account

1. Go to https://huggingface.co/join
2. Sign up (free account)
3. Verify your email

### 2. Create a New Space

1. Go to https://huggingface.co/spaces
2. Click **"Create new Space"**
3. Fill in:
   - **Owner**: Your username
   - **Space name**: `emotion-cipher-backend`
   - **License**: MIT
   - **Select the Space SDK**: Choose **"Docker"** (gives us full control)
   - **Space hardware**: CPU basic (free)
   - **Visibility**: Public

4. Click **"Create Space"**

### 3. Prepare Backend Files

Create these files in your backend directory:

#### `Dockerfile`
```dockerfile
FROM python:3.10-slim

WORKDIR /app

# Copy requirements
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY src/ ./src/

# Expose port
EXPOSE 7860

# Run the application
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "7860"]
```

#### `README.md` (for the Space)
```markdown
---
title: Emotion Cipher Backend
emoji: 🎭
colorFrom: purple
colorTo: pink
sdk: docker
pinned: false
---

# EMOTION CIPHER Backend API

AI-powered emotion detection and encryption API.

## Endpoints

- POST /api/encrypt - Encrypt message with emotions
- POST /api/decrypt - Decrypt message
- POST /api/analyze - Analyze emotions only

## Documentation

Visit /docs for interactive API documentation.
```

### 4. Deploy to Hugging Face

#### Option A: Using Git (Recommended)

```bash
# Navigate to your backend directory
cd backend

# Initialize git if not already done
git init

# Add Hugging Face Space as remote
git remote add hf https://huggingface.co/spaces/YOUR_USERNAME/emotion-cipher-backend

# Create Dockerfile (copy from above)
# Create README.md (copy from above)

# Add all files
git add .

# Commit
git commit -m "Deploy EMOTION CIPHER backend"

# Push to Hugging Face
git push hf main
```

#### Option B: Using Web Interface

1. In your Space, click **"Files"** tab
2. Click **"Add file"** → **"Upload files"**
3. Upload:
   - `Dockerfile`
   - `README.md`
   - `requirements.txt`
   - All files from `src/` directory
4. Click **"Commit changes to main"**

### 5. Wait for Build

- Hugging Face will automatically build your Docker container
- Watch the **"Logs"** tab to see build progress
- Build takes 2-5 minutes
- When done, you'll see "Running" status

### 6. Test Your Backend

Your backend is now live at:
```
https://YOUR_USERNAME-emotion-cipher-backend.hf.space
```

Test it:
```bash
curl https://YOUR_USERNAME-emotion-cipher-backend.hf.space/docs
```

### 7. Update Vercel Frontend

1. Go to your Vercel project dashboard
2. Click **"Settings"** → **"Environment Variables"**
3. Add or update:
   - **Name**: `NEXT_PUBLIC_API_URL`
   - **Value**: `https://YOUR_USERNAME-emotion-cipher-backend.hf.space`
4. Click **"Save"**
5. Go to **"Deployments"** tab
6. Click **"..."** on latest deployment → **"Redeploy"**

### 8. Update CORS in Backend

Make sure your backend allows requests from Vercel:

In `backend/src/main.py`, update CORS origins:
```python
origins = [
    "http://localhost:4000",
    "http://localhost:3000",
    "https://your-vercel-app.vercel.app",  # Add your Vercel URL
    "https://*.vercel.app",  # Allow all Vercel preview deployments
]
```

Commit and push this change to Hugging Face.

## Done! 🎉

Your app is now fully deployed:
- **Frontend**: Vercel
- **Backend**: Hugging Face Spaces

Both are FREE and production-ready!

## Troubleshooting

### Build Fails

Check `requirements.txt` has all dependencies:
```
fastapi==0.104.1
uvicorn==0.24.0
transformers==4.35.2
torch==2.1.0
pycryptodome==3.19.0
python-multipart==0.0.6
```

### CORS Errors

Make sure CORS origins include your Vercel domain in `main.py`.

### Model Download Issues

Hugging Face Spaces automatically caches models. First run might be slow (2-3 minutes) while downloading the emotion model.

### Port Issues

Hugging Face Spaces MUST use port 7860. Make sure your Dockerfile exposes this port.

## Alternative: Quick Deploy Script

Save this as `deploy-hf.sh`:

```bash
#!/bin/bash

echo "🎭 Deploying EMOTION CIPHER to Hugging Face Spaces..."

# Check if HF username is provided
if [ -z "$1" ]; then
    echo "Usage: ./deploy-hf.sh YOUR_HF_USERNAME"
    exit 1
fi

HF_USERNAME=$1
SPACE_NAME="emotion-cipher-backend"

cd backend

# Create Dockerfile if not exists
if [ ! -f "Dockerfile" ]; then
    cat > Dockerfile << 'EOF'
FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY src/ ./src/
EXPOSE 7860
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "7860"]
EOF
fi

# Add HF remote
git remote add hf https://huggingface.co/spaces/$HF_USERNAME/$SPACE_NAME 2>/dev/null || true

# Commit and push
git add .
git commit -m "Deploy to Hugging Face Spaces"
git push hf main

echo "✅ Deployed! Your backend will be live at:"
echo "https://$HF_USERNAME-$SPACE_NAME.hf.space"
```

Run it:
```bash
chmod +x deploy-hf.sh
./deploy-hf.sh YOUR_HF_USERNAME
```
