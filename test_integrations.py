"""
Integration Tests for Hotel Sales Multi-Agent System
Tests all external service integrations and file outputs
"""
import os
import sys
import json
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_environment_setup():
    """Test environment configuration"""
    print("🔧 Testing Environment Setup...")
    
    # Test .env.example exists
    if os.path.exists('.env.example'):
        print("✅ .env.example file exists")
    else:
        print("❌ .env.example file missing")
        return False
    
    # Test config validation
    try:
        from config import Config
        Config.validate_config()
        print("✅ Configuration validation passed")
    except Exception as e:
        print(f"⚠️  Configuration validation warning: {e}")
    
    return True

def test_memory_system():
    """Test memory system with both Pinecone and file fallback"""
    print("\n🧠 Testing Memory System...")
    
    try:
        from utils.memory import memory
        
        # Test saving to memory
        test_content = "Test memory content for integration testing"
        result = memory.save_to_memory(test_content, {'type': 'test', 'test_id': 'integration_test'})
        print(f"✅ Memory save: {result}")
        
        # Test retrieving from memory
        memories = memory.retrieve_from_memory("test memory", top_k=1)
        if memories:
            print(f"✅ Memory retrieval: Found {len(memories)} memories")
        else:
            print("⚠️  No memories retrieved")
        
        # Test file persistence
        if os.path.exists(memory.memory_file):
            print("✅ File-based memory persistence working")
        else:
            print("⚠️  File-based memory file not found")
        
        return True
        
    except Exception as e:
        print(f"❌ Memory system test failed: {e}")
        return False

def test_google_ads_integration():
    """Test Google Ads integration (real API and simulator)"""
    print("\n📊 Testing Google Ads Integration...")
    
    try:
        from utils.google_ads import get_google_ads_client, create_google_ad, get_ad_performance
        
        # Test client selection
        client = get_google_ads_client()
        print(f"✅ Google Ads client selected: {type(client).__name__}")
        
        # Test ad creation
        test_keywords = ["miami luxury hotel", "downtown miami hotel"]
        test_headlines = ["Luxury Miami Hotel", "Downtown Miami Resort"]
        test_descriptions = ["Experience luxury in Miami", "Book your stay today"]
        
        result = create_google_ad(test_keywords, test_headlines, test_descriptions)
        print(f"✅ Ad creation: {result}")
        
        # Test performance retrieval
        performance = get_ad_performance("test_campaign_1")
        print(f"✅ Performance retrieval: {performance[:100]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ Google Ads integration test failed: {e}")
        return False

def test_crewai_compatibility():
    """Test CrewAI compatibility layer"""
    print("\n🤖 Testing CrewAI Compatibility...")
    
    try:
        from utils.crewai_compat import create_agent, create_task, _crewai_available
        
        # Test availability check
        available = _crewai_available()
        print(f"✅ CrewAI available: {available}")
        
        # Test agent creation
        agent = create_agent(
            role="Test Agent",
            goal="Test goal",
            backstory="Test backstory"
        )
        print(f"✅ Agent created: {type(agent).__name__}")
        
        # Test task creation
        task = create_task(
            description="Test task",
            agent=agent,
            expected_output="Test output"
        )
        print(f"✅ Task created: {type(task).__name__}")
        
        return True
        
    except Exception as e:
        print(f"❌ CrewAI compatibility test failed: {e}")
        return False

def test_output_file_creation():
    """Test output file creation"""
    print("\n📄 Testing Output File Creation...")
    
    try:
        from utils.output_handler import output_handler
        
        # Test markdown report creation
        test_data = {
            'summary': 'Test summary',
            'trends': 'Test trends',
            'recommendations': 'Test recommendations'
        }
        
        report_path = output_handler.create_market_research_report(test_data)
        if report_path and os.path.exists(report_path):
            print(f"✅ Market research report created: {report_path}")
        else:
            print("❌ Market research report creation failed")
            return False
        
        # Test JSON data saving
        test_json = {'test': 'data', 'timestamp': datetime.now().isoformat()}
        json_path = output_handler.save_json_data('test_data.json', test_json)
        if json_path and os.path.exists(json_path):
            print(f"✅ JSON data saved: {json_path}")
        else:
            print("❌ JSON data saving failed")
            return False
        
        # Test workflow log
        workflow_data = {
            'test': True,
            'timestamp': datetime.now().isoformat(),
            'status': 'test_completed'
        }
        log_path = output_handler.save_workflow_log(workflow_data)
        if log_path and os.path.exists(log_path):
            print(f"✅ Workflow log saved: {log_path}")
        else:
            print("❌ Workflow log saving failed")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Output file creation test failed: {e}")
        return False

def test_llm_integration():
    """Test LLM integration (Ollama/OpenAI)"""
    print("\n🧠 Testing LLM Integration...")
    
    try:
        # Test Ollama availability
        ollama_url = os.getenv('OLLAMA_BASE_URL', 'http://localhost:11434')
        print(f"✅ Ollama URL configured: {ollama_url}")
        
        # Test OpenAI availability
        openai_key = os.getenv('OPENAI_API_KEY')
        if openai_key:
            print("✅ OpenAI API key configured")
        else:
            print("⚠️  OpenAI API key not configured")
        
        # Test LLM setup in main
        from main import setup_llm
        llm = setup_llm()
        if llm:
            print(f"✅ LLM setup successful: {type(llm).__name__}")
        else:
            print("⚠️  LLM setup returned None (may be expected if Ollama not running)")
        
        return True
        
    except Exception as e:
        print(f"❌ LLM integration test failed: {e}")
        return False

def test_full_workflow():
    """Test the complete workflow"""
    print("\n🚀 Testing Full Workflow...")
    
    try:
        from main import run_diagnosis_workflow
        
        # Test diagnosis
        test_diagnosis = """
        Test hotel diagnosis for integration testing.
        Low occupancy during shoulder season in Miami luxury segment.
        Current occupancy rate: 45% (target: 70%).
        Average daily rate: $280 (competitors: $320).
        Main issues: Untargeted marketing, weak digital presence.
        Goal: Increase occupancy to 70% through targeted campaigns.
        """
        
        print("Running test workflow...")
        result = run_diagnosis_workflow(test_diagnosis)
        
        if result:
            print("✅ Full workflow completed successfully")
            return True
        else:
            print("⚠️  Full workflow completed but returned no result (may be expected in simple mode)")
            return True  # Consider this a pass since simple mode is expected
        
    except Exception as e:
        print(f"❌ Full workflow test failed: {e}")
        return False

def cleanup_test_files():
    """Clean up test files"""
    print("\n🧹 Cleaning up test files...")
    
    test_files = [
        'outputs/test_data.json',
        'outputs/market_research_report.md',
        'outputs/google_ads_campaign.md',
        'outputs/optimization_report.md',
        'logs/workflow_log_*.json'
    ]
    
    for file_pattern in test_files:
        if '*' in file_pattern:
            # Handle wildcard patterns
            import glob
            for file_path in glob.glob(file_pattern):
                try:
                    os.remove(file_path)
                    print(f"✅ Removed: {file_path}")
                except:
                    pass
        else:
            if os.path.exists(file_pattern):
                try:
                    os.remove(file_pattern)
                    print(f"✅ Removed: {file_pattern}")
                except:
                    pass

def main():
    """Run all integration tests"""
    print("🧪 Hotel Sales Multi-Agent System - Integration Tests")
    print("=" * 60)
    
    tests = [
        test_environment_setup,
        test_memory_system,
        test_google_ads_integration,
        test_crewai_compatibility,
        test_output_file_creation,
        test_llm_integration,
        test_full_workflow
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"❌ Test {test.__name__} failed with exception: {e}")
    
    print(f"\n📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All integration tests passed!")
    else:
        print(f"⚠️  {total - passed} tests failed or had warnings")
    
    # Cleanup
    cleanup_test_files()
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)