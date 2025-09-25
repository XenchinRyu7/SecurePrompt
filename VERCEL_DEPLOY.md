# 🚀 Deploy SecurePrompt ke Vercel - 100% GRATIS!

## ⭐ Mengapa Vercel?
- ✅ **100% GRATIS** tanpa kartu kredit
- ✅ **Unlimited bandwidth** untuk personal projects
- ✅ **Auto-deploy** dari GitHub
- ✅ **Global CDN** dengan edge functions
- ✅ **HTTPS** built-in
- ✅ **Custom domains** gratis
- ✅ **No sleep mode** - always available!

## 📋 Step-by-Step Deploy

### 1. Persiapan (✅ Sudah Done!)
- Repository: `XenchinRyu7/SecurePrompt`
- Vercel config: `vercel.json` ✅
- API handler: `api/index.py` ✅

### 2. Deploy ke Vercel

#### A. Signup Vercel
1. Buka [vercel.com](https://vercel.com)
2. Klik **"Start Deploying"**
3. **Continue with GitHub** (no credit card needed!)
4. Authorize Vercel to access GitHub

#### B. Import Project
1. Di dashboard Vercel, klik **"New Project"**
2. Import dari GitHub: `XenchinRyu7/SecurePrompt`
3. Klik **"Import"**

#### C. Configure Project (Auto-detected!)
```
Framework Preset: Other
Root Directory: ./
Build Command: (leave empty)
Output Directory: (leave empty)
Install Command: pip install -r requirements.txt
```

#### D. Deploy!
1. Klik **"Deploy"**
2. Wait 1-2 menit untuk build & deploy
3. Your API akan available di: `https://secure-prompt-xxx.vercel.app`

## 🌐 API Endpoints

Setelah deploy, API akan tersedia di:

```
Base URL: https://your-project.vercel.app
Root: https://your-project.vercel.app/api
Health: https://your-project.vercel.app/api/health
Check: https://your-project.vercel.app/api/check
Keywords: https://your-project.vercel.app/api/keywords
```

## 🧪 Test Deployment

### 1. Health Check
```bash
curl https://your-project.vercel.app/api/health
```

Expected response:
```json
{
  "status": "healthy",
  "message": "SecurePrompt API is running on Vercel"
}
```

### 2. Test Prompt Check
```bash
curl -X POST "https://your-project.vercel.app/api/check" \
     -H "Content-Type: application/json" \
     -d '{"prompt": "What is my password?"}'
```

Expected response:
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

### 3. Safe Prompt Test
```bash
curl -X POST "https://your-project.vercel.app/api/check" \
     -H "Content-Type: application/json" \
     -d '{"prompt": "What is the weather today?"}'
```

Expected response:
```json
{
  "status": "SAFE",
  "matches": [],
  "response": "LLM response: What is the weather today?"
}
```

## ⚡ Performance & Limits

### Vercel Free Tier:
- ✅ **100GB bandwidth/month**
- ✅ **100 serverless function invocations/day** (reset daily)
- ✅ **10 second function timeout**
- ✅ **No sleep mode** - instant response
- ✅ **Global edge network**

### Cold Start:
- **First request**: ~2-3 seconds (cold start)
- **Subsequent requests**: <100ms (warm)

## 🔄 Auto-Deploy Setup

Vercel otomatis deploy setiap push ke main branch:

```bash
# Update code
git add .
git commit -m "Update: improve detection algorithm"
git push origin main

# Vercel auto-deploy dalam 1-2 menit!
```

## 🎯 Custom Domain (Optional)

1. Di Vercel dashboard → project settings
2. Klik **"Domains"**
3. Add custom domain (gratis!)
4. Update DNS records sesuai instruksi

## 💡 Tips & Optimization

1. **Function Size**: Keep small untuk faster cold starts
2. **Dependencies**: Minimal dependencies untuk faster builds
3. **Caching**: Vercel auto-cache static assets
4. **Monitoring**: Use Vercel Analytics (free)

## 🆓 Cost Breakdown

```
Signup: FREE (no credit card)
Deployment: FREE
Bandwidth: FREE (100GB/month)
Functions: FREE (100 invocations/day)
Custom Domain: FREE
HTTPS: FREE
Support: Community (free)

Total: $0.00/month 🎉
```

## 🐛 Troubleshooting

### Build Fails?
- Check `requirements.txt` syntax
- Ensure Python 3.9 compatibility

### Function Timeout?
- Optimize algorithm performance
- Reduce dependencies

### Import Errors?
- Check file paths in `api/index.py`
- Ensure all modules are accessible

---

## 🎯 READY TO DEPLOY!

Repository sudah siap dengan:
- ✅ `vercel.json` configuration
- ✅ `api/index.py` serverless handler
- ✅ Optimized for Vercel platform

**Steps:**
1. Buka [vercel.com](https://vercel.com)
2. Continue with GitHub (no card needed!)
3. Import `XenchinRyu7/SecurePrompt`
4. Deploy!

**Expected deploy time: 1-2 menit** ⚡

**Result: Instant global API!** 🌍