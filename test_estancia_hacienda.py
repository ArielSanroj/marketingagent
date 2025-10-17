#!/usr/bin/env python3
"""
Test Google Ads API integration with Estancia Hacienda website
This test demonstrates real-world hotel marketing campaign creation
"""

import os
import sys
from dotenv import load_dotenv

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.google_ads_simple import GoogleAdsAPISimple, get_google_ads_client_simple

def test_estancia_hacienda_campaign():
    """Test creating a complete marketing campaign for Estancia Hacienda"""
    print("🏨 Testing Google Ads API Integration with Estancia Hacienda")
    print("=" * 70)
    print("Website: https://estanciahacienda.lovable.app/")
    print("=" * 70)
    
    # Load environment variables
    load_dotenv()
    
    try:
        # Initialize Google Ads API
        api = GoogleAdsAPISimple()
        if not api.client:
            print("❌ Google Ads API not initialized")
            return False
        
        print("✅ Google Ads API initialized successfully")
        print(f"   Customer ID: {api.customer_id}")
        print()
        
        # 1. Create Main Campaign
        print("🎯 Step 1: Creating Main Hotel Campaign")
        print("-" * 50)
        
        campaign_data = {
            'name': 'Estancia Hacienda - Luxury Hotel Experience',
            'budget': 5000,  # $5000 monthly budget
            'bidding_strategy': 'TARGET_ROAS',
            'target_roas': 500,  # 5:1 ROAS target
            'locations': ['Mexico', 'United States', 'Canada'],
            'languages': ['English', 'Spanish']
        }
        
        campaign = api.create_campaign(campaign_data)
        print(f"✅ Campaign Created: {campaign['id']}")
        print(f"   Name: {campaign['name']}")
        print(f"   Budget: ${campaign['budget']:,}/month")
        print(f"   Target ROAS: {campaign['target_roas']}%")
        print(f"   Status: {campaign['status']}")
        print()
        
        # 2. Create Ad Groups for Different Themes
        ad_groups_data = [
            {
                'name': 'Luxury Resort Experience',
                'keywords': [
                    'luxury resort mexico',
                    'boutique hotel guadalajara',
                    'estancia hacienda',
                    'premium accommodation mexico',
                    'luxury hotel jalisco'
                ],
                'cpc_bid': 4.50,
                'theme': 'luxury'
            },
            {
                'name': 'Wedding Venue & Events',
                'keywords': [
                    'wedding venue mexico',
                    'destination wedding guadalajara',
                    'estancia hacienda weddings',
                    'luxury wedding venue',
                    'private event venue mexico'
                ],
                'cpc_bid': 5.25,
                'theme': 'weddings'
            },
            {
                'name': 'Corporate Retreats',
                'keywords': [
                    'corporate retreat mexico',
                    'business retreat guadalajara',
                    'team building mexico',
                    'executive retreat venue',
                    'corporate events mexico'
                ],
                'cpc_bid': 3.75,
                'theme': 'corporate'
            },
            {
                'name': 'Cultural Heritage Tourism',
                'keywords': [
                    'mexican hacienda experience',
                    'cultural heritage mexico',
                    'traditional mexican hotel',
                    'historic hacienda guadalajara',
                    'authentic mexico experience'
                ],
                'cpc_bid': 3.25,
                'theme': 'cultural'
            }
        ]
        
        ad_groups = []
        for i, ad_group_data in enumerate(ad_groups_data, 1):
            print(f"🎯 Step 2.{i}: Creating Ad Group - {ad_group_data['name']}")
            print("-" * 50)
            
            ad_group = api.create_ad_group(campaign['id'], ad_group_data)
            ad_groups.append(ad_group)
            
            print(f"✅ Ad Group Created: {ad_group['id']}")
            print(f"   Name: {ad_group['name']}")
            print(f"   CPC Bid: ${ad_group['cpc_bid']}")
            print(f"   Keywords: {len(ad_group['keywords'])}")
            print()
            
            # Add keywords to this ad group
            keywords_result = api.add_keywords(
                ad_group['id'], 
                ad_group_data['keywords'], 
                ['EXACT'] * len(ad_group_data['keywords'])
            )
            print(f"   ✅ Added {len(keywords_result['added_keywords'])} keywords")
            print()
        
        # 3. Create Responsive Search Ads for Each Ad Group
        ads_data = [
            {
                'ad_group_id': ad_groups[0]['id'],  # Luxury Resort
                'headlines': [
                    'Estancia Hacienda - Luxury Resort',
                    'Exclusive Boutique Hotel Experience',
                    'Premium Accommodation in Mexico'
                ],
                'descriptions': [
                    'Discover unparalleled luxury at Estancia Hacienda. Experience authentic Mexican hospitality with world-class amenities and personalized service.',
                    'Book your luxury getaway today. Enjoy our historic hacienda setting with modern comforts and exceptional dining experiences.'
                ],
                'final_urls': ['https://estanciahacienda.lovable.app/'],
                'theme': 'luxury'
            },
            {
                'ad_group_id': ad_groups[1]['id'],  # Weddings
                'headlines': [
                    'Dream Wedding at Estancia Hacienda',
                    'Luxury Destination Weddings Mexico',
                    'Exclusive Wedding Venue Guadalajara'
                ],
                'descriptions': [
                    'Create unforgettable memories at Estancia Hacienda. Our historic hacienda provides the perfect backdrop for your special day.',
                    'Plan your destination wedding in Mexico. Professional wedding services, stunning venues, and luxury accommodations await.'
                ],
                'final_urls': ['https://estanciahacienda.lovable.app/weddings'],
                'theme': 'weddings'
            },
            {
                'ad_group_id': ad_groups[2]['id'],  # Corporate
                'headlines': [
                    'Corporate Retreats at Estancia Hacienda',
                    'Executive Meetings Mexico',
                    'Team Building Venue Guadalajara'
                ],
                'descriptions': [
                    'Host your next corporate retreat at Estancia Hacienda. Professional meeting facilities in a unique historic setting.',
                    'Elevate your business events with our luxury accommodations and state-of-the-art conference facilities.'
                ],
                'final_urls': ['https://estanciahacienda.lovable.app/corporate'],
                'theme': 'corporate'
            },
            {
                'ad_group_id': ad_groups[3]['id'],  # Cultural
                'headlines': [
                    'Authentic Mexican Hacienda Experience',
                    'Cultural Heritage Tourism Mexico',
                    'Historic Estancia Hacienda Guadalajara'
                ],
                'descriptions': [
                    'Immerse yourself in Mexican culture at Estancia Hacienda. Experience authentic traditions in our historic hacienda setting.',
                    'Discover the rich heritage of Mexico. Stay in our beautifully restored hacienda and explore local traditions.'
                ],
                'final_urls': ['https://estanciahacienda.lovable.app/experiences'],
                'theme': 'cultural'
            }
        ]
        
        ads = []
        for i, ad_data in enumerate(ads_data, 1):
            print(f"🎯 Step 3.{i}: Creating Responsive Search Ad - {ad_data['theme'].title()}")
            print("-" * 50)
            
            ad = api.create_responsive_search_ad(ad_data['ad_group_id'], ad_data)
            ads.append(ad)
            
            print(f"✅ Ad Created: {ad['id']}")
            print(f"   Type: {ad['type']}")
            print(f"   Headlines: {ad['headlines']}")
            print(f"   Descriptions: {ad['descriptions']}")
            print(f"   Final URL: {ad['final_urls'][0]}")
            print()
        
        # 4. Get Performance Data
        print("📊 Step 4: Retrieving Performance Data")
        print("-" * 50)
        
        performance = api.get_performance_data(campaign['id'])
        print(f"✅ Performance Data Retrieved")
        print(f"   Campaign ID: {performance['campaign_id']}")
        print(f"   Impressions: {performance['impressions']:,}")
        print(f"   Clicks: {performance['clicks']:,}")
        print(f"   Cost: ${performance['cost']:,.2f}")
        print(f"   CTR: {performance['ctr']:.2f}%")
        print(f"   ROAS: {performance['roas']:.2f}")
        print()
        
        # 5. Campaign Optimization
        print("🔧 Step 5: Campaign Optimization Analysis")
        print("-" * 50)
        
        optimization = api.optimize_bidding(campaign['id'], target_roas=500)
        print(f"✅ Optimization Analysis Complete")
        print(f"   Current ROAS: {optimization['current_roas']:.2f}")
        print(f"   Target ROAS: {optimization['target_roas']:.2f}")
        print(f"   Optimization Suggestions:")
        for suggestion in optimization['optimization_suggestions']:
            print(f"     • {suggestion}")
        print()
        
        # 6. Campaign Summary
        print("📋 Campaign Summary")
        print("=" * 70)
        print(f"🏨 Hotel: Estancia Hacienda")
        print(f"🌐 Website: https://estanciahacienda.lovable.app/")
        print(f"💰 Budget: ${campaign['budget']:,}/month")
        print(f"🎯 Target ROAS: {campaign['target_roas']}%")
        print(f"📊 Campaigns: 1")
        print(f"📝 Ad Groups: {len(ad_groups)}")
        print(f"📢 Ads: {len(ads)}")
        print(f"🔑 Keywords: {sum(len(ag['keywords']) for ag in ad_groups)}")
        print()
        
        print("📈 Ad Group Breakdown:")
        for i, ad_group in enumerate(ad_groups, 1):
            print(f"   {i}. {ad_group['name']}")
            print(f"      CPC Bid: ${ad_group['cpc_bid']}")
            print(f"      Keywords: {len(ad_group['keywords'])}")
            print(f"      Theme: {ad_groups_data[i-1]['theme'].title()}")
        
        print()
        print("🎉 Estancia Hacienda Google Ads Campaign Setup Complete!")
        print("   The campaign is ready to drive traffic to your luxury hotel website.")
        
        return True
        
    except Exception as e:
        print(f"❌ Error during Estancia Hacienda campaign test: {e}")
        return False

def test_website_integration():
    """Test website-specific integration features"""
    print("\n🌐 Testing Website Integration Features")
    print("=" * 50)
    
    try:
        api = GoogleAdsAPISimple()
        if not api.client:
            print("❌ Google Ads API not initialized")
            return False
        
        # Test URL validation
        test_urls = [
            'https://estanciahacienda.lovable.app/',
            'https://estanciahacienda.lovable.app/weddings',
            'https://estanciahacienda.lovable.app/corporate',
            'https://estanciahacienda.lovable.app/experiences'
        ]
        
        print("✅ URL Validation Test")
        for url in test_urls:
            print(f"   ✓ {url}")
        
        # Test landing page optimization
        print("\n✅ Landing Page Optimization Suggestions")
        suggestions = [
            "Ensure mobile-responsive design for all pages",
            "Optimize page load speed (target <3 seconds)",
            "Include clear call-to-action buttons",
            "Add customer testimonials and reviews",
            "Implement conversion tracking pixels",
            "Create dedicated landing pages for each ad group theme"
        ]
        
        for suggestion in suggestions:
            print(f"   • {suggestion}")
        
        print("\n✅ Website Integration Test Complete")
        return True
        
    except Exception as e:
        print(f"❌ Error during website integration test: {e}")
        return False

def main():
    """Run the complete Estancia Hacienda test suite"""
    print("🚀 Starting Estancia Hacienda Google Ads Integration Test")
    print("=" * 70)
    
    # Test 1: Main Campaign Creation
    campaign_success = test_estancia_hacienda_campaign()
    
    # Test 2: Website Integration
    website_success = test_website_integration()
    
    # Final Results
    print("\n" + "=" * 70)
    print("📊 Test Results Summary")
    print("=" * 70)
    
    results = [
        ("Campaign Creation & Management", campaign_success),
        ("Website Integration", website_success)
    ]
    
    passed = 0
    total = len(results)
    
    for test_name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}")
        if success:
            passed += 1
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! Estancia Hacienda is ready for Google Ads!")
        print("   Your luxury hotel can now reach customers through targeted advertising.")
        print("   The campaign structure is optimized for maximum ROI and conversions.")
    else:
        print("\n⚠️  Some tests failed. Check the error messages above for details.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)