"""
Run the tphagent Frontend Server
Simple web interface for hotel marketing strategy generation
"""
import os
import sys

# Add parent directory to path
sys.path.append('..')

# Install required packages
os.system('pip install Flask==2.3.3 Werkzeug==2.3.7')

# Import and run the app
from app import app

if __name__ == '__main__':
    print("🚀 Starting tphagent Frontend Server...")
    print("📧 Email: arielsanroj@carmanfe.com.co")
    print("🌐 Server: http://127.0.0.1:8080")
    print("📱 Open your browser and go to: http://127.0.0.1:8080")
    print("💡 Note: Using port 8080 to avoid macOS AirPlay Receiver conflict")
    print()
    print("✨ Features:")
    print("  • Simple form to input email and hotel URL/Instagram")
    print("  • Real-time progress tracking")
    print("  • AI-powered marketing strategy generation")
    print("  • Email delivery of results")
    print("  • Download results as JSON")
    print()
    
    app.run(debug=True, host='127.0.0.1', port=8080)