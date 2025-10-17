"""
Simplified Hotel Sales Multi-Agent System
Main orchestration file for the hotel sales agent crew
Uses simplified memory system for compatibility
"""
import os
import json
from datetime import datetime
from dotenv import load_dotenv

# Import agents
from agents.researcher import researcher
from agents.ad_generator import ad_generator
from agents.optimizer import optimizer
from agents.supervisor import supervisor

# Import tasks
from tasks.research_task import research_task
from tasks.ad_generation_task import ad_generation_task
from tasks.optimization_task import optimization_task

# Import utilities
from utils.memory_simple import memory
from utils.google_ads import google_ads_simulator

# Load environment variables
load_dotenv()

def test_system():
    """Test the system with sample data"""
    print("🧪 Testing Hotel Sales Multi-Agent System")
    print("=" * 50)
    
    # Test memory system
    print("\n📚 Testing memory system...")
    test_content = "Test market trend: Luxury hotels in Miami showing 15% increase in bookings"
    memory_result = memory.save_to_memory(test_content, {'type': 'test_data'})
    print(f"Memory save result: {memory_result}")
    
    # Test memory retrieval
    retrieved = memory.retrieve_from_memory("luxury hotels miami", top_k=3)
    print(f"Retrieved memories: {len(retrieved)} found")
    
    # Test Google Ads simulator
    print("\n🎯 Testing Google Ads simulator...")
    test_campaign = google_ads_simulator.create_campaign({
        'name': 'Test Campaign',
        'budget': 500,
        'bidding_strategy': 'TARGET_ROAS',
        'target_roas': 400
    })
    print(f"Test campaign created: {test_campaign['id']}")
    
    # Test performance data
    performance = google_ads_simulator.get_performance_data(test_campaign['id'])
    print(f"Performance data: ROAS={performance['roas']:.2f}, CTR={performance['ctr']:.2f}%")
    
    print("\n✅ System tests completed!")

def run_sample_workflow():
    """Run a sample workflow without LLM dependencies"""
    print("🏨 Hotel Sales Multi-Agent System - Sample Workflow")
    print("=" * 60)
    
    # Sample diagnosis
    diagnosis = """
    Hotel: The Grand Miami Resort & Spa
    Location: Miami Beach, FL
    Issue: Low occupancy during shoulder season (April-May)
    
    Current Metrics:
    - Occupancy Rate: 45% (Target: 70%)
    - Average Daily Rate: $280 (Competitors: $320)
    - Revenue per Available Room: $126 (Target: $200)
    
    Main Problems:
    1. Untargeted marketing campaigns
    2. Weak digital presence and SEO
    3. Poor keyword targeting in Google Ads
    4. No seasonal promotion strategy
    5. Limited social media engagement
    
    Goals:
    - Increase occupancy to 70% by June
    - Raise ADR to $300+
    - Improve RevPAR to $200+
    - Launch targeted Google Ads campaigns
    - Enhance digital marketing presence
    """
    
    print("📊 Sample Diagnosis:")
    print(diagnosis)
    
    # Save diagnosis to memory
    memory.save_to_memory(
        f"Hotel diagnosis: {diagnosis}",
        {
            'type': 'diagnosis',
            'hotel': 'The Grand Miami Resort & Spa',
            'location': 'Miami Beach, FL',
            'timestamp': datetime.now().isoformat()
        }
    )
    
    # Simulate research phase
    print("\n🔍 Research Phase:")
    print("- Analyzing market trends for luxury hotels in Miami")
    print("- Identifying competitor strategies")
    print("- Researching seasonal demand patterns")
    
    research_data = {
        'market_trends': 'Luxury hotels in Miami showing 15% increase in bookings during shoulder season',
        'competitor_analysis': 'Competitors using targeted Google Ads with 3.5% CTR',
        'seasonal_patterns': 'Shoulder season (April-May) shows 25% lower occupancy'
    }
    
    for key, value in research_data.items():
        memory.save_to_memory(value, {'type': 'research', 'category': key})
    
    # Simulate ad generation phase
    print("\n📝 Ad Generation Phase:")
    print("- Creating targeted ad campaigns")
    print("- Developing compelling ad copy")
    print("- Setting up keyword targeting")
    
    # Create sample campaign
    campaign_data = {
        'name': 'Miami Luxury Resort - Shoulder Season',
        'budget': 2000,
        'bidding_strategy': 'TARGET_ROAS',
        'target_roas': 400
    }
    
    campaign = google_ads_simulator.create_campaign(campaign_data)
    print(f"✅ Campaign created: {campaign['id']}")
    
    # Create ad groups
    ad_groups = [
        {
            'name': 'Luxury Miami Beach Hotels',
            'keywords': ['luxury hotel miami beach', 'miami beach resort', 'luxury miami hotel'],
            'cpc_bid': 3.50
        },
        {
            'name': 'Shoulder Season Deals',
            'keywords': ['miami hotel deals april', 'miami beach spring break', 'miami hotel specials'],
            'cpc_bid': 2.75
        }
    ]
    
    for ad_group_data in ad_groups:
        ad_group = google_ads_simulator.create_ad_group(campaign['id'], ad_group_data)
        print(f"✅ Ad group created: {ad_group['id']}")
        
        # Create ads
        ad_data = {
            'headlines': [
                'Luxury Miami Beach Resort',
                'Exclusive Spring Deals',
                'Book Direct & Save 20%'
            ],
            'descriptions': [
                'Experience unparalleled luxury with ocean views and world-class service.',
                'Limited time offer - book your luxury Miami getaway today.'
            ]
        }
        
        ad = google_ads_simulator.create_responsive_search_ad(ad_group['id'], ad_data)
        print(f"✅ Ad created: {ad['id']}")
    
    # Simulate optimization phase
    print("\n⚡ Optimization Phase:")
    print("- Analyzing campaign performance")
    print("- Optimizing bidding strategies")
    print("- Refining targeting parameters")
    
    performance = google_ads_simulator.get_performance_data(campaign['id'])
    print(f"✅ Campaign performance: ROAS={performance['roas']:.2f}, CTR={performance['ctr']:.2f}%")
    
    optimization = google_ads_simulator.optimize_bidding(campaign['id'], 400)
    print(f"✅ Optimization suggestions: {len(optimization['optimization_suggestions'])} recommendations")
    
    # Generate final report
    print("\n📋 Final Report:")
    print("-" * 40)
    print("Campaign Strategy:")
    print(f"- Campaign ID: {campaign['id']}")
    print(f"- Budget: ${campaign_data['budget']:,}")
    print(f"- Target ROAS: {campaign_data['target_roas']}%")
    print(f"- Ad Groups: {len(ad_groups)}")
    
    print("\nExpected Results:")
    print("- Occupancy increase: 25% (45% → 70%)")
    print("- ADR increase: $20 ($280 → $300)")
    print("- Monthly revenue increase: $252,000")
    print("- ROAS target: 400%")
    
    print("\nNext Steps:")
    print("1. Monitor campaign performance daily")
    print("2. Adjust bids based on performance data")
    print("3. A/B test different ad variations")
    print("4. Expand to additional keywords and locations")
    
    # Save results to memory
    memory.save_to_memory(
        f"Workflow completed for campaign {campaign['id']}",
        {
            'type': 'workflow_result',
            'campaign_id': campaign['id'],
            'timestamp': datetime.now().isoformat(),
            'status': 'completed'
        }
    )
    
    print("\n✅ Sample workflow completed successfully!")
    return campaign

def main():
    """Main entry point"""
    print("🏨 Hotel Sales Multi-Agent System")
    print("Built with CrewAI and the Unified Agent Framework")
    print("=" * 60)
    
    # Check if running in test mode
    if len(os.sys.argv) > 1 and os.sys.argv[1] == "test":
        test_system()
        return
    
    # Run sample workflow
    result = run_sample_workflow()
    
    if result:
        print(f"\n💾 Results saved to memory")
    
    print("\n🎉 Hotel Sales Multi-Agent System completed!")

if __name__ == "__main__":
    main()