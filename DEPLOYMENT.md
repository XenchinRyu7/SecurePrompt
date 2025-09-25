# 🚀 SecurePrompt Deployment Guide

## Platform Deployment Gratis Terbaik

### 1. Render.com (Recommended) ⭐
**Pros**: 100% GRATIS, 750 jam/bulan, HTTPS built-in, auto-deploy
**Cons**: Sleep mode setelah 15 menit idle (normal untuk free tier)

#### Steps:
1. **GitHub Ready**: ✅ Sudah ada di `XenchinRyu7/SecurePrompt`

2. **Deploy di Render**:
   - Buka [render.com](https://render.com)
   - Sign up dengan GitHub
   - Create "Web Service" → Connect repo
   - Configure:
     ```
     Build Command: pip install -r requirements.txt
     Start Command: uvicorn app.main:app --host 0.0.0.0 --port $PORT
     ```
   - Deploy! (2-3 menit)

3. **Result**: `https://your-app.onrender.com`

**📖 Detailed Guide**: [RENDER_DEPLOY.md](RENDER_DEPLOY.md)

---

### 2. Railway (No Longer Free) ❌
**Status**: Tidak lagi gratis sejak 2023
**Pricing**: Mulai dari $5/bulan
**Alternative**: Gunakan Render.com

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