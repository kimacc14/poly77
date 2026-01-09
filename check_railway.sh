#!/bin/bash

# Script to check Railway deployment status

echo "🚀 Checking Railway Deployment Status..."
echo ""

# Check if railway CLI is installed
if ! command -v railway &> /dev/null; then
    echo "❌ Railway CLI not installed"
    exit 1
fi

echo "✅ Railway CLI installed: $(railway --version)"
echo ""

# Check who is logged in
echo "👤 Logged in as:"
railway whoami
echo ""

# Check project status
echo "📊 Project Status:"
railway status
echo ""

# Try to get logs (this might fail in non-interactive mode)
echo "📝 Attempting to get deployment logs..."
railway logs 2>&1 | head -30 || echo "⚠️  Cannot get logs in non-interactive mode"
echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "🌐 Next Steps:"
echo ""
echo "1. Open Railway Dashboard:"
echo "   https://railway.com/project/77950b06-1505-4ce4-9198-d48dd25291a9"
echo ""
echo "2. Check Deployments tab:"
echo "   - Look for ✅ Success or ❌ Failed status"
echo "   - If building, wait 5-10 minutes"
echo ""
echo "3. Set Environment Variables (Variables tab):"
echo "   REDDIT_CLIENT_ID=mock"
echo "   REDDIT_CLIENT_SECRET=mock"
echo "   REDDIT_USER_AGENT=AI-Mindshare-Analyzer/1.0"
echo ""
echo "4. Generate Domain (Settings → Networking):"
echo "   Click 'Generate Domain' button"
echo ""
echo "5. Test your app:"
echo "   Open the generated URL in browser"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
