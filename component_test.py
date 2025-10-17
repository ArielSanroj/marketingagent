#!/usr/bin/env python3
"""
Component test script for the Hotel Sales Multi-Agent System
Tests individual components without heavy dependencies
"""
import sys
import os
from datetime import datetime

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_google_ads_simulator():
    """Test the Google Ads simulator functionality"""
    print("🎯 Testing Google Ads Simulator...")
    print("-" * 30)
    
    try:
        from utils.google_ads import google_ads_simulator
        
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
        from config import Config
        
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

def test_basic_calculations():
    """Test basic hotel revenue calculations"""
    print("\n🧮 Testing Basic Calculations...")
    print("-" * 30)
    
    try:
        # Test hotel metrics calculations
        current_occupancy = 45
        target_occupancy = 70
        current_adr = 280
        target_adr = 300
        rooms = 100
        
        # Calculate gaps
        occupancy_gap = target_occupancy - current_occupancy
        adr_gap = target_adr - current_adr
        
        # Calculate revenue
        current_revenue = (current_occupancy / 100) * rooms * current_adr * 30  # Monthly
        target_revenue = (target_occupancy / 100) * rooms * target_adr * 30
        
        revenue_gap = target_revenue - current_revenue
        
        print(f"✅ Occupancy gap: {occupancy_gap}%")
        print(f"✅ ADR gap: ${adr_gap}")
        print(f"✅ Current monthly revenue: ${current_revenue:,.2f}")
        print(f"✅ Target monthly revenue: ${target_revenue:,.2f}")
        print(f"✅ Revenue gap: ${revenue_gap:,.2f}")
        
        return True
        
    except Exception as e:
        print(f"❌ Basic calculations test failed: {str(e)}")
        return False

def test_sample_workflow():
    """Test a sample workflow without LLM dependencies"""
    print("\n🔄 Testing Sample Workflow...")
    print("-" * 30)
    
    try:
        # Simulate a hotel diagnosis
        diagnosis = {
            'hotel_name': 'The Grand Miami Resort',
            'location': 'Miami Beach, FL',
            'current_occupancy': 45,
            'target_occupancy': 70,
            'current_adr': 280,
            'target_adr': 300,
            'rooms': 100,
            'issues': [
                'Untargeted marketing campaigns',
                'Weak digital presence',
                'Poor keyword targeting'
            ]
        }
        
        print(f"✅ Hotel: {diagnosis['hotel_name']}")
        print(f"✅ Location: {diagnosis['location']}")
        print(f"✅ Current occupancy: {diagnosis['current_occupancy']}%")
        print(f"✅ Target occupancy: {diagnosis['target_occupancy']}%")
        print(f"✅ Current ADR: ${diagnosis['current_adr']}")
        print(f"✅ Target ADR: ${diagnosis['target_adr']}")
        print(f"✅ Issues identified: {len(diagnosis['issues'])}")
        
        # Calculate improvement potential
        occupancy_gap = diagnosis['target_occupancy'] - diagnosis['current_occupancy']
        adr_gap = diagnosis['target_adr'] - diagnosis['current_adr']
        
        print(f"✅ Occupancy improvement potential: {occupancy_gap}%")
        print(f"✅ ADR improvement potential: ${adr_gap}")
        
        return True
        
    except Exception as e:
        print(f"❌ Sample workflow test failed: {str(e)}")
        return False

def main():
    """Run all component tests"""
    print("🧪 Hotel Sales Multi-Agent System - Component Test Suite")
    print("=" * 70)
    print(f"Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)
    
    tests = [
        ("Configuration", test_configuration),
        ("Google Ads Simulator", test_google_ads_simulator),
        ("Agent Imports", test_agent_imports),
        ("Task Imports", test_task_imports),
        ("Basic Calculations", test_basic_calculations),
        ("Sample Workflow", test_sample_workflow)
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
        print("🎉 All component tests passed! Core functionality is working.")
        print("\nNext steps:")
        print("1. Install remaining dependencies for full functionality")
        print("2. Set up Ollama for LLM functionality")
        print("3. Run the main application: python main.py")
        return True
    else:
        print("⚠️  Some tests failed. Please check the issues above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)