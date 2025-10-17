#!/usr/bin/env python3
"""
Setup script for Hotel Sales Multi-Agent System
Helps users configure the system with proper integrations
"""
import os
import sys
import subprocess
import shutil
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible"""
    print("🐍 Checking Python version...")
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ required. Current version:", sys.version)
        return False
    print(f"✅ Python {sys.version.split()[0]} detected")
    return True

def install_dependencies():
    """Install required dependencies"""
    print("\n📦 Installing dependencies...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                      check=True, capture_output=True)
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def setup_environment():
    """Set up environment file"""
    print("\n🔧 Setting up environment...")
    
    if os.path.exists('.env'):
        print("✅ .env file already exists")
        return True
    
    if os.path.exists('.env.example'):
        shutil.copy('.env.example', '.env')
        print("✅ Created .env file from .env.example")
        print("⚠️  Please edit .env file with your actual API keys")
        return True
    else:
        print("❌ .env.example file not found")
        return False

def check_ollama():
    """Check if Ollama is installed and running"""
    print("\n🦙 Checking Ollama...")
    
    # Check if Ollama is installed
    try:
        result = subprocess.run(["ollama", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Ollama detected: {result.stdout.strip()}")
            
            # Check if llama2 model is available
            models_result = subprocess.run(["ollama", "list"], capture_output=True, text=True)
            if "llama2" in models_result.stdout:
                print("✅ Llama2 model found")
            else:
                print("⚠️  Llama2 model not found. Run: ollama pull llama2")
                print("   Or use: ollama pull mistral (alternative model)")
            
            return True
        else:
            print("❌ Ollama not found. Please install from https://ollama.ai/")
            return False
    except FileNotFoundError:
        print("❌ Ollama not found. Please install from https://ollama.ai/")
        return False

def create_directories():
    """Create necessary directories"""
    print("\n📁 Creating directories...")
    
    directories = ['outputs', 'logs']
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✅ Created directory: {directory}")

def run_integration_tests():
    """Run integration tests"""
    print("\n🧪 Running integration tests...")
    
    try:
        result = subprocess.run([sys.executable, "test_integrations.py"], 
                              capture_output=True, text=True)
        print(result.stdout)
        if result.stderr:
            print("Errors:", result.stderr)
        
        if result.returncode == 0:
            print("✅ Integration tests passed")
            return True
        else:
            print("⚠️  Some integration tests failed (this may be expected)")
            return False
    except Exception as e:
        print(f"❌ Failed to run integration tests: {e}")
        return False

def print_next_steps():
    """Print next steps for the user"""
    print("\n🎯 Next Steps:")
    print("=" * 50)
    print("1. Edit .env file with your API keys:")
    print("   - PINECONE_API_KEY (optional, for vector memory)")
    print("   - GOOGLE_ADS_* (optional, for real Google Ads)")
    print("   - OPENAI_API_KEY (optional, alternative to Ollama)")
    print()
    print("2. Start Ollama (if using local LLM):")
    print("   ollama serve")
    print("   ollama pull llama2")
    print()
    print("3. Run the system:")
    print("   python main.py")
    print()
    print("4. Run tests:")
    print("   python test_integrations.py")
    print()
    print("5. Check outputs in the 'outputs/' directory")

def main():
    """Main setup function"""
    print("🏨 Hotel Sales Multi-Agent System - Setup")
    print("=" * 50)
    
    steps = [
        ("Python Version", check_python_version),
        ("Dependencies", install_dependencies),
        ("Environment", setup_environment),
        ("Directories", create_directories),
        ("Ollama", check_ollama),
        ("Integration Tests", run_integration_tests)
    ]
    
    success_count = 0
    total_steps = len(steps)
    
    for step_name, step_func in steps:
        print(f"\n{'='*20} {step_name} {'='*20}")
        try:
            if step_func():
                success_count += 1
            else:
                print(f"⚠️  {step_name} step had issues")
        except Exception as e:
            print(f"❌ {step_name} step failed: {e}")
    
    print(f"\n📊 Setup Results: {success_count}/{total_steps} steps completed")
    
    if success_count >= total_steps - 1:  # Allow one failure
        print("🎉 Setup completed successfully!")
        print_next_steps()
        return True
    else:
        print("❌ Setup had significant issues. Please check the errors above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)