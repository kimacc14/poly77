# 🚀 Render.com Deployment Guide

## Overview

Deploy your AI-Powered Market Analyzer to Render.com with **FREE hosting**.

**Cost**: $0/month (Free tier)
**Build Time**: 5-8 minutes (includes AI models)
**Resources**: 512MB RAM, 750 hours/month

---

## ✅ Why Render?

### Free Tier Benefits:
- ✅ **100% FREE** (750 hours/month ≈ 25 days)
- ✅ Auto-deploy from GitHub
- ✅ Free SSL certificates
- ✅ Custom domains (free on Starter plan)
- ✅ Python 3.12 support
- ✅ AI/ML libraries support (PyTorch, Transformers)
- ✅ Singapore region available

### vs Railway:
| Feature | Render (Free) | Railway (Free) |
|---------|--------------|----------------|
| Cost | $0/month | ~$5.79/month |
| RAM | 512MB | 1GB |
| Hours | 750/month | 500/month |
| Custom Domain | ✅ Free | ❌ Requires $5/month |
| Auto-deploy | ✅ Yes | ✅ Yes |
| AI Support | ✅ Yes | ✅ Yes |

---

## 📋 Prerequisites

1. ✅ GitHub repository (already done): https://github.com/kimacc14/poly77
2. ✅ `render.yaml` configuration (already created)
3. ✅ Environment variables ready
4. 📝 Render.com account (free signup)

---

## 🚀 Step 1: Sign Up for Render

### Create Account:

1. Go to: https://render.com
2. Click **"Get Started for Free"**
3. Sign up with:
   - **GitHub** (recommended - easiest)
   - Or Email

### Connect GitHub:

If using email signup:
1. Go to **Account Settings** → **Connected Accounts**
2. Click **"Connect GitHub"**
3. Authorize Render to access your repositories

---

## 🔧 Step 2: Create Web Service

### Via Render Dashboard:

1. **Login** to https://dashboard.render.com

2. Click **"New +"** → **"Web Service"**

3. **Connect Repository**:
   - Select: `kimacc14/poly77`
   - Click **"Connect"**

4. **Configure Service**:

   **Basic Settings**:
   ```
   Name: poly77-ai-market-analyzer
   Region: Singapore (closest to Thailand)
   Branch: main
   Runtime: Python 3
   ```

   **Build Settings**:
   ```
   Build Command:
   pip install --upgrade pip && pip install -r backend/requirements.txt

   Start Command:
   cd backend && python production_server.py
   ```

   **Plan**:
   ```
   Instance Type: Free
   (512 MB RAM, 750 hours/month)
   ```

5. Click **"Create Web Service"**

---

## 🔐 Step 3: Add Environment Variables

After creating service, go to **Environment** tab:

### Required Variables:

Click **"Add Environment Variable"** for each:

```bash
# Reddit API (for sentiment analysis)
REDDIT_CLIENT_ID=your_reddit_client_id
REDDIT_CLIENT_SECRET=your_reddit_client_secret

# Twitter API (optional)
TWITTER_BEARER_TOKEN=your_twitter_token

# Kalshi API (optional - uses public API if not set)
KALSHI_API_KEY=your_kalshi_api_key

# Port (auto-set by Render)
PORT=10000
```

### Get API Keys:

**Reddit** (Required for AI sentiment):
1. Go to: https://www.reddit.com/prefs/apps
2. Create app: "AI Market Analyzer"
3. Type: "script"
4. Copy Client ID and Secret

**Twitter** (Optional):
1. Go to: https://developer.twitter.com
2. Create project and app
3. Get Bearer Token

**Kalshi** (Optional):
- Uses public API by default
- Get key from: https://kalshi.com/api

---

## ⚙️ Step 4: Configure Auto-Deploy

### Via render.yaml (Already Done):

The `render.yaml` file enables:
- ✅ Auto-deploy on git push
- ✅ Health check endpoint: `/health`
- ✅ Region: Singapore
- ✅ Free plan

### Manual Deploy:

If you need to manually deploy:
1. Go to service dashboard
2. Click **"Manual Deploy"** → **"Deploy latest commit"**

---

## 🏗️ Step 5: Wait for Build

### Build Process:

Render will automatically:
1. **Clone** your GitHub repository
2. **Install** Python dependencies (~5 minutes)
3. **Download** AI models (PyTorch, Transformers)
4. **Start** production server
5. **Health check** at `/health`

### Monitor Build:

Watch logs in real-time:
1. Go to **"Logs"** tab
2. See build progress
3. Wait for: `✅ Application startup complete`

### Expected Build Time:
- **First deploy**: 6-8 minutes (downloads AI models)
- **Subsequent deploys**: 2-4 minutes (cached dependencies)

---

## ✅ Step 6: Verify Deployment

### Your Render URL:

Render will assign a URL like:
```
https://poly77-ai-market-analyzer.onrender.com
```

### Test Endpoints:

#### 1. Health Check:
```bash
curl https://poly77-ai-market-analyzer.onrender.com/health
```

**Expected**:
```json
{
  "status": "healthy",
  "sentiment_analyzer": true,
  "polymarket": true,
  "kalshi": true
}
```

#### 2. Frontend UI:
Open in browser:
```
https://poly77-ai-market-analyzer.onrender.com
```

Should show:
- ✅ Full UI with market cards
- ✅ Platform filters (Polymarket/Kalshi)
- ✅ Category filters
- ✅ Real-time market data

#### 3. API Endpoints:
```bash
# List all markets
curl https://poly77-ai-market-analyzer.onrender.com/api/markets

# Get market with AI analysis
curl https://poly77-ai-market-analyzer.onrender.com/api/markets/MARKET_ID
```

---

## 🌐 Step 7: Custom Domain (Optional)

### Add Custom Domain (Free on Render):

1. Go to service **"Settings"**
2. Scroll to **"Custom Domain"**
3. Click **"Add Custom Domain"**
4. Enter: `yourdomain.com`

### Configure DNS:

Add CNAME record at your domain registrar:

```
Type: CNAME
Name: @  (or yourdomain.com)
Value: poly77-ai-market-analyzer.onrender.com
TTL: 3600
```

For www subdomain:
```
Type: CNAME
Name: www
Value: poly77-ai-market-analyzer.onrender.com
TTL: 3600
```

### SSL Certificate:

Render automatically provisions **free SSL** via Let's Encrypt.
- No configuration needed
- Takes 5-10 minutes after DNS propagation

---

## 🔄 Step 8: Auto-Deploy Setup

### Already Enabled via render.yaml:

Every time you push to GitHub:
1. Render detects new commit
2. Automatically triggers build
3. Deploys new version
4. Zero downtime deployment

### Manual Control:

Disable auto-deploy if needed:
1. Go to **"Settings"** → **"Build & Deploy"**
2. Toggle **"Auto-Deploy"**

---

## 📊 Monitoring & Logs

### View Logs:

**Real-time logs**:
```bash
# In Render dashboard → Logs tab
# Or use Render CLI
render logs -t poly77-ai-market-analyzer
```

### Metrics:

Go to **"Metrics"** tab to see:
- CPU usage
- Memory usage
- Request rate
- Response time

### Health Checks:

Render automatically pings `/health` endpoint:
- Every 5 minutes
- Restarts if unhealthy
- Email alerts on failure

---

## 🐛 Troubleshooting

### Issue 1: Build Failed - Dependency Error

**Error**: `Could not install torch` or `numpy error`

**Solution**:
Check `backend/requirements.txt` has:
```
torch==2.2.0
numpy==1.26.0
transformers==4.40.0
```

### Issue 2: Application Not Starting

**Error**: `Port already in use` or `timeout`

**Solution**:
Verify `production_server.py` uses PORT env:
```python
port = int(os.getenv("PORT", 8002))
uvicorn.run(app, host="0.0.0.0", port=port)
```

### Issue 3: Out of Memory (OOM)

**Error**: `Killed` or `Out of memory`

**Solution**:
Free tier has 512MB RAM. AI models are large.
- Upgrade to **Starter plan** ($7/month) for 2GB RAM
- Or optimize model loading (lazy load)

### Issue 4: Service Sleeping

**Behavior**: Free tier spins down after 15 minutes inactivity

**Solution**:
- First request takes 30-60 seconds to wake up
- Keep alive with ping service (e.g., UptimeRobot)
- Or upgrade to Starter plan ($7/month) for always-on

### Issue 5: Environment Variables Not Loading

**Error**: `REDDIT_CLIENT_ID not found`

**Solution**:
1. Go to **Environment** tab
2. Verify all variables are set
3. Click **"Save Changes"**
4. Redeploy: **Manual Deploy** → **"Clear build cache & deploy"**

---

## 💰 Cost Breakdown

### Free Tier:
- **Cost**: $0/month
- **RAM**: 512MB
- **Hours**: 750/month (~25 days)
- **Bandwidth**: 100GB/month
- **Build Minutes**: 500/month
- **Sleeps after**: 15 min inactivity

### Starter Plan ($7/month):
- **RAM**: 2GB (better for AI)
- **Hours**: Unlimited (always-on)
- **Bandwidth**: 100GB/month
- **No sleep**: Instant response
- **Custom domains**: Unlimited

### Comparison:

| Feature | Render Free | Render Starter | Railway Hobby |
|---------|-------------|----------------|---------------|
| Cost | $0 | $7/month | $5/month |
| RAM | 512MB | 2GB | 8GB |
| Uptime | 750h/month | Always-on | Always-on |
| Sleep | Yes (15min) | No | No |
| Custom Domain | ✅ Free | ✅ Free | ✅ Included |

**Recommendation**: Start with Free tier, upgrade if you need always-on service.

---

## 🎯 Performance Optimization

### 1. Enable Caching

Already enabled in code:
```python
# 5-minute cache for market data
cache_ttl = 300
```

### 2. Use CDN for Assets

If using custom domain:
1. Enable Cloudflare proxy
2. Cache static assets (logos, CSS)
3. Reduce server load

### 3. Lazy Load AI Models

Modify `ai_analyzer.py` to load on first request:
```python
model = None

def get_model():
    global model
    if model is None:
        model = pipeline("sentiment-analysis")
    return model
```

### 4. Reduce Log Verbosity

In production:
```python
logger.setLevel(logging.WARNING)  # Instead of INFO
```

---

## 📈 Scaling Options

### When to Upgrade:

**Free tier sufficient if**:
- Low traffic (<100 requests/day)
- Can tolerate 30s wake-up time
- Development/testing

**Upgrade to Starter ($7/month) if**:
- Need instant response (always-on)
- High traffic (>1000 requests/day)
- Production use
- AI models causing OOM

**Upgrade to Pro ($25/month) if**:
- Very high traffic
- Need horizontal scaling
- Multiple regions
- Enterprise SLA

---

## 🔐 Security Best Practices

### 1. Environment Variables

✅ **Never commit** `.env` files:
```bash
# Already in .gitignore
.env
*.env
.env.local
```

### 2. Secret Management

Use Render's environment variables:
- Encrypted at rest
- Never exposed in logs
- Separate per environment

### 3. API Rate Limiting

Add to `production_server.py`:
```python
from slowapi import Limiter
limiter = Limiter(key_func=get_remote_address)

@app.get("/api/markets")
@limiter.limit("100/hour")
async def get_markets():
    ...
```

### 4. CORS Configuration

Already configured:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Restrict in production
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)
```

---

## 🚀 Quick Deployment Checklist

- [ ] Sign up for Render.com (free)
- [ ] Connect GitHub repository
- [ ] Create Web Service
- [ ] Configure build & start commands
- [ ] Add environment variables (Reddit API keys)
- [ ] Wait for build (6-8 minutes)
- [ ] Test health endpoint: `/health`
- [ ] Verify UI loads
- [ ] Test API endpoints
- [ ] (Optional) Add custom domain
- [ ] Enable auto-deploy
- [ ] Monitor logs and metrics

---

## 🎉 Success Criteria

✅ **Deployment Successful When**:

1. **Health check passes**:
   ```bash
   curl https://your-app.onrender.com/health
   # Returns: {"status": "healthy", "sentiment_analyzer": true}
   ```

2. **Frontend UI loads**:
   - All markets visible
   - Filters working
   - Trade buttons functional

3. **AI Analysis works**:
   ```bash
   curl https://your-app.onrender.com/api/markets/MARKET_ID
   # Returns: sentiment analysis + predictions
   ```

4. **No errors in logs**:
   - Check Logs tab
   - Look for: `✅ Application startup complete`
   - No Python exceptions

---

## 📞 Support Resources

### Render Documentation:
- Main docs: https://render.com/docs
- Python guide: https://render.com/docs/deploy-fastapi
- Environment variables: https://render.com/docs/environment-variables
- Troubleshooting: https://render.com/docs/troubleshooting-deploys

### Community:
- Render Discord: https://discord.gg/render
- Community forum: https://community.render.com

### This Project:
- GitHub: https://github.com/kimacc14/poly77
- Railway (alternative): https://poly77-ai-market-analyzer-production.up.railway.app

---

## 🆚 Render vs Other Platforms

### vs Vercel:
- ❌ Vercel doesn't support Python FastAPI (serverless only)
- ✅ Render supports full Python web apps
- ✅ Render better for AI/ML models

### vs Heroku:
- ✅ Render free tier (Heroku removed free tier)
- ✅ Faster builds
- ✅ Better DX

### vs Railway:
- ✅ Render: Free ($0)
- ❌ Railway: $5.79/month
- ✅ Render: Custom domain free
- ❌ Railway: Requires $5/month for custom domain

### vs Hugging Face Spaces:
- ✅ Render: Full FastAPI + frontend
- ❌ Spaces: Only Gradio/Streamlit UI
- ✅ Render: Better for production apps

---

## 🎓 Next Steps

After successful deployment:

1. **Share your app**:
   - URL: `https://your-app.onrender.com`
   - Add to GitHub README

2. **Monitor performance**:
   - Check Metrics tab daily
   - Review logs for errors
   - Test from different regions

3. **Consider upgrades**:
   - If traffic grows → Starter plan ($7/month)
   - If AI is slow → More RAM
   - If need always-on → Remove sleep

4. **Add features**:
   - User authentication
   - Database (PostgreSQL)
   - Email alerts
   - API rate limiting

---

## 💡 Pro Tips

### 1. Keep Service Awake (Free Tier)

Use external ping service:
- **UptimeRobot** (free): https://uptimerobot.com
- Ping every 5 minutes to prevent sleep
- Set monitor: `https://your-app.onrender.com/health`

### 2. Optimize Build Time

Cache dependencies:
```yaml
# render.yaml
buildCommand: |
  pip install --upgrade pip
  pip install -r backend/requirements.txt --cache-dir /opt/render/.cache/pip
```

### 3. Use Preview Environments

Render supports preview deploys for PRs:
- Automatic staging URLs
- Test before merging
- Enable in Settings

### 4. Add Status Badge

Add to GitHub README:
```markdown
![Render Deploy](https://img.shields.io/badge/render-deployed-success)
```

---

## ✅ Final Verification

After deployment, run these tests:

```bash
# 1. Health check
curl https://your-app.onrender.com/health

# 2. API test
curl https://your-app.onrender.com/api/markets?platform=polymarket

# 3. Load test
ab -n 100 -c 10 https://your-app.onrender.com/health

# 4. SSL check
curl -I https://your-app.onrender.com | grep -i "strict-transport-security"
```

---

**Ready to deploy!** 🚀

Follow the steps above and your AI Market Analyzer will be live on Render in ~10 minutes!

---

**Deployed by** 🤖 [Claude Code](https://claude.com/claude-code)
