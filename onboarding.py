"""
Hotel Marketing Onboarding System
Complete user onboarding workflow with URL analysis and strategy approval
"""
import os
import sys
from typing import Dict, Any, Optional, List
from datetime import datetime

# Add current directory to path for imports
sys.path.append('.')

from utils.hotel_analyzer import HotelAnalyzer, analyze_hotel_from_url, analyze_instagram_from_url
from utils.user_approval import UserApprovalInterface, MarketingStrategy
from utils.validators import validate_and_sanitize_input, ValidationError
from main import run_diagnosis_workflow

class HotelOnboardingSystem:
    """Complete hotel marketing onboarding system"""
    
    def __init__(self):
        self.analyzer = HotelAnalyzer()
        self.approval_interface = UserApprovalInterface()
        self.current_strategy = None
        self.hotel_analysis = None
        self.instagram_analysis = None
    
    def start_onboarding(self):
        """Start the complete onboarding process"""
        print("🏨 WELCOME TO tphagent HOTEL MARKETING ONBOARDING")
        print("=" * 60)
        print("Let's analyze your hotel and create a personalized marketing strategy!")
        print()
        
        # Step 1: Get hotel information
        hotel_url = self._get_hotel_url()
        if not hotel_url:
            print("❌ No hotel URL provided. Exiting onboarding.")
            return None
        
        # Step 2: Analyze hotel website
        print("\n🔍 STEP 1: ANALYZING HOTEL WEBSITE")
        print("-" * 40)
        self.hotel_analysis = self.analyzer.analyze_hotel_url(hotel_url)
        
        if self.hotel_analysis.get('analysis_status') != 'success':
            print(f"❌ Failed to analyze hotel website: {self.hotel_analysis.get('error', 'Unknown error')}")
            return None
        
        # Step 3: Ask for Instagram (optional)
        instagram_url = self._get_instagram_url()
        if instagram_url:
            print("\n📸 STEP 2: ANALYZING INSTAGRAM PAGE")
            print("-" * 40)
            self.instagram_analysis = self.analyzer.analyze_instagram_page(instagram_url)
        
        # Step 4: Create marketing strategy
        print("\n📋 STEP 3: CREATING MARKETING STRATEGY")
        print("-" * 40)
        self.current_strategy = self.approval_interface.create_strategy_from_analysis(
            self.hotel_analysis, self.instagram_analysis
        )
        
        # Step 5: Display strategy for approval
        print("\n📊 STEP 4: STRATEGY REVIEW & APPROVAL")
        print("-" * 40)
        self._display_strategy_for_approval()
        
        # Step 6: Get user approval
        approval_decision = self._get_user_approval()
        
        if approval_decision == 'approve':
            return self._approve_and_launch()
        elif approval_decision == 'modify':
            return self._modify_and_launch()
        else:
            print("❌ Strategy rejected. Onboarding cancelled.")
            return None
    
    def _get_hotel_url(self) -> Optional[str]:
        """Get hotel URL from user with validation"""
        print("Please provide your hotel's website URL:")
        print("Examples:")
        print("  • https://www.yourhotel.com")
        print("  • yourhotel.com")
        print("  • www.yourhotel.com")
        print()
        
        while True:
            url = input("Hotel URL: ").strip()
            if not url:
                print("❌ Please enter a valid URL")
                continue
            
            # Validate URL using our validation system
            is_valid, sanitized_data, validation_results = validate_and_sanitize_input(
                {'hotel_url': url}, 'onboarding'
            )
            
            if not is_valid:
                error_messages = [result.message for result in validation_results if not result.is_valid]
                print(f"❌ Validation failed: {'; '.join(error_messages)}")
                continue
            
            return sanitized_data['hotel_url']
    
    def _get_instagram_url(self) -> Optional[str]:
        """Get Instagram URL from user (optional) with validation"""
        print("\nDo you have an Instagram page for your hotel? (Optional)")
        print("This will help us understand your visual branding and content strategy.")
        print()
        
        while True:
            choice = input("Enter Instagram URL (or press Enter to skip): ").strip()
            if not choice:
                return None
            
            # Handle @username format
            if choice.startswith('@'):
                choice = f"https://instagram.com/{choice[1:]}"
            
            # Validate Instagram URL using our validation system
            is_valid, sanitized_data, validation_results = validate_and_sanitize_input(
                {'instagram_url': choice}, 'onboarding'
            )
            
            if not is_valid:
                error_messages = [result.message for result in validation_results if not result.is_valid]
                print(f"❌ Validation failed: {'; '.join(error_messages)}")
                continue
            
            return sanitized_data['instagram_url']
    
    def _display_strategy_for_approval(self):
        """Display the marketing strategy for user review"""
        if not self.current_strategy:
            print("❌ No strategy to display")
            return
        
        strategy_display = self.approval_interface.display_strategy_for_approval(self.current_strategy)
        print(strategy_display)
        
        # Save strategy for reference
        strategy_file = self.approval_interface.save_strategy(self.current_strategy)
        print(f"💾 Strategy saved to: {strategy_file}")
    
    def _get_user_approval(self) -> str:
        """Get user approval decision"""
        print("\n🤔 WHAT WOULD YOU LIKE TO DO?")
        print("-" * 35)
        print("1. ✅ APPROVE - Launch this strategy")
        print("2. ✏️  MODIFY - Make changes to the strategy")
        print("3. ❌ REJECT - Cancel and start over")
        print()
        
        while True:
            choice = input("Enter your choice (1/2/3): ").strip()
            if choice == '1':
                return 'approve'
            elif choice == '2':
                return 'modify'
            elif choice == '3':
                return 'reject'
            else:
                print("❌ Please enter 1, 2, or 3")
                continue
    
    def _approve_and_launch(self) -> Dict[str, Any]:
        """Approve strategy and launch marketing campaign"""
        print("\n✅ STRATEGY APPROVED!")
        print("-" * 25)
        
        # Get user notes
        user_notes = input("Any additional notes for the campaign? (Optional): ").strip()
        
        # Approve the strategy
        approved_strategy = self.approval_interface.approve_strategy(
            self.current_strategy, user_notes
        )
        
        # Save approved strategy
        strategy_file = self.approval_interface.save_strategy(approved_strategy)
        
        # Launch marketing campaign
        print("\n🚀 LAUNCHING MARKETING CAMPAIGN")
        print("-" * 35)
        return self._launch_campaign(approved_strategy)
    
    def _modify_and_launch(self) -> Dict[str, Any]:
        """Modify strategy based on user feedback and launch"""
        print("\n✏️ STRATEGY MODIFICATION")
        print("-" * 25)
        
        modifications = []
        print("What would you like to modify? (Enter one modification per line, press Enter when done)")
        print("Examples:")
        print("  • Change target audience to business travelers")
        print("  • Increase budget by 20%")
        print("  • Focus on spa services")
        print("  • Add family-friendly amenities")
        print()
        
        while True:
            modification = input("Modification: ").strip()
            if not modification:
                break
            modifications.append(modification)
        
        if modifications:
            # Get user notes
            user_notes = input("Additional notes: ").strip()
            
            # Modify the strategy
            modified_strategy = self.approval_interface.modify_strategy(
                self.current_strategy, modifications, user_notes
            )
            
            # Save modified strategy
            strategy_file = self.approval_interface.save_strategy(modified_strategy)
            
            # Display modified strategy
            print("\n📊 MODIFIED STRATEGY:")
            print("-" * 25)
            modified_display = self.approval_interface.display_strategy_for_approval(modified_strategy)
            print(modified_display)
            
            # Ask for final approval
            final_approval = input("\nApprove this modified strategy? (y/n): ").strip().lower()
            if final_approval == 'y':
                return self._launch_campaign(modified_strategy)
            else:
                print("❌ Strategy not approved. Onboarding cancelled.")
                return None
        else:
            print("No modifications provided. Launching original strategy...")
            return self._launch_campaign(self.current_strategy)
    
    def _launch_campaign(self, strategy: MarketingStrategy) -> Dict[str, Any]:
        """Launch the marketing campaign using the agent system"""
        print("\n🎯 LAUNCHING AI MARKETING CAMPAIGN")
        print("-" * 40)
        
        # Create diagnosis from strategy
        diagnosis = self._create_diagnosis_from_strategy(strategy)
        
        print("📊 Campaign Diagnosis:")
        print(diagnosis)
        print()
        
        # Run the marketing workflow
        print("🤖 AI Agents are now working on your campaign...")
        print("This may take a few minutes...")
        print()
        
        try:
            result = run_diagnosis_workflow(diagnosis)
            
            if result:
                print("✅ CAMPAIGN LAUNCHED SUCCESSFULLY!")
                print("-" * 40)
                print("Your marketing campaign is now active.")
                print("Check the 'outputs' folder for detailed reports.")
                
                return {
                    'status': 'success',
                    'strategy': strategy,
                    'campaign_result': result,
                    'timestamp': datetime.now().isoformat()
                }
            else:
                print("❌ Campaign launch failed. Please check the logs.")
                return {
                    'status': 'error',
                    'strategy': strategy,
                    'error': 'Campaign launch failed'
                }
                
        except Exception as e:
            print(f"❌ Error launching campaign: {e}")
            return {
                'status': 'error',
                'strategy': strategy,
                'error': str(e)
            }
    
    def _create_diagnosis_from_strategy(self, strategy: MarketingStrategy) -> str:
        """Create a diagnosis string from the approved strategy"""
        diagnosis_parts = []
        
        # Hotel name and basic info
        diagnosis_parts.append(f"Hotel: {strategy.hotel_name}")
        
        # Target audience
        if strategy.target_audience:
            diagnosis_parts.append(f"Target Audience: {', '.join(strategy.target_audience)}")
        
        # Key selling points
        if strategy.key_selling_points:
            diagnosis_parts.append(f"Key Selling Points: {', '.join(strategy.key_selling_points)}")
        
        # Marketing opportunities
        if strategy.marketing_opportunities:
            diagnosis_parts.append(f"Marketing Opportunities: {', '.join(strategy.marketing_opportunities)}")
        
        # Budget information
        budget = strategy.budget_recommendation
        diagnosis_parts.append(f"Budget Tier: {budget['tier']} (${budget['monthly_budget']:,.2f}/month)")
        
        # Goals
        diagnosis_parts.append("Goals: Increase bookings, improve online visibility, optimize ad performance")
        
        # Current challenges (inferred from opportunities)
        if strategy.marketing_opportunities:
            challenges = []
            for opp in strategy.marketing_opportunities:
                if "needed" in opp.lower():
                    challenges.append(opp.replace(" needed", ""))
            if challenges:
                diagnosis_parts.append(f"Current Challenges: {', '.join(challenges)}")
        
        return " | ".join(diagnosis_parts)

def main():
    """Main onboarding entry point"""
    onboarding = HotelOnboardingSystem()
    result = onboarding.start_onboarding()
    
    if result and result.get('status') == 'success':
        print("\n🎉 ONBOARDING COMPLETED SUCCESSFULLY!")
        print("=" * 50)
        print("Your hotel marketing campaign is now live!")
        print("Monitor the 'outputs' folder for performance reports.")
    else:
        print("\n❌ ONBOARDING INCOMPLETE")
        print("=" * 30)
        print("Please try again or contact support.")

if __name__ == "__main__":
    main()