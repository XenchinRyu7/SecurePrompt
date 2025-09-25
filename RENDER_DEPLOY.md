# 🚀 Deploy SecurePrompt ke Render.com - GRATIS!

## ⭐ Mengapa Render.com?
- ✅ **100% GRATIS** untuk web services
- ✅ **750 jam/bulan** - lebih dari cukup
- ✅ **Auto-deploy** dari GitHub
- ✅ **HTTPS built-in** gratis
- ✅ **Custom domains** support
- ✅ **Environment variables** support
- ⚠️ **Sleep mode** setelah 15 menit idle (normal untuk free tier)

## 📋 Step-by-Step Deploy

### 1. Persiapan (✅ Sudah Done!)
Repository sudah di GitHub: `XenchinRyu7/SecurePrompt`

### 2. Deploy ke Render

#### A. Buka render.com
1. Kunjungi [render.com](https://render.com)
2. Click **"Get Started for Free"**
3. Sign up dengan GitHub account

#### B. Create New Web Service
1. Click **"New +"** di dashboard
2. Pilih **"Web Service"**
3. Connect GitHub repository: `XenchinRyu7/SecurePrompt`
4. Click **"Connect"**

#### C. Configure Service
```
Name: secureprompt-api
Runtime: Python 3
Build Command: pip install -r requirements.txt
Start Command: uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

#### D. Environment Variables (Optional)
```
ENVIRONMENT=production
API_TITLE=SecurePrompt API
```

#### E. Deploy!
1. Click **"Create Web Service"**
2. Wait 2-3 minutes untuk build & deploy
3. Your API akan available di: `https://secureprompt-api.onrender.com`

## 🧪 Test Deployment

Setelah deploy berhasil, test endpoints:

```bash
# Health check
curl https://secureprompt-api.onrender.com/api/v1/health

# Test sensitive prompt
curl -X POST "https://secureprompt-api.onrender.com/api/v1/check" \
     -H "Content-Type: application/json" \
     -d '{"prompt": "What is my password?"}'

# API Documentation
# Visit: https://secureprompt-api.onrender.com/docs
```

## 📊 Expected Response

### Health Check:
```json
{
  "status": "healthy",
  "message": "SecurePrompt API is running"
}
```

### Sensitive Prompt:
```json
{
  "status": "SENSITIVE",
  "matches": [
    {
      "keyword": "password",
      "position": 11
    }
  ]
}
```

## ⚡ Performance Notes

- **Cold start**: ~10-15 seconds (normal untuk free tier)
- **Warm requests**: <100ms response time
- **Auto-sleep**: Setelah 15 menit idle
- **Auto-wake**: Otomatis saat ada request baru

## 🔄 Auto-Deploy Setup

Render otomatis deploy setiap kali ada push ke main branch:

```bash
# Update code
git add .
git commit -m "Update: improve security detection"
git push origin main

# Render akan auto-deploy dalam 2-3 menit!
```

## 🎯 Production URL Structure

```
Base URL: https://secureprompt-api.onrender.com
Health: https://secureprompt-api.onrender.com/api/v1/health
Check: https://secureprompt-api.onrender.com/api/v1/check
Docs: https://secureprompt-api.onrender.com/docs
```

## 💡 Tips & Tricks

1. **Keep Alive**: Ping health endpoint setiap 10-14 menit untuk avoid sleep
2. **Monitoring**: Use UptimeRobot atau similar untuk monitoring
3. **Custom Domain**: Bisa add custom domain di Render dashboard
4. **Logs**: Check logs di Render dashboard untuk debugging

## 🆓 Free Tier Limits

- ✅ **750 jam/bulan** (25 hari penuh)
- ✅ **Unlimited requests** saat active
- ✅ **1GB RAM** per service
- ✅ **HTTPS** included
- ⚠️ **Sleep** setelah 15 menit idle

---

## 🎉 READY TO DEPLOY!

Repository sudah siap, tinggal:
1. Buka render.com
2. Connect repo `XenchinRyu7/SecurePrompt`
3. Deploy!

**Expected deployment time: 3-5 menit** ⚡