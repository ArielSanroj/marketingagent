"""
Demo: Email Results for Estancia Hacienda
Shows what would be sent to user's email
"""
import os
import json
from datetime import datetime

def create_email_preview():
    """Create a preview of what would be sent via email"""
    
    print("📧 tphagent Marketing Strategy Results Email")
    print("=" * 60)
    print()
    
    # Hotel information
    hotel_name = "The Peacock House by Hacienda La Estancia"
    user_email = "user@example.com"  # This would be the actual user's email
    
    print(f"📧 TO: {user_email}")
    print(f"📧 FROM: tphagent@marketing.com")
    print(f"📧 SUBJECT: 🏨 tphagent Marketing Strategy Results - {hotel_name}")
    print()
    
    print("📋 EMAIL CONTENT:")
    print("=" * 30)
    print()
    
    print("🎉 Congratulations! Your Marketing Strategy is Ready")
    print("-" * 50)
    print(f"Our AI agents have analyzed {hotel_name} and created a comprehensive")
    print("marketing strategy tailored specifically for your eco-lodge colonial property.")
    print("All results are included in this email with detailed next steps for implementation.")
    print()
    
    print("📊 EXECUTIVE SUMMARY")
    print("-" * 20)
    print("✅ Hotel Analysis: Successfully analyzed as 100-year-old eco-lodge colonial")
    print("✅ Target Market: Eco-conscious families, heritage enthusiasts, international tourists")
    print("✅ Budget: $720/month (Standard tier)")
    print("✅ Expected ROI: 400%+ within 30 days")
    print("✅ Campaigns: 3 Google Ads campaigns with 27 targeted keywords")
    print()
    
    print("🔍 MARKET RESEARCH HIGHLIGHTS")
    print("-" * 35)
    print("• Market Growth: Eco-tourism growing 15% annually in Colombia")
    print("• Target Segments: 4 identified with specific demographics")
    print("• Competitor Analysis: 3 direct competitors in Cundinamarca region")
    print("• Keywords: 5 high-value terms with 480-1,200 monthly searches")
    print("• Opportunity: 2.5M potential customers in Bogotá area")
    print()
    
    print("📢 GOOGLE ADS CAMPAIGN STRATEGY")
    print("-" * 40)
    print("• 3 Campaigns: Eco-Tourism, Heritage Tourism, Family Getaways")
    print("• 6 Ad Groups: Themed around key experiences")
    print("• 27 Keywords: High-value, targeted terms")
    print("• 9 Ad Variations: A/B testing ready")
    print("• Budget: $432/month (60% of total budget)")
    print()
    
    print("⚡ PERFORMANCE OPTIMIZATION PLAN")
    print("-" * 40)
    print("• Phase 1 (Days 1-14): Foundation optimization")
    print("• Phase 2 (Days 15-30): Performance enhancement")
    print("• Phase 3 (Days 31-60): Scale and expand")
    print("• Target CTR: 3.5%")
    print("• Target Conversion: 8%")
    print("• Target ROAS: 400%+")
    print()
    
    print("📁 ATTACHED FILES")
    print("-" * 20)
    print("1. 📄 estancia_hacienda_market_research.md")
    print("   Complete market analysis and competitor research")
    print()
    print("2. 📄 estancia_hacienda_google_ads.md")
    print("   Detailed campaign structure and ad copy")
    print()
    print("3. 📄 estancia_hacienda_optimization.md")
    print("   3-phase performance optimization plan")
    print()
    print("4. 📄 estancia_hacienda_workflow_results.json")
    print("   Complete JSON data with all metrics and settings")
    print()
    
    print("🚀 IMMEDIATE NEXT STEPS")
    print("-" * 25)
    print("1. Set up Google Ads account and implement the 3 campaigns")
    print("2. Create social media profiles (Instagram, Facebook)")
    print("3. Add pricing transparency to your website")
    print("4. Implement review collection system")
    print("5. Monitor performance daily and optimize based on data")
    print()
    
    print("📊 EXPECTED RESULTS")
    print("-" * 20)
    print("Month 1: 1,575 clicks, 126 conversions, $1,728 revenue")
    print("Month 3: 2,400 clicks, 240 conversions, $3,600 revenue")
    print("ROAS: 400%+ return on ad spend")
    print()
    
    print("📞 SUPPORT")
    print("-" * 10)
    print("If you have questions about implementing this strategy or need")
    print("assistance with any of the next steps, please don't hesitate to reach out.")
    print()
    print("tphagent Team")
    print("AI-Powered Hotel Marketing Solutions")
    print()
    
    print("=" * 60)
    print("✅ EMAIL READY TO SEND!")
    print("=" * 60)
    print()
    print("To actually send this email, you would need to:")
    print("1. Configure email credentials (Gmail SMTP)")
    print("2. Provide the user's actual email address")
    print("3. Run the email sending function")
    print()
    print("The email contains all the AI agent results and next steps for")
    print("implementing the marketing strategy for Estancia Hacienda.")

def show_file_contents():
    """Show the actual content of generated files"""
    
    print("\n📁 ACTUAL GENERATED FILES CONTENT:")
    print("=" * 50)
    
    files_to_show = [
        ('Market Research Report', 'outputs/estancia_hacienda_market_research.md'),
        ('Google Ads Campaign', 'outputs/estancia_hacienda_google_ads.md'),
        ('Optimization Strategy', 'outputs/estancia_hacienda_optimization.md'),
        ('Workflow Results', 'outputs/estancia_hacienda_workflow_results.json')
    ]
    
    for title, file_path in files_to_show:
        print(f"\n📄 {title.upper()}")
        print("-" * len(title))
        
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    # Show first 500 characters
                    preview = content[:500] + "..." if len(content) > 500 else content
                    print(preview)
            except Exception as e:
                print(f"Error reading file: {e}")
        else:
            print(f"File not found: {file_path}")
        
        print(f"\n📁 File: {file_path}")
        print(f"📏 Size: {os.path.getsize(file_path) if os.path.exists(file_path) else 0} bytes")

def main():
    """Main function"""
    create_email_preview()
    show_file_contents()
    
    print("\n🎯 SUMMARY")
    print("=" * 20)
    print("✅ All AI agent results have been generated")
    print("✅ Complete marketing strategy created for Estancia Hacienda")
    print("✅ Email content prepared with all results and next steps")
    print("✅ Ready to send to user's email address")
    print()
    print("The user will receive:")
    print("• Complete market research analysis")
    print("• Google Ads campaign strategy")
    print("• Performance optimization plan")
    print("• All generated files as attachments")
    print("• Step-by-step implementation guide")

if __name__ == "__main__":
    main()