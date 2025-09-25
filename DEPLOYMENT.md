# 🚀 SecurePrompt Deployment Guide

## Platform Deployment Gratis Terbaik

### 1. Railway (Recommended) ⭐
**Pros**: Easy setup, generous free tier, auto-deploy
**Free tier**: 500 jam/bulan + $5 credit

#### Steps:
1. **Push ke GitHub**:
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/username/secureprompt.git
   git push -u origin main
   ```

2. **Deploy di Railway**:
   - Buka [railway.app](https://railway.app)
   - Login dengan GitHub
   - Click "New Project" → "Deploy from GitHub repo"
   - Pilih repository SecurePrompt
   - Railway akan auto-detect Python dan deploy!

3. **Environment Variables** (optional):
   - Set `PORT=8000` jika diperlukan

---

### 2. Render
**Pros**: 750 jam gratis/bulan, HTTPS built-in
**Cons**: Sleep mode setelah 15 menit idle

#### Steps:
1. Push code ke GitHub
2. Buka [render.com](https://render.com)
3. Connect GitHub repo
4. Set build command: `pip install -r requirements.txt`
5. Set start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

---

### 3. Fly.io
**Pros**: Fast global deployment, good free tier

#### Steps:
1. Install flyctl: `curl -L https://fly.io/install.sh | sh`
2. Login: `flyctl auth login`
3. Launch: `flyctl launch`
4. Deploy: `flyctl deploy`

---

## Files untuk Deployment

Project sudah include:
- ✅ `Dockerfile` - untuk containerized deployment
- ✅ `Procfile` - untuk Heroku-style platforms
- ✅ `railway.json` - Railway configuration
- ✅ `requirements.txt` - Python dependencies

## Testing Deployment

Setelah deploy, test endpoints:
- `GET /` - Root endpoint
- `GET /api/v1/health` - Health check
- `POST /api/v1/check` - Main functionality
- `GET /docs` - Swagger UI

## Environment Variables

Untuk production, consider menambah:
```
PORT=8000
ENVIRONMENT=production
```

## Quick Deploy Commands

### Railway:
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login and deploy
railway login
railway link
railway up
```

### Render:
Upload ke GitHub, lalu connect di dashboard Render.

### Fly.io:
```bash
flyctl launch
flyctl deploy
```

---

## 🎯 Recommendation: Railway

Railway adalah pilihan terbaik karena:
- ✅ Setup paling mudah (1 click deploy)
- ✅ Free tier generous (500 jam)
- ✅ Auto-scaling
- ✅ Built-in monitoring
- ✅ Custom domains
- ✅ Database add-ons available

Cukup push ke GitHub dan connect ke Railway! 🚀