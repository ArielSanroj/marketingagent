"""
Interactive Demo of the Hotel Onboarding System
Shows the complete workflow with sample data
"""
import sys
import os
sys.path.append('.')

from utils.hotel_analyzer import HotelAnalyzer
from utils.user_approval import UserApprovalInterface
from onboarding import HotelOnboardingSystem

def demo_complete_workflow():
    """Demonstrate the complete onboarding workflow"""
    print("🏨 tphagent HOTEL ONBOARDING DEMO")
    print("=" * 50)
    print("This demo shows how the onboarding system works")
    print("with sample hotel data (no real URLs needed)")
    print()
    
    # Step 1: Simulate hotel analysis
    print("🔍 STEP 1: HOTEL WEBSITE ANALYSIS")
    print("-" * 40)
    print("Analyzing hotel website...")
    
    # Create mock hotel analysis (simulating what would come from real URL)
    mock_hotel_analysis = {
        'url': 'https://luxuryhotel.com',
        'domain': 'luxuryhotel.com',
        'hotel_name': 'The Grand Luxury Resort & Spa',
        'description': 'Luxury 5-star resort with world-class amenities and stunning ocean views',
        'analysis_status': 'success',
        'amenities': ['wifi', 'pool', 'spa', 'restaurant', 'bar', 'parking', 'room service', 'concierge'],
        'price_range': {
            'min': 350,
            'max': 800,
            'average': 575
        },
        'location_keywords': ['oceanfront', 'beach', 'downtown', 'near airport'],
        'social_media_links': {
            'instagram': ['https://instagram.com/grandluxuryresort'],
            'facebook': ['https://facebook.com/grandluxuryresort']
        },
        'marketing_insights': {
            'target_audience': ['Luxury travelers', 'Honeymooners', 'Business executives'],
            'key_selling_points': ['Oceanfront location', 'World-class spa', 'Fine dining', 'Luxury suites'],
            'competitive_advantages': ['Prime beachfront location', 'Award-winning spa', 'Michelin-starred restaurant'],
            'marketing_opportunities': ['Video content creation', 'Influencer partnerships', 'Virtual tours'],
            'content_suggestions': ['Spa treatment videos', 'Chef cooking demos', 'Guest testimonials', 'Sunset views']
        }
    }
    
    print(f"✅ Successfully analyzed: {mock_hotel_analysis['hotel_name']}")
    print(f"📍 Location: Oceanfront resort")
    print(f"💰 Average Rate: ${mock_hotel_analysis['price_range']['average']}")
    print(f"⭐ Amenities: {len(mock_hotel_analysis['amenities'])} found")
    print()
    
    # Step 2: Simulate Instagram analysis
    print("📸 STEP 2: INSTAGRAM PAGE ANALYSIS")
    print("-" * 40)
    print("Analyzing Instagram presence...")
    
    mock_instagram_analysis = {
        'url': 'https://instagram.com/grandluxuryresort',
        'username': 'grandluxuryresort',
        'analysis_status': 'success',
        'followers_estimate': '25K+',
        'engagement_estimate': 'High',
        'content_themes': ['luxury travel', 'spa', 'fine dining', 'ocean views'],
        'visual_style': 'Professional luxury hospitality',
        'marketing_insights': {
            'visual_quality': 'Excellent',
            'brand_consistency': 'Strong',
            'engagement_potential': 'Very High',
            'content_gaps': ['Booking CTAs', 'Pricing transparency', 'Local attractions']
        }
    }
    
    print(f"✅ Instagram: @{mock_instagram_analysis['username']}")
    print(f"👥 Followers: {mock_instagram_analysis['followers_estimate']}")
    print(f"📈 Engagement: {mock_instagram_analysis['engagement_estimate']}")
    print(f"🎨 Visual Quality: {mock_instagram_analysis['marketing_insights']['visual_quality']}")
    print()
    
    # Step 3: Create marketing strategy
    print("📋 STEP 3: CREATING MARKETING STRATEGY")
    print("-" * 40)
    print("AI is analyzing data and creating personalized strategy...")
    
    approval_interface = UserApprovalInterface()
    strategy = approval_interface.create_strategy_from_analysis(
        mock_hotel_analysis, mock_instagram_analysis
    )
    
    print(f"✅ Strategy created for: {strategy.hotel_name}")
    print(f"🎯 Target Audience: {', '.join(strategy.target_audience)}")
    print(f"💰 Budget Tier: {strategy.budget_recommendation['tier']}")
    print(f"💵 Monthly Budget: ${strategy.budget_recommendation['monthly_budget']:,.2f}")
    print()
    
    # Step 4: Display strategy for approval
    print("📊 STEP 4: STRATEGY REVIEW & APPROVAL")
    print("-" * 40)
    print("Here's your personalized marketing strategy:")
    print()
    
    strategy_display = approval_interface.display_strategy_for_approval(strategy)
    print(strategy_display)
    
    # Step 5: Simulate user approval
    print("🤔 STEP 5: USER APPROVAL SIMULATION")
    print("-" * 40)
    print("Simulating user approval process...")
    print("✅ User approves the strategy")
    print("📝 User adds note: 'This looks perfect! Let's launch it.'")
    print()
    
    # Approve the strategy
    approved_strategy = approval_interface.approve_strategy(
        strategy, "This looks perfect! Let's launch it."
    )
    
    # Step 6: Launch campaign
    print("🚀 STEP 6: LAUNCHING MARKETING CAMPAIGN")
    print("-" * 40)
    print("Converting approved strategy to campaign diagnosis...")
    
    # Create diagnosis from strategy
    onboarding = HotelOnboardingSystem()
    diagnosis = onboarding._create_diagnosis_from_strategy(approved_strategy)
    
    print("Generated Campaign Diagnosis:")
    print("-" * 35)
    print(diagnosis)
    print()
    
    print("🤖 AI Agents are now working on your campaign...")
    print("This would normally take a few minutes...")
    print()
    
    # Simulate campaign launch
    print("✅ CAMPAIGN LAUNCHED SUCCESSFULLY!")
    print("-" * 40)
    print("Your marketing campaign is now active!")
    print("Generated files:")
    print("  📄 market_research_report.md")
    print("  📄 google_ads_campaign.md")
    print("  📄 optimization_report.md")
    print("  📄 workflow_results.json")
    print()
    
    # Step 7: Show modification example
    print("✏️ BONUS: STRATEGY MODIFICATION EXAMPLE")
    print("-" * 45)
    print("What if the user wanted to modify the strategy?")
    print()
    
    # Create a modified strategy
    modified_strategy = approval_interface.modify_strategy(
        strategy,
        [
            "Increase budget by 30% for peak season",
            "Add family-friendly targeting",
            "Focus on local events and attractions"
        ],
        "Please make these changes for the holiday season"
    )
    
    print("User requested modifications:")
    for i, mod in enumerate(modified_strategy.modifications, 1):
        print(f"  {i}. {mod}")
    print()
    print(f"Strategy Status: {modified_strategy.status}")
    print(f"User Notes: {modified_strategy.user_notes}")
    print()
    
    print("🎉 ONBOARDING DEMO COMPLETED!")
    print("=" * 40)
    print("The system successfully:")
    print("✅ Analyzed hotel website and Instagram")
    print("✅ Created personalized marketing strategy")
    print("✅ Got user approval and modifications")
    print("✅ Launched AI-powered marketing campaign")
    print()
    print("🚀 Ready for real hotel onboarding!")
    print("Run: python onboarding.py")

def demo_url_analysis():
    """Demonstrate URL analysis capabilities"""
    print("\n🔍 URL ANALYSIS CAPABILITIES DEMO")
    print("=" * 45)
    
    analyzer = HotelAnalyzer()
    
    # Show what the analyzer looks for
    print("The hotel analyzer extracts:")
    print("• Hotel name and description")
    print("• Pricing information and rates")
    print("• Amenities and features")
    print("• Location and address data")
    print("• Social media links")
    print("• Reviews and ratings")
    print("• Marketing opportunities")
    print()
    
    print("Example analysis patterns:")
    print("• Price patterns: $123.45, from $200, starting at $150")
    print("• Amenities: wifi, pool, spa, restaurant, parking")
    print("• Location: addresses, 'near airport', 'downtown'")
    print("• Social: facebook.com, instagram.com, twitter.com")
    print("• Reviews: 'reviews', 'ratings', 'stars', 'tripadvisor'")
    print()

def main():
    """Run the complete demo"""
    demo_complete_workflow()
    demo_url_analysis()
    
    print("\n📱 HOW TO USE THE ONBOARDING SYSTEM")
    print("=" * 45)
    print("1. Run: python onboarding.py")
    print("2. Enter your hotel's website URL")
    print("3. Optionally provide Instagram URL")
    print("4. Review the generated strategy")
    print("5. Approve, modify, or reject")
    print("6. Launch your AI marketing campaign!")
    print()
    print("🎯 Perfect for:")
    print("• Hotel marketing managers")
    print("• Digital marketing agencies")
    print("• Hotel owners and operators")
    print("• Marketing consultants")

if __name__ == "__main__":
    main()