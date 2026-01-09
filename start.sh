#!/bin/bash

# AI-Powered Mindshare Market Analyzer - Quick Start Script

echo "🚀 AI-Powered Mindshare Market Analyzer - Quick Start"
echo "======================================================"
echo ""

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    echo "   Visit: https://docs.docker.com/get-docker/"
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

echo "✅ Docker and Docker Compose detected"
echo ""

# Check if .env file exists
if [ ! -f "backend/.env" ]; then
    echo "⚠️  No .env file found. Creating from template..."
    cp backend/.env.example backend/.env
    echo ""
    echo "📝 Please edit backend/.env and add your API credentials:"
    echo "   - TWITTER_BEARER_TOKEN"
    echo "   - REDDIT_CLIENT_ID"
    echo "   - REDDIT_CLIENT_SECRET"
    echo ""
    read -p "Press Enter once you've updated the .env file..."
fi

echo "🔧 Starting services with Docker Compose..."
echo ""

# Start Docker Compose
docker-compose up --build -d

echo ""
echo "⏳ Waiting for services to be ready..."
sleep 10

# Check service health
echo ""
echo "🔍 Checking service status..."
docker-compose ps

echo ""
echo "✅ Services started successfully!"
echo ""
echo "📍 Access points:"
echo "   - Frontend Dashboard: http://localhost:3000"
echo "   - Backend API: http://localhost:8000"
echo "   - API Documentation: http://localhost:8000/docs"
echo ""
echo "📊 Next steps:"
echo "   1. Open http://localhost:3000 in your browser"
echo "   2. Refresh market data: curl -X POST http://localhost:8000/api/refresh-markets"
echo "   3. Analyze a topic: curl -X POST 'http://localhost:8000/api/analyze-topic?topic=Bitcoin&hours_back=24'"
echo ""
echo "🛠️  To view logs:"
echo "   docker-compose logs -f"
echo ""
echo "🛑 To stop services:"
echo "   docker-compose down"
echo ""
echo "📚 For detailed setup instructions, see SETUP.md"
echo ""
