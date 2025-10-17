#!/bin/bash

# tphagent Optimized Frontend Startup Script
echo "🚀 Starting tphagent Optimized Frontend Server..."
echo "=============================================="
echo

# Check if we're in the right directory
if [ ! -d "frontend" ]; then
    echo "❌ Error: frontend directory not found"
    echo "Please run this script from the tphagent root directory"
    exit 1
fi

# Navigate to frontend directory
cd frontend

# Check if virtual environment exists
if [ ! -d "../.venv" ]; then
    echo "❌ Error: Virtual environment not found"
    echo "Please run 'python -m venv .venv' first"
    exit 1
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source ../.venv/bin/activate

# Install required packages
echo "📦 Installing required packages..."
pip install Flask==2.3.3 Werkzeug==2.3.7 requests beautifulsoup4 lxml aiohttp

# Start the optimized server
echo "🌐 Starting optimized web server..."
echo
echo "📧 Email: arielsanroj@carmanfe.com.co"
echo "🌐 Server: http://127.0.0.1:8080"
echo "📱 Open your browser and go to: http://127.0.0.1:8080"
echo "💡 Note: Using port 8080 to avoid macOS AirPlay Receiver conflict"
echo
echo "⚡ PERFORMANCE OPTIMIZATIONS ENABLED:"
echo "  • Parallel processing for hotel/Instagram analysis"
echo "  • Connection pooling and request caching"
echo "  • Optimized HTML parsing with lxml"
echo "  • Background task processing with thread pools"
echo "  • Adaptive polling for status updates"
echo "  • Performance monitoring and metrics"
echo
echo "🧪 To test performance, run: python test_performance.py"
echo
echo "Press Ctrl+C to stop the server"
echo

# Run the optimized Flask app
python app.py