#!/usr/bin/env python3
"""
Test script for real Google Ads API integration
This script tests the actual Google Ads API implementation
"""

import os
import sys
from dotenv import load_dotenv

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.google_ads import GoogleAdsAPI, get_google_ads_client

def test_google_ads_api_initialization():
    """Test Google Ads API initialization"""
    print("🧪 Testing Google Ads API initialization...")
    
    try:
        api = GoogleAdsAPI()
        if api.client:
            print("✅ Google Ads API initialized successfully")
            print(f"   Customer ID: {api.customer_id}")
            return True
        else:
            print("❌ Google Ads API initialization failed")
            return False
    except Exception as e:
        print(f"❌ Error initializing Google Ads API: {e}")
        return False

def test_campaign_creation():
    """Test campaign creation"""
    print("\n🧪 Testing campaign creation...")
    
    try:
        api = GoogleAdsAPI()
        if not api.client:
            print("❌ Google Ads API not initialized, skipping test")
            return False
        
        campaign_data = {
            'name': 'Test Hotel Campaign - API Integration',
            'budget': 1000,
            'bidding_strategy': 'TARGET_ROAS',
            'target_roas': 400,
            'locations': ['United States']
        }
        
        campaign = api.create_campaign(campaign_data)
        print(f"✅ Campaign created successfully: {campaign['id']}")
        print(f"   Name: {campaign['name']}")
        print(f"   Status: {campaign['status']}")
        print(f"   Budget: ${campaign['budget']}")
        
        return campaign['id']
        
    except Exception as e:
        print(f"❌ Error creating campaign: {e}")
        return None

def test_ad_group_creation(campaign_id):
    """Test ad group creation"""
    print(f"\n🧪 Testing ad group creation for campaign {campaign_id}...")
    
    try:
        api = GoogleAdsAPI()
        if not api.client:
            print("❌ Google Ads API not initialized, skipping test")
            return False
        
        ad_group_data = {
            'name': 'Test Ad Group - Luxury Hotels',
            'keywords': ['luxury hotel', 'boutique hotel', 'resort'],
            'cpc_bid': 3.50
        }
        
        ad_group = api.create_ad_group(campaign_id, ad_group_data)
        print(f"✅ Ad group created successfully: {ad_group['id']}")
        print(f"   Name: {ad_group['name']}")
        print(f"   CPC Bid: ${ad_group['cpc_bid']}")
        
        return ad_group['id']
        
    except Exception as e:
        print(f"❌ Error creating ad group: {e}")
        return None

def test_responsive_search_ad_creation(ad_group_id):
    """Test responsive search ad creation"""
    print(f"\n🧪 Testing responsive search ad creation for ad group {ad_group_id}...")
    
    try:
        api = GoogleAdsAPI()
        if not api.client:
            print("❌ Google Ads API not initialized, skipping test")
            return False
        
        ad_data = {
            'headlines': [
                'Luxury Hotel Experience',
                'Book Direct & Save 20%',
                'Exclusive Resort Deals'
            ],
            'descriptions': [
                'Experience unparalleled luxury with world-class service and amenities.',
                'Limited time offer - book your luxury getaway today and save big.'
            ],
            'final_urls': ['https://example-luxury-hotel.com']
        }
        
        ad = api.create_responsive_search_ad(ad_group_id, ad_data)
        print(f"✅ Responsive search ad created successfully: {ad['id']}")
        print(f"   Type: {ad['type']}")
        print(f"   Headlines: {ad['headlines']}")
        print(f"   Descriptions: {ad['descriptions']}")
        
        return ad['id']
        
    except Exception as e:
        print(f"❌ Error creating responsive search ad: {e}")
        return None

def test_keywords_addition(ad_group_id):
    """Test keywords addition"""
    print(f"\n🧪 Testing keywords addition for ad group {ad_group_id}...")
    
    try:
        api = GoogleAdsAPI()
        if not api.client:
            print("❌ Google Ads API not initialized, skipping test")
            return False
        
        keywords = [
            'luxury hotel miami',
            'boutique resort florida',
            'premium accommodation'
        ]
        match_types = ['EXACT', 'PHRASE', 'BROAD']
        
        result = api.add_keywords(ad_group_id, keywords, match_types)
        print(f"✅ Keywords added successfully")
        print(f"   Added keywords: {len(result['added_keywords'])}")
        for kw in result['added_keywords']:
            print(f"     - {kw['keyword']} ({kw['match_type']})")
        
        return True
        
    except Exception as e:
        print(f"❌ Error adding keywords: {e}")
        return False

def test_performance_data(campaign_id):
    """Test performance data retrieval"""
    print(f"\n🧪 Testing performance data retrieval for campaign {campaign_id}...")
    
    try:
        api = GoogleAdsAPI()
        if not api.client:
            print("❌ Google Ads API not initialized, skipping test")
            return False
        
        performance = api.get_performance_data(campaign_id)
        print(f"✅ Performance data retrieved successfully")
        print(f"   Campaign ID: {performance['campaign_id']}")
        print(f"   Impressions: {performance['impressions']}")
        print(f"   Clicks: {performance['clicks']}")
        print(f"   Cost: ${performance['cost']:.2f}")
        print(f"   CTR: {performance['ctr']:.2f}%")
        print(f"   ROAS: {performance['roas']:.2f}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error retrieving performance data: {e}")
        return False

def test_campaign_listing():
    """Test campaign listing"""
    print(f"\n🧪 Testing campaign listing...")
    
    try:
        api = GoogleAdsAPI()
        if not api.client:
            print("❌ Google Ads API not initialized, skipping test")
            return False
        
        campaigns = api.list_campaigns()
        print(f"✅ Campaigns listed successfully")
        print(f"   Found {len(campaigns)} campaigns")
        
        for campaign in campaigns[:5]:  # Show first 5 campaigns
            print(f"     - {campaign['name']} (ID: {campaign['id']}, Status: {campaign['status']})")
        
        return True
        
    except Exception as e:
        print(f"❌ Error listing campaigns: {e}")
        return False

def test_client_selection():
    """Test client selection logic"""
    print(f"\n🧪 Testing client selection logic...")
    
    try:
        # Test with simulators enabled
        os.environ['USE_SIMULATORS'] = 'true'
        client = get_google_ads_client()
        print(f"✅ Simulator client selected: {type(client).__name__}")
        
        # Test with simulators disabled
        os.environ['USE_SIMULATORS'] = 'false'
        client = get_google_ads_client()
        print(f"✅ Real API client selected: {type(client).__name__}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing client selection: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Starting Google Ads API Integration Tests")
    print("=" * 50)
    
    # Load environment variables
    load_dotenv()
    
    # Test results
    results = []
    
    # Test 1: API Initialization
    results.append(("API Initialization", test_google_ads_api_initialization()))
    
    # Test 2: Client Selection
    results.append(("Client Selection", test_client_selection()))
    
    # Test 3: Campaign Listing (if API is available)
    if results[0][1]:  # If API initialization succeeded
        results.append(("Campaign Listing", test_campaign_listing()))
        
        # Test 4: Campaign Creation
        campaign_id = test_campaign_creation()
        if campaign_id:
            results.append(("Campaign Creation", True))
            
            # Test 5: Ad Group Creation
            ad_group_id = test_ad_group_creation(campaign_id)
            if ad_group_id:
                results.append(("Ad Group Creation", True))
                
                # Test 6: Responsive Search Ad Creation
                ad_id = test_responsive_search_ad_creation(ad_group_id)
                if ad_id:
                    results.append(("Responsive Search Ad Creation", True))
                
                # Test 7: Keywords Addition
                results.append(("Keywords Addition", test_keywords_addition(ad_group_id)))
            
            # Test 8: Performance Data
            results.append(("Performance Data", test_performance_data(campaign_id)))
        else:
            results.append(("Campaign Creation", False))
    else:
        print("\n⚠️  Skipping API-dependent tests due to initialization failure")
        results.extend([
            ("Campaign Listing", False),
            ("Campaign Creation", False),
            ("Ad Group Creation", False),
            ("Responsive Search Ad Creation", False),
            ("Keywords Addition", False),
            ("Performance Data", False)
        ])
    
    # Print summary
    print("\n" + "=" * 50)
    print("📊 Test Results Summary")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    
    for test_name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}")
        if success:
            passed += 1
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Google Ads API integration is working correctly.")
    else:
        print("⚠️  Some tests failed. Check the error messages above for details.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)