#!/usr/bin/env python3
"""
Simplified example usage of the Hotel Sales Multi-Agent System
Demonstrates core functionality without heavy dependencies
"""
import sys
import os
from datetime import datetime

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.google_ads import google_ads_simulator
from utils.memory_simple import memory

def example_miami_luxury_hotel():
    """Example: Miami luxury hotel with low occupancy"""
    print("🏨 Example: Miami Luxury Hotel - Low Occupancy Issue")
    print("=" * 60)
    
    diagnosis = {
        'hotel_name': 'The Grand Miami Resort & Spa',
        'location': 'Miami Beach, FL',
        'current_occupancy': 45,
        'target_occupancy': 70,
        'current_adr': 280,
        'target_adr': 300,
        'rooms': 100,
        'issues': [
            'Untargeted marketing campaigns',
            'Weak digital presence and SEO',
            'Poor keyword targeting in Google Ads',
            'No seasonal promotion strategy',
            'Limited social media engagement'
        ]
    }
    
    print(f"Hotel: {diagnosis['hotel_name']}")
    print(f"Location: {diagnosis['location']}")
    print(f"Current Occupancy: {diagnosis['current_occupancy']}%")
    print(f"Target Occupancy: {diagnosis['target_occupancy']}%")
    print(f"Current ADR: ${diagnosis['current_adr']}")
    print(f"Target ADR: ${diagnosis['target_adr']}")
    print(f"Rooms: {diagnosis['rooms']}")
    
    print("\nIssues Identified:")
    for i, issue in enumerate(diagnosis['issues'], 1):
        print(f"{i}. {issue}")
    
    # Calculate improvement potential
    occupancy_gap = diagnosis['target_occupancy'] - diagnosis['current_occupancy']
    adr_gap = diagnosis['target_adr'] - diagnosis['current_adr']
    current_revenue = (diagnosis['current_occupancy'] / 100) * diagnosis['rooms'] * diagnosis['current_adr'] * 30
    target_revenue = (diagnosis['target_occupancy'] / 100) * diagnosis['rooms'] * diagnosis['target_adr'] * 30
    revenue_gap = target_revenue - current_revenue
    
    print(f"\nImprovement Potential:")
    print(f"- Occupancy gap: {occupancy_gap}%")
    print(f"- ADR gap: ${adr_gap}")
    print(f"- Monthly revenue gap: ${revenue_gap:,.2f}")
    
    # Save diagnosis to memory
    memory.save_to_memory(
        f"Hotel diagnosis: {diagnosis['hotel_name']} - Low occupancy issue",
        {
            'type': 'diagnosis',
            'hotel': diagnosis['hotel_name'],
            'location': diagnosis['location'],
            'issue': 'low_occupancy'
        }
    )
    
    print("\n🚀 Running Multi-Agent Workflow...")
    print("-" * 40)
    
    # Simulate research phase
    print("🔍 Research Phase:")
    print("- Analyzing market trends for luxury hotels in Miami")
    print("- Identifying competitor strategies")
    print("- Researching seasonal demand patterns")
    
    research_findings = [
        "Luxury hotels in Miami showing 15% increase in bookings during shoulder season",
        "Competitors using targeted Google Ads with 3.5% CTR",
        "Shoulder season (April-May) shows 25% lower occupancy but higher ADR potential"
    ]
    
    for finding in research_findings:
        memory.save_to_memory(finding, {'type': 'research', 'category': 'market_analysis'})
    
    # Simulate ad generation phase
    print("\n📝 Ad Generation Phase:")
    print("- Creating targeted ad campaigns")
    print("- Developing compelling ad copy")
    print("- Setting up keyword targeting")
    
    # Create campaign
    campaign_data = {
        'name': f"{diagnosis['hotel_name']} - Shoulder Season Campaign",
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
        },
        {
            'name': 'Luxury Resort Experience',
            'keywords': ['luxury resort miami', 'miami spa resort', 'exclusive miami hotel'],
            'cpc_bid': 4.00
        }
    ]
    
    for ad_group_data in ad_groups:
        ad_group = google_ads_simulator.create_ad_group(campaign['id'], ad_group_data)
        print(f"✅ Ad group created: {ad_group['id']} - {ad_group_data['name']}")
        
        # Create ads for each ad group
        ad_data = {
            'headlines': [
                f"{diagnosis['hotel_name']} - Luxury Experience",
                'Exclusive Spring Deals Available',
                'Book Direct & Save 20%'
            ],
            'descriptions': [
                'Experience unparalleled luxury with ocean views and world-class service.',
                'Limited time offer - book your luxury Miami getaway today.'
            ]
        }
        
        ad = google_ads_simulator.create_responsive_search_ad(ad_group['id'], ad_data)
        print(f"  ✅ Ad created: {ad['id']}")
    
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
    print(f"- Total Keywords: {sum(len(ag['keywords']) for ag in ad_groups)}")
    
    print("\nExpected Results:")
    print(f"- Occupancy increase: {occupancy_gap}% ({diagnosis['current_occupancy']}% → {diagnosis['target_occupancy']}%)")
    print(f"- ADR increase: ${adr_gap} (${diagnosis['current_adr']} → ${diagnosis['target_adr']})")
    print(f"- Monthly revenue increase: ${revenue_gap:,.2f}")
    print(f"- ROAS target: {campaign_data['target_roas']}%")
    
    print("\nNext Steps:")
    print("1. Monitor campaign performance daily")
    print("2. Adjust bids based on performance data")
    print("3. A/B test different ad variations")
    print("4. Expand to additional keywords and locations")
    print("5. Implement dynamic pricing strategy")
    
    # Save results to memory
    memory.save_to_memory(
        f"Workflow completed for {diagnosis['hotel_name']} - Campaign {campaign['id']}",
        {
            'type': 'workflow_result',
            'hotel': diagnosis['hotel_name'],
            'campaign_id': campaign['id'],
            'status': 'completed'
        }
    )
    
    print("\n✅ Example workflow completed successfully!")
    return campaign

def example_boutique_hotel():
    """Example: Boutique hotel with pricing issues"""
    print("\n🏨 Example: Boutique Hotel - Pricing Strategy Issue")
    print("=" * 60)
    
    diagnosis = {
        'hotel_name': 'The Artisan Boutique Hotel',
        'location': 'Fort Lauderdale, FL',
        'current_occupancy': 65,
        'target_occupancy': 75,
        'current_adr': 180,
        'target_adr': 220,
        'rooms': 50,
        'issues': [
            'Undervalued pricing strategy',
            'No dynamic pricing implementation',
            'Limited understanding of demand patterns',
            'Weak competitive positioning',
            'Ineffective upselling strategies'
        ]
    }
    
    print(f"Hotel: {diagnosis['hotel_name']}")
    print(f"Location: {diagnosis['location']}")
    print(f"Current Occupancy: {diagnosis['current_occupancy']}%")
    print(f"Target Occupancy: {diagnosis['target_occupancy']}%")
    print(f"Current ADR: ${diagnosis['current_adr']}")
    print(f"Target ADR: ${diagnosis['target_adr']}")
    print(f"Rooms: {diagnosis['rooms']}")
    
    print("\nIssues Identified:")
    for i, issue in enumerate(diagnosis['issues'], 1):
        print(f"{i}. {issue}")
    
    # Calculate improvement potential
    occupancy_gap = diagnosis['target_occupancy'] - diagnosis['current_occupancy']
    adr_gap = diagnosis['target_adr'] - diagnosis['current_adr']
    current_revenue = (diagnosis['current_occupancy'] / 100) * diagnosis['rooms'] * diagnosis['current_adr'] * 30
    target_revenue = (diagnosis['target_occupancy'] / 100) * diagnosis['rooms'] * diagnosis['target_adr'] * 30
    revenue_gap = target_revenue - current_revenue
    
    print(f"\nImprovement Potential:")
    print(f"- Occupancy gap: {occupancy_gap}%")
    print(f"- ADR gap: ${adr_gap}")
    print(f"- Monthly revenue gap: ${revenue_gap:,.2f}")
    
    # Save diagnosis to memory
    memory.save_to_memory(
        f"Hotel diagnosis: {diagnosis['hotel_name']} - Pricing strategy issue",
        {
            'type': 'diagnosis',
            'hotel': diagnosis['hotel_name'],
            'location': diagnosis['location'],
            'issue': 'pricing_strategy'
        }
    )
    
    print("\n🚀 Running Multi-Agent Workflow...")
    print("-" * 40)
    
    # Create campaign focused on pricing optimization
    campaign_data = {
        'name': f"{diagnosis['hotel_name']} - Pricing Optimization Campaign",
        'budget': 1500,
        'bidding_strategy': 'TARGET_ROAS',
        'target_roas': 350
    }
    
    campaign = google_ads_simulator.create_campaign(campaign_data)
    print(f"✅ Campaign created: {campaign['id']}")
    
    # Create ad groups focused on value proposition
    ad_groups = [
        {
            'name': 'Boutique Hotel Experience',
            'keywords': ['boutique hotel fort lauderdale', 'unique hotel experience', 'artisan hotel'],
            'cpc_bid': 2.25
        },
        {
            'name': 'Value Luxury Stays',
            'keywords': ['affordable luxury hotel', 'boutique hotel deals', 'unique stay fort lauderdale'],
            'cpc_bid': 1.95
        }
    ]
    
    for ad_group_data in ad_groups:
        ad_group = google_ads_simulator.create_ad_group(campaign['id'], ad_group_data)
        print(f"✅ Ad group created: {ad_group['id']} - {ad_group_data['name']}")
        
        # Create ads
        ad_data = {
            'headlines': [
                f"{diagnosis['hotel_name']} - Unique Boutique Experience",
                'Affordable Luxury in Fort Lauderdale',
                'Book Direct & Save 15%'
            ],
            'descriptions': [
                'Discover our unique boutique hotel with personalized service and local charm.',
                'Experience luxury without the luxury price tag - book your stay today.'
            ]
        }
        
        ad = google_ads_simulator.create_responsive_search_ad(ad_group['id'], ad_data)
        print(f"  ✅ Ad created: {ad['id']}")
    
    # Get performance data
    performance = google_ads_simulator.get_performance_data(campaign['id'])
    print(f"✅ Campaign performance: ROAS={performance['roas']:.2f}, CTR={performance['ctr']:.2f}%")
    
    print("\n📋 Pricing Strategy Recommendations:")
    print("- Implement dynamic pricing based on demand")
    print("- Focus on value proposition in marketing")
    print("- Target higher-end market segments")
    print("- Implement upselling strategies")
    print("- Monitor competitor pricing regularly")
    
    print("\n✅ Boutique hotel example completed!")
    return campaign

def main():
    """Run example scenarios"""
    print("🏨 Hotel Sales Multi-Agent System - Example Scenarios")
    print("=" * 70)
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)
    
    # Run example scenarios
    scenarios = [
        ("Miami Luxury Hotel", example_miami_luxury_hotel),
        ("Boutique Hotel Pricing", example_boutique_hotel)
    ]
    
    results = []
    
    for scenario_name, scenario_func in scenarios:
        print(f"\n{'='*70}")
        print(f"Running Scenario: {scenario_name}")
        print('='*70)
        
        try:
            result = scenario_func()
            results.append((scenario_name, True, result))
        except Exception as e:
            print(f"❌ Scenario failed: {e}")
            results.append((scenario_name, False, None))
    
    # Summary
    print("\n" + "="*70)
    print("📊 Example Scenarios Summary")
    print("="*70)
    
    successful = 0
    total = len(results)
    
    for scenario_name, success, result in results:
        status = "✅ COMPLETED" if success else "❌ FAILED"
        print(f"{scenario_name:.<30} {status}")
        if success:
            successful += 1
    
    print("-" * 70)
    print(f"Total: {successful}/{total} scenarios completed successfully")
    
    if successful == total:
        print("🎉 All example scenarios completed successfully!")
        print("\n📋 Next Steps:")
        print("1. Review the generated campaigns and recommendations")
        print("2. Customize the strategies for your specific hotels")
        print("3. Integrate with real Google Ads API for production use")
        print("4. Add more sophisticated analysis and optimization")
        print("5. Scale to multiple hotels and properties")
    else:
        print("⚠️  Some scenarios failed. Please check the issues above.")

if __name__ == "__main__":
    main()