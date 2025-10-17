#!/usr/bin/env python3
"""
Simplified test script for the Hotel Sales Multi-Agent System
Tests core functionality without heavy dependencies
"""
import sys
import os
from datetime import datetime

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test that core modules can be imported"""
    print("🔍 Testing Core Imports...")
    print("-" * 30)
    
    try:
        # Test basic imports
        from config import Config
        print("✅ Config module imported successfully")
        
        # Test configuration
        print(f"   - LLM Model: {Config.LLM_MODEL}")
        print(f"   - LLM Base URL: {Config.LLM_BASE_URL}")
        print(f"   - Pinecone Index: {Config.PINECONE_INDEX_NAME}")
        
        return True
        
    except Exception as e:
        print(f"❌ Import test failed: {str(e)}")
        return False

def test_configuration():
    """Test configuration validation"""
    print("\n⚙️ Testing Configuration...")
    print("-" * 30)
    
    try:
        from config import Config
        
        # Test basic config access
        print(f"✅ LLM Model: {Config.LLM_MODEL}")
        print(f"✅ LLM Base URL: {Config.LLM_BASE_URL}")
        print(f"✅ Pinecone Index: {Config.PINECONE_INDEX_NAME}")
        print(f"✅ Embedding Model: {Config.EMBEDDING_MODEL}")
        print(f"✅ Default Budget: ${Config.DEFAULT_BUDGET}")
        print(f"✅ Default Target ROAS: {Config.DEFAULT_TARGET_ROAS}")
        
        # Test environment variable loading
        from dotenv import load_dotenv
        load_dotenv()
        
        pinecone_key = os.getenv('PINECONE_API_KEY')
        if pinecone_key and pinecone_key != 'your_pinecone_api_key':
            print("✅ Pinecone API key loaded from environment")
        else:
            print("⚠️  Pinecone API key not configured")
        
        return True
        
    except Exception as e:
        print(f"❌ Configuration test failed: {str(e)}")
        return False

def test_agent_structure():
    """Test that agent files exist and have correct structure"""
    print("\n🤖 Testing Agent Structure...")
    print("-" * 30)
    
    agent_files = [
        'agents/researcher.py',
        'agents/ad_generator.py', 
        'agents/optimizer.py',
        'agents/supervisor.py'
    ]
    
    all_good = True
    
    for agent_file in agent_files:
        if os.path.exists(agent_file):
            print(f"✅ {agent_file} exists")
            
            # Check if file has content
            with open(agent_file, 'r') as f:
                content = f.read()
                if len(content) > 100:  # Basic content check
                    print(f"   - File has content ({len(content)} chars)")
                else:
                    print(f"   ⚠️  File seems empty or very short")
                    all_good = False
        else:
            print(f"❌ {agent_file} not found")
            all_good = False
    
    return all_good

def test_task_structure():
    """Test that task files exist and have correct structure"""
    print("\n📋 Testing Task Structure...")
    print("-" * 30)
    
    task_files = [
        'tasks/research_task.py',
        'tasks/ad_generation_task.py',
        'tasks/optimization_task.py'
    ]
    
    all_good = True
    
    for task_file in task_files:
        if os.path.exists(task_file):
            print(f"✅ {task_file} exists")
            
            # Check if file has content
            with open(task_file, 'r') as f:
                content = f.read()
                if len(content) > 100:  # Basic content check
                    print(f"   - File has content ({len(content)} chars)")
                else:
                    print(f"   ⚠️  File seems empty or very short")
                    all_good = False
        else:
            print(f"❌ {task_file} not found")
            all_good = False
    
    return all_good

def test_utils_structure():
    """Test that utility files exist and have correct structure"""
    print("\n🛠️ Testing Utils Structure...")
    print("-" * 30)
    
    util_files = [
        'utils/memory.py',
        'utils/google_ads.py'
    ]
    
    all_good = True
    
    for util_file in util_files:
        if os.path.exists(util_file):
            print(f"✅ {util_file} exists")
            
            # Check if file has content
            with open(util_file, 'r') as f:
                content = f.read()
                if len(content) > 100:  # Basic content check
                    print(f"   - File has content ({len(content)} chars)")
                else:
                    print(f"   ⚠️  File seems empty or very short")
                    all_good = False
        else:
            print(f"❌ {util_file} not found")
            all_good = False
    
    return all_good

def test_file_structure():
    """Test overall project structure"""
    print("\n📁 Testing Project Structure...")
    print("-" * 30)
    
    required_files = [
        'main.py',
        'config.py',
        'requirements.txt',
        'setup.py',
        'README.md',
        '.env'
    ]
    
    all_good = True
    
    for file_name in required_files:
        if os.path.exists(file_name):
            print(f"✅ {file_name} exists")
        else:
            print(f"❌ {file_name} not found")
            all_good = False
    
    return all_good

def test_basic_functionality():
    """Test basic functionality without heavy dependencies"""
    print("\n🧪 Testing Basic Functionality...")
    print("-" * 30)
    
    try:
        # Test environment loading
        from dotenv import load_dotenv
        load_dotenv()
        print("✅ Environment variables loaded")
        
        # Test basic Python functionality
        test_data = {
            'hotel_name': 'Test Hotel',
            'occupancy_rate': 45,
            'target_rate': 70,
            'current_adr': 280,
            'target_adr': 300
        }
        
        print(f"✅ Test data created: {test_data}")
        
        # Test basic calculations
        occupancy_gap = test_data['target_rate'] - test_data['occupancy_rate']
        adr_gap = test_data['target_adr'] - test_data['current_adr']
        
        print(f"✅ Occupancy gap: {occupancy_gap}%")
        print(f"✅ ADR gap: ${adr_gap}")
        
        return True
        
    except Exception as e:
        print(f"❌ Basic functionality test failed: {str(e)}")
        return False

def main():
    """Run all simplified tests"""
    print("🧪 Hotel Sales Multi-Agent System - Simplified Test Suite")
    print("=" * 70)
    print(f"Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)
    
    tests = [
        ("File Structure", test_file_structure),
        ("Core Imports", test_imports),
        ("Configuration", test_configuration),
        ("Agent Structure", test_agent_structure),
        ("Task Structure", test_task_structure),
        ("Utils Structure", test_utils_structure),
        ("Basic Functionality", test_basic_functionality)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} test crashed: {str(e)}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 70)
    print("📊 Test Results Summary")
    print("=" * 70)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{test_name:.<30} {status}")
        if result:
            passed += 1
    
    print("-" * 70)
    print(f"Total: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All basic tests passed! System structure looks good.")
        print("\nNext steps:")
        print("1. Install full dependencies: pip install -r requirements.txt")
        print("2. Set up Ollama: ollama serve")
        print("3. Run full test suite: python test_system.py")
        print("4. Run main application: python main.py")
        return True
    else:
        print("⚠️  Some tests failed. Please check the issues above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)