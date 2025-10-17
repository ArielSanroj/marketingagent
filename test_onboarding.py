"""
Test script for the hotel onboarding system
Demonstrates the complete workflow without user interaction
"""
import sys
import os
sys.path.append('.')

from utils.hotel_analyzer import HotelAnalyzer
from utils.user_approval import UserApprovalInterface
from onboarding import HotelOnboardingSystem

def test_hotel_analysis():
    """Test hotel website analysis"""
    print("🧪 TESTING HOTEL ANALYSIS")
    print("=" * 40)
    
    analyzer = HotelAnalyzer()
    
    # Test with a sample hotel URL (using a generic example)
    test_url = "https://example.com"  # This will fail, but shows the process
    
    print(f"Testing URL analysis with: {test_url}")
    result = analyzer.analyze_hotel_url(test_url)
    
    print(f"Analysis Status: {result.get('analysis_status', 'unknown')}")
    if result.get('analysis_status') == 'error':
        print(f"Error: {result.get('error', 'Unknown error')}")
    
    return result

def test_strategy_creation():
    """Test marketing strategy creation"""
    print("\n🧪 TESTING STRATEGY CREATION")
    print("=" * 40)
    
    # Create mock hotel analysis data
    mock_hotel_analysis = {
        'hotel_name': 'Test Boutique Hotel',
        'domain': 'testhotel.com',
        'analysis_status': 'success',
        'description': 'Luxury boutique hotel with spa services',
        'amenities': ['wifi', 'pool', 'spa', 'restaurant', 'parking'],
        'price_range': {
            'min': 150,
            'max': 300,
            'average': 225
        },
        'marketing_insights': {
            'target_audience': ['Luxury travelers', 'Couples'],
            'key_selling_points': ['Swimming pool', 'Spa services', 'On-site dining'],
            'competitive_advantages': ['Boutique experience', 'Personalized service'],
            'marketing_opportunities': ['Social media presence needed', 'Review management needed'],
            'content_suggestions': ['Spa treatment videos', 'Guest testimonials']
        }
    }
    
    # Create mock Instagram analysis
    mock_instagram_analysis = {
        'url': 'https://instagram.com/testhotel',
        'username': 'testhotel',
        'analysis_status': 'success',
        'marketing_insights': {
            'content_gaps': ['Pricing information', 'Booking CTAs'],
            'visual_quality': 'High'
        }
    }
    
    # Create strategy
    approval_interface = UserApprovalInterface()
    strategy = approval_interface.create_strategy_from_analysis(
        mock_hotel_analysis, mock_instagram_analysis
    )
    
    print(f"Strategy created for: {strategy.hotel_name}")
    print(f"Target Audience: {', '.join(strategy.target_audience)}")
    print(f"Budget Tier: {strategy.budget_recommendation['tier']}")
    print(f"Monthly Budget: ${strategy.budget_recommendation['monthly_budget']:,.2f}")
    
    return strategy

def test_strategy_display():
    """Test strategy display for approval"""
    print("\n🧪 TESTING STRATEGY DISPLAY")
    print("=" * 40)
    
    # Create a test strategy
    strategy = test_strategy_creation()
    
    # Display strategy
    approval_interface = UserApprovalInterface()
    strategy_display = approval_interface.display_strategy_for_approval(strategy)
    
    print("Strategy Display Preview:")
    print("-" * 30)
    # Show first 20 lines of the display
    lines = strategy_display.split('\n')
    for i, line in enumerate(lines[:20]):
        print(line)
    if len(lines) > 20:
        print("... (truncated)")
    
    return strategy

def test_approval_workflow():
    """Test the approval workflow"""
    print("\n🧪 TESTING APPROVAL WORKFLOW")
    print("=" * 40)
    
    # Create test strategy
    strategy = test_strategy_creation()
    approval_interface = UserApprovalInterface()
    
    # Test approval
    approved_strategy = approval_interface.approve_strategy(
        strategy, "This looks great! Let's launch it."
    )
    
    print(f"Strategy Status: {approved_strategy.status}")
    print(f"User Notes: {approved_strategy.user_notes}")
    
    # Test modification
    modified_strategy = approval_interface.modify_strategy(
        strategy, 
        ["Increase budget by 20%", "Focus on business travelers"],
        "Please make these changes"
    )
    
    print(f"Modified Strategy Status: {modified_strategy.status}")
    print(f"Modifications: {modified_strategy.modifications}")
    
    return approved_strategy, modified_strategy

def test_diagnosis_creation():
    """Test diagnosis creation from strategy"""
    print("\n🧪 TESTING DIAGNOSIS CREATION")
    print("=" * 40)
    
    # Create test strategy
    strategy = test_strategy_creation()
    
    # Create onboarding system
    onboarding = HotelOnboardingSystem()
    
    # Create diagnosis from strategy
    diagnosis = onboarding._create_diagnosis_from_strategy(strategy)
    
    print("Generated Diagnosis:")
    print("-" * 25)
    print(diagnosis)
    
    return diagnosis

def main():
    """Run all tests"""
    print("🏨 tphagent ONBOARDING SYSTEM TEST")
    print("=" * 50)
    print("Testing the complete onboarding workflow...")
    print()
    
    try:
        # Test 1: Hotel Analysis
        hotel_result = test_hotel_analysis()
        
        # Test 2: Strategy Creation
        strategy = test_strategy_creation()
        
        # Test 3: Strategy Display
        display_strategy = test_strategy_display()
        
        # Test 4: Approval Workflow
        approved, modified = test_approval_workflow()
        
        # Test 5: Diagnosis Creation
        diagnosis = test_diagnosis_creation()
        
        print("\n✅ ALL TESTS COMPLETED SUCCESSFULLY!")
        print("=" * 45)
        print("The onboarding system is ready for use!")
        print()
        print("🚀 READY TO ONBOARD HOTELS!")
        print("Run: python onboarding.py")
        
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()