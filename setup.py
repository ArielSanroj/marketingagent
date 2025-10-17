"""
Setup script for the Hotel Sales Multi-Agent System
"""
import os
import sys
import subprocess
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        return False
    print(f"✅ Python {sys.version.split()[0]} detected")
    return True

def install_dependencies():
    """Install required dependencies"""
    print("\n📦 Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def create_directories():
    """Create necessary directories"""
    print("\n📁 Creating directories...")
    directories = ["outputs", "logs"]
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"✅ Created directory: {directory}")
    
    return True

def check_ollama():
    """Check if Ollama is installed and running"""
    print("\n🦙 Checking Ollama...")
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
            
            return True
        else:
            print("❌ Ollama not found. Please install from https://ollama.ai/")
            return False
    except FileNotFoundError:
        print("❌ Ollama not found. Please install from https://ollama.ai/")
        return False

def check_env_file():
    """Check if .env file exists and has required variables"""
    print("\n🔧 Checking environment configuration...")
    
    if not os.path.exists(".env"):
        print("❌ .env file not found. Please copy .env.example to .env and configure it.")
        return False
    
    # Check for required variables
    required_vars = ["PINECONE_API_KEY"]
    missing_vars = []
    
    with open(".env", "r") as f:
        env_content = f.read()
    
    for var in required_vars:
        if f"{var}=" not in env_content or f"{var}=your_" in env_content:
            missing_vars.append(var)
    
    if missing_vars:
        print(f"❌ Missing or incomplete environment variables: {', '.join(missing_vars)}")
        print("Please update your .env file with the correct values.")
        return False
    
    print("✅ Environment configuration looks good")
    return True

def run_tests():
    """Run the test suite"""
    print("\n🧪 Running tests...")
    try:
        result = subprocess.run([sys.executable, "test_system.py"], capture_output=True, text=True)
        print(result.stdout)
        if result.stderr:
            print("Errors:", result.stderr)
        return result.returncode == 0
    except Exception as e:
        print(f"❌ Failed to run tests: {e}")
        return False

def main():
    """Main setup function"""
    print("🏨 Hotel Sales Multi-Agent System Setup")
    print("=" * 50)
    
    steps = [
        ("Python Version", check_python_version),
        ("Dependencies", install_dependencies),
        ("Directories", create_directories),
        ("Ollama", check_ollama),
        ("Environment", check_env_file),
        ("Tests", run_tests)
    ]
    
    all_passed = True
    
    for step_name, step_func in steps:
        print(f"\n🔍 {step_name}...")
        if not step_func():
            all_passed = False
            print(f"❌ {step_name} setup failed")
        else:
            print(f"✅ {step_name} setup completed")
    
    print("\n" + "=" * 50)
    if all_passed:
        print("🎉 Setup completed successfully!")
        print("\nNext steps:")
        print("1. Make sure Ollama is running: ollama serve")
        print("2. Run the system: python main.py")
        print("3. Or run tests: python test_system.py")
    else:
        print("⚠️  Setup completed with issues. Please resolve the errors above.")
        print("\nTroubleshooting:")
        print("1. Check your Python version (3.8+ required)")
        print("2. Install Ollama from https://ollama.ai/")
        print("3. Configure your .env file with API keys")
        print("4. Run: ollama pull llama2")
    
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)