"""
Example usage of the Hotel Sales Multi-Agent System
"""
import sys
import os
from datetime import datetime

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from main import run_diagnosis_workflow, test_system

def example_miami_luxury_hotel():
    """Example: Miami luxury hotel with low occupancy"""
    print("🏨 Example: Miami Luxury Hotel - Low Occupancy Issue")
    print("=" * 60)
    
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
    
    print(diagnosis)
    print("\n🚀 Running Multi-Agent Workflow...")
    print("-" * 40)
    
    result = run_diagnosis_workflow(diagnosis)
    
    if result:
        print("\n📊 Workflow Results:")
        print("-" * 20)
        print(result)
    else:
        print("❌ Workflow failed. Please check your configuration.")

def example_boutique_hotel():
    """Example: Boutique hotel with pricing issues"""
    print("\n🏨 Example: Boutique Hotel - Pricing Strategy Issue")
    print("=" * 60)
    
    diagnosis = """
    Hotel: The Artisan Boutique Hotel
    Location: Fort Lauderdale, FL
    Issue: Pricing strategy not optimized for market demand
    
    Current Metrics:
    - Occupancy Rate: 65% (Good)
    - Average Daily Rate: $180 (Below market: $220)
    - Revenue per Available Room: $117 (Target: $150)
    
    Main Problems:
    1. Undervalued pricing strategy
    2. No dynamic pricing implementation
    3. Limited understanding of demand patterns
    4. Weak competitive positioning
    5. Ineffective upselling strategies
    
    Goals:
    - Implement dynamic pricing strategy
    - Increase ADR to $220+
    - Improve RevPAR to $150+
    - Better competitive positioning
    - Enhanced revenue management
    """
    
    print(diagnosis)
    print("\n🚀 Running Multi-Agent Workflow...")
    print("-" * 40)
    
    result = run_diagnosis_workflow(diagnosis)
    
    if result:
        print("\n📊 Workflow Results:")
        print("-" * 20)
        print(result)
    else:
        print("❌ Workflow failed. Please check your configuration.")

def example_resort_expansion():
    """Example: Resort looking to expand market reach"""
    print("\n🏨 Example: Resort - Market Expansion Strategy")
    print("=" * 60)
    
    diagnosis = """
    Hotel: Paradise Key Resort & Marina
    Location: Key Largo, FL
    Issue: Need to expand market reach and attract new guest segments
    
    Current Metrics:
    - Occupancy Rate: 55% (Target: 75%)
    - Average Daily Rate: $320 (Good)
    - Revenue per Available Room: $176 (Target: $240)
    
    Main Problems:
    1. Limited market reach and awareness
    2. Narrow target audience (only fishing enthusiasts)
    3. Seasonal dependency on fishing season
    4. Limited digital marketing presence
    5. No wedding/event marketing strategy
    
    Goals:
    - Expand to wedding and event market
    - Attract family vacationers
    - Increase occupancy to 75%
    - Improve RevPAR to $240+
    - Diversify revenue streams
    """
    
    print(diagnosis)
    print("\n🚀 Running Multi-Agent Workflow...")
    print("-" * 40)
    
    result = run_diagnosis_workflow(diagnosis)
    
    if result:
        print("\n📊 Workflow Results:")
        print("-" * 20)
        print(result)
    else:
        print("❌ Workflow failed. Please check your configuration.")

def main():
    """Run example scenarios"""
    print("🏨 Hotel Sales Multi-Agent System - Example Scenarios")
    print("=" * 70)
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)
    
    # Check if system is properly configured
    print("\n🔍 Checking system configuration...")
    try:
        test_system()
        print("✅ System configuration looks good!")
    except Exception as e:
        print(f"❌ System configuration issue: {e}")
        print("Please run 'python setup.py' to configure the system.")
        return
    
    # Run example scenarios
    scenarios = [
        ("Miami Luxury Hotel", example_miami_luxury_hotel),
        ("Boutique Hotel Pricing", example_boutique_hotel),
        ("Resort Market Expansion", example_resort_expansion)
    ]
    
    for scenario_name, scenario_func in scenarios:
        print(f"\n{'='*70}")
        print(f"Running Scenario: {scenario_name}")
        print('='*70)
        
        try:
            scenario_func()
        except Exception as e:
            print(f"❌ Scenario failed: {e}")
        
        print(f"\n✅ Scenario '{scenario_name}' completed")
    
    print("\n" + "="*70)
    print("🎉 All example scenarios completed!")
    print("="*70)
    
    print("\n📋 Next Steps:")
    print("1. Review the generated reports and recommendations")
    print("2. Customize the agents and tasks for your specific needs")
    print("3. Integrate with real Google Ads API for production use")
    print("4. Add more sophisticated memory and learning capabilities")
    print("5. Scale to multiple hotels and properties")

if __name__ == "__main__":
    main()