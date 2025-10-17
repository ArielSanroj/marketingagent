#!/bin/bash

# tphagent Frontend Startup Script
echo "🚀 Starting tphagent Frontend Server..."
echo "======================================"
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
pip install Flask==2.3.3 Werkzeug==2.3.7

# Start the server
echo "🌐 Starting web server..."
echo
echo "📧 Email: arielsanroj@carmanfe.com.co"
echo "🌐 Server: http://127.0.0.1:8080"
echo "📱 Open your browser and go to: http://127.0.0.1:8080"
echo "💡 Note: Using port 8080 to avoid macOS AirPlay Receiver conflict"
echo
echo "✨ Features:"
echo "  • Simple form to input email and hotel URL/Instagram"
echo "  • Real-time progress tracking"
echo "  • AI-powered marketing strategy generation"
echo "  • Email delivery of results"
echo "  • Download results as JSON"
echo
echo "Press Ctrl+C to stop the server"
echo

# Run the Flask app
python app.py