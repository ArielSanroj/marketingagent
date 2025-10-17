"""
Test script for the Hotel Sales Multi-Agent System
"""
import sys
import os
from datetime import datetime

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.memory import memory
from utils.google_ads import google_ads_simulator
from config import Config

def test_memory_system():
    """Test the memory system functionality"""
    print("🧠 Testing Memory System...")
    print("-" * 30)
    
    try:
        # Test saving to memory
        test_content = "Luxury hotels in Miami showing 15% increase in bookings during shoulder season"
        result = memory.save_to_memory(test_content, {'type': 'market_trends'})
        print(f"✅ Memory save: {result}")
        
        # Test retrieving from memory
        retrieved = memory.retrieve_from_memory("luxury hotels miami", top_k=3)
        print(f"✅ Memory retrieval: {len(retrieved)} memories found")
        
        # Test specific type search
        trends = memory.search_by_type('market_trends')
        print(f"✅ Type search: {len(trends)} market trend memories")
        
        return True
        
    except Exception as e:
        print(f"❌ Memory test failed: {str(e)}")
        return False

def test_google_ads_simulator():
    """Test the Google Ads simulator functionality"""
    print("\n🎯 Testing Google Ads Simulator...")
    print("-" * 30)
    
    try:
        # Test campaign creation
        campaign_data = {
            'name': 'Test Luxury Hotel Campaign',
            'budget': 1000,
            'bidding_strategy': 'TARGET_ROAS',
            'target_roas': 400
        }
        
        campaign = google_ads_simulator.create_campaign(campaign_data)
        print(f"✅ Campaign created: {campaign['id']}")
        
        # Test ad group creation
        ad_group_data = {
            'name': 'Luxury Hotel Ad Group',
            'keywords': ['luxury hotel miami', 'miami beach resort'],
            'cpc_bid': 2.50
        }
        
        ad_group = google_ads_simulator.create_ad_group(campaign['id'], ad_group_data)
        print(f"✅ Ad group created: {ad_group['id']}")
        
        # Test ad creation
        ad_data = {
            'headlines': [
                'Luxury Miami Beach Hotel',
                'Exclusive Resort Experience',
                'Book Direct & Save 20%'
            ],
            'descriptions': [
                'Experience unparalleled luxury with ocean views and world-class service.',
                'Limited time offer - book your luxury Miami getaway today.'
            ]
        }
        
        ad = google_ads_simulator.create_responsive_search_ad(ad_group['id'], ad_data)
        print(f"✅ Ad created: {ad['id']}")
        
        # Test performance data
        performance = google_ads_simulator.get_performance_data(campaign['id'])
        print(f"✅ Performance data: ROAS={performance['roas']:.2f}, CTR={performance['ctr']:.2f}%")
        
        # Test optimization
        optimization = google_ads_simulator.optimize_bidding(campaign['id'], 400)
        print(f"✅ Optimization suggestions: {len(optimization['optimization_suggestions'])} recommendations")
        
        return True
        
    except Exception as e:
        print(f"❌ Google Ads simulator test failed: {str(e)}")
        return False

def test_configuration():
    """Test configuration validation"""
    print("\n⚙️ Testing Configuration...")
    print("-" * 30)
    
    try:
        Config.validate_config()
        print("✅ Configuration validation passed")
        return True
        
    except Exception as e:
        print(f"❌ Configuration validation failed: {str(e)}")
        return False

def test_agent_imports():
    """Test that all agents can be imported"""
    print("\n🤖 Testing Agent Imports...")
    print("-" * 30)
    
    try:
        from agents.researcher import researcher
        from agents.ad_generator import ad_generator
        from agents.optimizer import optimizer
        from agents.supervisor import supervisor
        
        print("✅ All agents imported successfully")
        print(f"   - Researcher: {researcher.role}")
        print(f"   - Ad Generator: {ad_generator.role}")
        print(f"   - Optimizer: {optimizer.role}")
        print(f"   - Supervisor: {supervisor.role}")
        
        return True
        
    except Exception as e:
        print(f"❌ Agent import test failed: {str(e)}")
        return False

def test_task_imports():
    """Test that all tasks can be imported"""
    print("\n📋 Testing Task Imports...")
    print("-" * 30)
    
    try:
        from tasks.research_task import research_task
        from tasks.ad_generation_task import ad_generation_task
        from tasks.optimization_task import optimization_task
        
        print("✅ All tasks imported successfully")
        print(f"   - Research task: {research_task.description[:50]}...")
        print(f"   - Ad generation task: {ad_generation_task.description[:50]}...")
        print(f"   - Optimization task: {optimization_task.description[:50]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ Task import test failed: {str(e)}")
        return False

def main():
    """Run all tests"""
    print("🧪 Hotel Sales Multi-Agent System - Test Suite")
    print("=" * 60)
    print(f"Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    tests = [
        ("Configuration", test_configuration),
        ("Memory System", test_memory_system),
        ("Google Ads Simulator", test_google_ads_simulator),
        ("Agent Imports", test_agent_imports),
        ("Task Imports", test_task_imports)
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
    print("\n" + "=" * 60)
    print("📊 Test Results Summary")
    print("=" * 60)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{test_name:.<30} {status}")
        if result:
            passed += 1
    
    print("-" * 60)
    print(f"Total: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! System is ready to use.")
        return True
    else:
        print("⚠️  Some tests failed. Please check the configuration and dependencies.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)