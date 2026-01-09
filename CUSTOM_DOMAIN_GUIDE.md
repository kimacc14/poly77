# 🌐 Custom Domain Setup Guide for Railway

## Overview

This guide will help you set up a custom domain (e.g., `polymarket-ai.com`) for your Railway deployment.

**Current URL**: https://poly77-ai-market-analyzer-production.up.railway.app
**Target**: Your custom domain (e.g., `polymarket-ai.com`)

---

## 📋 Prerequisites

### 1. Railway Plan
- ✅ **Hobby Plan** ($5/month) - Recommended
- ✅ **Pro Plan** ($20/month) - For teams
- ❌ **Free Tier** - Does NOT support custom domains

### 2. Domain Name
- Buy from: Namecheap, Cloudflare, Google Domains, etc.
- Cost: ~$8-15/year for `.com` domain

---

## 🛒 Step 1: Buy a Domain

### Option A: Namecheap (Recommended)

**Website**: https://www.namecheap.com

**Steps**:
1. Go to https://www.namecheap.com
2. Search for your desired domain (e.g., `polymarket-ai.com`)
3. Add to cart and checkout ($8-15/year)
4. Create account or login
5. Complete payment

**Pros**:
- Cheap prices
- Easy DNS management
- Free WhoisGuard (privacy protection)
- Great support

### Option B: Cloudflare

**Website**: https://www.cloudflare.com/products/registrar/

**Steps**:
1. Sign up at https://dash.cloudflare.com
2. Go to "Domain Registration"
3. Search and register domain (~$10/year at cost)
4. Complete payment

**Pros**:
- At-cost pricing (no markup)
- Built-in CDN and DDoS protection
- Free SSL certificates
- Fast DNS propagation

### Option C: Google Domains (now Squarespace)

**Website**: https://domains.squarespace.com

**Steps**:
1. Go to https://domains.squarespace.com
2. Search for domain
3. Purchase ($12/year)

**Pros**:
- Reliable
- Simple interface
- Good integration with other services

---

## 🚀 Step 2: Upgrade Railway to Hobby Plan

**Current Plan**: Free Tier (no custom domain support)

### Upgrade Steps:

1. **Via Railway Dashboard**:
   ```
   https://railway.com/account/billing
   ```
   - Click "Upgrade to Hobby"
   - Add payment method
   - Confirm $5/month subscription

2. **Via CLI** (check current plan):
   ```bash
   railway whoami
   ```

**Cost**: $5/month for Hobby Plan

**What You Get**:
- ✅ Unlimited custom domains
- ✅ 8GB RAM (vs 1GB on free tier)
- ✅ 100GB bandwidth/month
- ✅ Faster builds
- ✅ Priority support

---

## 🔧 Step 3: Add Custom Domain to Railway

### Via Railway CLI:

```bash
# Add your domain
railway domain add yourdomain.com

# Add www subdomain
railway domain add www.yourdomain.com
```

### Via Railway Dashboard:

1. Go to your project: https://railway.com/project/77950b06-1505-4ce4-9198-d48dd25291a9

2. Click on your service: `poly77-ai-market-analyzer`

3. Go to **Settings** tab

4. Scroll to **Domains** section

5. Click **+ Custom Domain**

6. Enter your domain: `yourdomain.com`

7. Railway will show DNS records you need to add:
   ```
   Type: CNAME
   Name: @  (or yourdomain.com)
   Value: poly77-ai-market-analyzer-production.up.railway.app

   Type: CNAME
   Name: www
   Value: poly77-ai-market-analyzer-production.up.railway.app
   ```

---

## 🌍 Step 4: Configure DNS Records

### For Namecheap:

1. Login to https://www.namecheap.com
2. Go to **Domain List**
3. Click **Manage** next to your domain
4. Go to **Advanced DNS** tab
5. Add these records:

   **Record 1** (Root domain):
   ```
   Type: CNAME Record
   Host: @
   Value: poly77-ai-market-analyzer-production.up.railway.app
   TTL: Automatic
   ```

   **Record 2** (WWW subdomain):
   ```
   Type: CNAME Record
   Host: www
   Value: poly77-ai-market-analyzer-production.up.railway.app
   TTL: Automatic
   ```

6. **Remove** any existing A records for `@` and `www` if present

7. Click **Save All Changes**

### For Cloudflare:

1. Login to https://dash.cloudflare.com
2. Select your domain
3. Go to **DNS** → **Records**
4. Add these records:

   **Record 1**:
   ```
   Type: CNAME
   Name: @
   Target: poly77-ai-market-analyzer-production.up.railway.app
   Proxy status: DNS only (gray cloud)
   TTL: Auto
   ```

   **Record 2**:
   ```
   Type: CNAME
   Name: www
   Target: poly77-ai-market-analyzer-production.up.railway.app
   Proxy status: DNS only (gray cloud)
   TTL: Auto
   ```

5. Click **Save**

**Important**: Use "DNS only" mode (gray cloud) initially. After verification, you can enable Cloudflare proxy (orange cloud) for CDN.

### For Other Providers:

The process is similar - add CNAME records pointing to:
```
poly77-ai-market-analyzer-production.up.railway.app
```

---

## ⏱️ Step 5: Wait for DNS Propagation

DNS changes take time to propagate worldwide:

- **Typical time**: 5 minutes - 24 hours
- **Average time**: 30 minutes - 2 hours
- **Check status**: Use https://dnschecker.org

**Check DNS propagation**:
```bash
# Check if CNAME is set correctly
dig yourdomain.com CNAME +short

# Should return: poly77-ai-market-analyzer-production.up.railway.app
```

---

## ✅ Step 6: Verify Custom Domain

### Via Browser:
1. Open `https://yourdomain.com`
2. Should show your AI Market Analyzer
3. SSL certificate should be automatic (Railway provides free SSL)

### Via CLI:
```bash
# Check HTTP response
curl -I https://yourdomain.com

# Should return 200 OK and show your app
```

### Verify SSL:
Railway automatically provisions SSL certificates via Let's Encrypt. This may take 5-10 minutes after DNS propagation.

---

## 🐛 Troubleshooting

### Issue 1: Domain not resolving

**Problem**: `yourdomain.com` shows error or doesn't load

**Solutions**:
1. Check DNS propagation: https://dnschecker.org
2. Verify CNAME records are correct:
   ```bash
   dig yourdomain.com CNAME +short
   ```
3. Clear browser cache: Ctrl+Shift+Delete (Chrome/Firefox)
4. Wait longer (DNS can take up to 24 hours)

### Issue 2: SSL Certificate Error

**Problem**: "Your connection is not private" warning

**Solutions**:
1. Wait 5-10 minutes for Railway to provision SSL
2. Check Railway dashboard → Domains section for SSL status
3. Ensure domain is verified (green checkmark in Railway)
4. Try clearing browser cache and retry

### Issue 3: Shows old Railway subdomain

**Problem**: Domain redirects to `.up.railway.app` URL

**Solutions**:
1. Check DNS records are CNAME (not A records)
2. Disable any URL forwarding in domain registrar
3. Check Railway dashboard shows domain as active

### Issue 4: WWW not working

**Problem**: `www.yourdomain.com` doesn't work but `yourdomain.com` does

**Solutions**:
1. Add separate CNAME record for `www`:
   ```
   Type: CNAME
   Host: www
   Value: poly77-ai-market-analyzer-production.up.railway.app
   ```
2. Or add both domains separately in Railway dashboard

---

## 💡 Tips & Best Practices

### 1. Use Both Root and WWW
Add both `yourdomain.com` and `www.yourdomain.com` to Railway, so both work.

### 2. Enable Cloudflare Proxy (Optional)
After domain works, enable Cloudflare proxy (orange cloud) for:
- Free CDN (faster loading worldwide)
- DDoS protection
- Additional caching
- Analytics

### 3. Update Frontend (if needed)
Your app uses auto-detection, so no code changes needed:
```javascript
const API_BASE = window.location.hostname === 'localhost'
    ? 'http://localhost:8002'
    : '';  // Uses same domain
```

### 4. Monitor DNS
Use these tools to check DNS status:
- https://dnschecker.org
- https://www.whatsmydns.net
- `dig yourdomain.com CNAME +short`

---

## 💰 Total Cost Breakdown

### One-Time Costs:
- **Domain**: $8-15/year (e.g., `polymarket-ai.com`)

### Monthly Costs:
- **Railway Hobby**: $5/month
- **Total**: ~$5.75/month average (including domain)

### Annual Costs:
- **Domain**: $12/year
- **Railway**: $60/year ($5 × 12)
- **Total**: $72/year (~$6/month)

---

## 📝 Quick Setup Checklist

- [ ] Choose and buy domain from Namecheap/Cloudflare
- [ ] Upgrade Railway to Hobby Plan ($5/month)
- [ ] Add custom domain in Railway dashboard
- [ ] Note the CNAME value Railway provides
- [ ] Add CNAME records in domain DNS settings:
  - [ ] `@` → `poly77-ai-market-analyzer-production.up.railway.app`
  - [ ] `www` → `poly77-ai-market-analyzer-production.up.railway.app`
- [ ] Wait 30 minutes - 2 hours for DNS propagation
- [ ] Verify domain works: `https://yourdomain.com`
- [ ] Check SSL certificate is active (green padlock)
- [ ] Test all features work on custom domain
- [ ] Update any documentation/links

---

## 🎯 Example Domain Names (Available to check)

For prediction markets / AI analytics, consider:
- `polymarket-ai.com`
- `market-sentiment.ai`
- `prediction-analyzer.com`
- `ai-market-insights.com`
- `sentiment-markets.com`
- `crypto-prediction.ai`
- `market-mindshare.com`

Check availability at: https://www.namecheap.com/domains/domain-name-search/

---

## 📞 Support

If you need help:

**Railway Support**:
- Dashboard: https://railway.com/help
- Discord: https://discord.gg/railway
- Docs: https://docs.railway.app/guides/public-networking#custom-domains

**Domain Support**:
- Namecheap: https://www.namecheap.com/support/
- Cloudflare: https://support.cloudflare.com/

---

## ✅ After Setup

Once your custom domain is working:

1. Update any external links to use new domain
2. Add to README.md
3. Share with users!
4. Consider adding `sitemap.xml` and `robots.txt` for SEO

Your app will be accessible at:
- ✅ `https://yourdomain.com`
- ✅ `https://www.yourdomain.com`
- ✅ `https://poly77-ai-market-analyzer-production.up.railway.app` (still works)

---

**Good luck with your custom domain!** 🚀
