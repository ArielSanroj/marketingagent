"""
Google Ads API Integration and Simulation Tools
Provides tools for creating, managing, and optimizing Google Ads campaigns
"""
import os
import json
from typing import List, Dict, Any, Optional
from dotenv import load_dotenv

# Try to import Google Ads API
try:
    from google.ads.googleads.client import GoogleAdsClient
    from google.ads.googleads.errors import GoogleAdsException
    GOOGLE_ADS_AVAILABLE = True
except ImportError:
    GOOGLE_ADS_AVAILABLE = False
    GoogleAdsClient = None
    GoogleAdsException = None

load_dotenv()

class GoogleAdsAPI:
    """Real Google Ads API integration"""
    
    def __init__(self):
        self.client = None
        self.customer_id = None
        self._initialize_client()
    
    def _initialize_client(self):
        """Initialize Google Ads client"""
        if not GOOGLE_ADS_AVAILABLE:
            print("⚠️  Google Ads API library not available")
            return False
        
        try:
            # Check for required credentials
            required_vars = [
                'GOOGLE_ADS_DEVELOPER_TOKEN',
                'GOOGLE_ADS_CLIENT_ID',
                'GOOGLE_ADS_CLIENT_SECRET',
                'GOOGLE_ADS_REFRESH_TOKEN',
                'GOOGLE_ADS_LOGIN_CUSTOMER_ID'
            ]
            
            missing_vars = [var for var in required_vars if not os.getenv(var)]
            if missing_vars:
                print(f"⚠️  Google Ads API credentials not fully configured. Missing: {missing_vars}")
                return False
            
            # Try to load from google-ads.yaml first
            try:
                self.client = GoogleAdsClient.load_from_storage()
                self.customer_id = os.getenv('GOOGLE_ADS_LOGIN_CUSTOMER_ID')
                print("✅ Google Ads API client initialized from google-ads.yaml")
                return True
            except Exception as yaml_error:
                print(f"⚠️  Failed to load from google-ads.yaml: {yaml_error}")
                
                # Fallback to environment variables
                try:
                    # Create client from environment variables using the correct constructor
                    self.client = GoogleAdsClient(
                        developer_token=os.getenv('GOOGLE_ADS_DEVELOPER_TOKEN'),
                        oauth2_client_id=os.getenv('GOOGLE_ADS_CLIENT_ID'),
                        oauth2_client_secret=os.getenv('GOOGLE_ADS_CLIENT_SECRET'),
                        oauth2_refresh_token=os.getenv('GOOGLE_ADS_REFRESH_TOKEN'),
                        login_customer_id=os.getenv('GOOGLE_ADS_LOGIN_CUSTOMER_ID'),
                        use_proto_plus=True
                    )
                    self.customer_id = os.getenv('GOOGLE_ADS_LOGIN_CUSTOMER_ID')
                    print("✅ Google Ads API client initialized from environment variables")
                    return True
                except Exception as env_error:
                    print(f"⚠️  Failed to initialize from environment variables: {env_error}")
                    raise env_error
            
        except Exception as e:
            print(f"⚠️  Google Ads API initialization failed: {e}")
            return False
    
    def create_campaign(self, campaign_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a real Google Ads campaign"""
        if not self.client:
            raise Exception("Google Ads API not initialized")
        
        try:
            # Services and enums
            campaign_service = self.client.get_service("CampaignService")
            advertising_channel_type_enum = self.client.enums.AdvertisingChannelTypeEnum
            campaign_status_enum = self.client.enums.CampaignStatusEnum

            # Create campaign operation using get_type
            campaign_operation = self.client.get_type("CampaignOperation")
            campaign_obj = campaign_operation.create

            # Set basic properties
            campaign_obj.name = campaign_data.get('name', 'Hotel Campaign')
            campaign_obj.advertising_channel_type = advertising_channel_type_enum.SEARCH
            campaign_obj.status = campaign_status_enum.PAUSED  # Start paused for review

            # Budget
            budget_id = self._create_campaign_budget(campaign_data)
            campaign_obj.campaign_budget = (
                f"customers/{self.customer_id}/campaignBudgets/{budget_id}"
            )

            # Optional: bidding strategy (keep minimal to avoid version field mismatches)
            # Target ROAS strategies can be configured post-creation if needed

            # Execute
            response = campaign_service.mutate_campaigns(
                customer_id=self.customer_id,
                operations=[campaign_operation],
            )
            
            campaign_resource_name = response.results[0].resource_name
            campaign_id = campaign_resource_name.split('/')[-1]
            
            return {
                'id': campaign_id,
                'name': campaign_data.get('name', 'Hotel Campaign'),
                'status': 'PAUSED',
                'budget': campaign_data.get('budget', 1000),
                'resource_name': campaign_resource_name,
                'created_at': '2024-01-01T00:00:00Z'
            }
            
        except GoogleAdsException as ex:
            print(f"Google Ads API error: {ex}")
            raise Exception(f"Failed to create campaign: {ex}")
        except Exception as e:
            print(f"Unexpected error creating campaign: {e}")
            raise Exception(f"Failed to create campaign: {e}")
    
    def _create_campaign_budget(self, campaign_data: Dict[str, Any]) -> str:
        """Create a campaign budget"""
        try:
            budget_service = self.client.get_service("CampaignBudgetService")
            budget_operation = self.client.get_type("CampaignBudgetOperation")
            budget_obj = budget_operation.create

            budget_obj.name = f"{campaign_data.get('name', 'Hotel Campaign')} Budget"
            budget_obj.amount_micros = int(campaign_data.get('budget', 1000) * 1_000_000)
            # Not explicitly shared by default
            if hasattr(budget_obj, 'explicitly_shared'):
                budget_obj.explicitly_shared = False
            
            response = budget_service.mutate_campaign_budgets(
                customer_id=self.customer_id,
                operations=[budget_operation],
            )

            budget_resource_name = response.results[0].resource_name
            return budget_resource_name.split('/')[-1]
            
        except Exception as e:
            print(f"Error creating campaign budget: {e}")
            raise Exception(f"Failed to create campaign budget: {e}")
    
    def create_ad_group(self, campaign_id: str, ad_group_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create an ad group within a campaign"""
        if not self.client:
            raise Exception("Google Ads API not initialized")
        
        try:
            from google.ads.googleads.v22.services.services import ad_group_service
            from google.ads.googleads.v22.resources.types import ad_group
            from google.ads.googleads.v22.enums.types import ad_group_status
            from google.ads.googleads.v22.common.types import types
            
            # Create ad group operation
            ad_group_operation = ad_group_service.AdGroupOperation()
            ad_group_operation.create = ad_group.AdGroup()
            
            # Set ad group properties
            ad_group_obj = ad_group_operation.create
            ad_group_obj.name = ad_group_data.get('name', 'Ad Group')
            ad_group_obj.status = ad_group_status.AdGroupStatus.ENABLED
            ad_group_obj.campaign = f"customers/{self.customer_id}/campaigns/{campaign_id}"
            ad_group_obj.cpc_bid_micros = int(ad_group_data.get('cpc_bid', 2.80) * 1_000_000)
            
            # Execute the operation
            ad_group_service_client = self.client.get_service("AdGroupService")
            response = ad_group_service_client.mutate_ad_groups(
                customer_id=self.customer_id,
                operations=[ad_group_operation]
            )
            
            ad_group_resource_name = response.results[0].resource_name
            ad_group_id = ad_group_resource_name.split('/')[-1]
            
            return {
                'id': ad_group_id,
                'campaign_id': campaign_id,
                'name': ad_group_data.get('name', 'Ad Group'),
                'status': 'ENABLED',
                'cpc_bid': ad_group_data.get('cpc_bid', 2.80),
                'resource_name': ad_group_resource_name,
                'created_at': '2024-01-01T00:00:00Z'
            }
            
        except GoogleAdsException as ex:
            print(f"Google Ads API error: {ex}")
            raise Exception(f"Failed to create ad group: {ex}")
        except Exception as e:
            print(f"Unexpected error creating ad group: {e}")
            raise Exception(f"Failed to create ad group: {e}")
    
    def create_responsive_search_ad(self, ad_group_id: str, ad_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a responsive search ad"""
        if not self.client:
            raise Exception("Google Ads API not initialized")
        
        try:
            from google.ads.googleads.v22.services.services import ad_group_ad_service
            from google.ads.googleads.v22.resources.types import ad_group_ad
            from google.ads.googleads.v22.resources.types import ad
            from google.ads.googleads.v22.common.types import types
            from google.ads.googleads.v22.enums.types import ad_group_ad_status
            from google.ads.googleads.v22.enums.types import ad_type
            from google.ads.googleads.v22.enums.types import asset_type
            
            # Create ad group ad operation
            ad_group_ad_operation = ad_group_ad_service.AdGroupAdOperation()
            ad_group_ad_operation.create = ad_group_ad.AdGroupAd()
            
            # Set ad group ad properties
            ad_group_ad_obj = ad_group_ad_operation.create
            ad_group_ad_obj.ad_group = f"customers/{self.customer_id}/adGroups/{ad_group_id}"
            ad_group_ad_obj.status = ad_group_ad_status.AdGroupAdStatus.ENABLED
            
            # Create responsive search ad
            responsive_search_ad = ad.Ad()
            responsive_search_ad.type_ = ad_type.AdType.RESPONSIVE_SEARCH_AD
            
            # Set final URLs
            final_urls = ad_data.get('final_urls', ['https://example.com'])
            responsive_search_ad.final_urls.extend(final_urls)
            
            # Create headlines
            headlines = ad_data.get('headlines', [])
            for headline_text in headlines[:3]:  # Max 3 headlines
                headline_asset = types.AdTextAsset()
                headline_asset.text = headline_text[:30]  # Max 30 chars
                headline_asset.pinned_field = types.ServedAssetFieldType.HEADLINE_1
                responsive_search_ad.headlines.append(headline_asset)
            
            # Create descriptions
            descriptions = ad_data.get('descriptions', [])
            for desc_text in descriptions[:2]:  # Max 2 descriptions
                description_asset = types.AdTextAsset()
                description_asset.text = desc_text[:90]  # Max 90 chars
                responsive_search_ad.descriptions.append(description_asset)
            
            ad_group_ad_obj.ad.CopyFrom(responsive_search_ad)
            
            # Execute the operation
            ad_group_ad_service_client = self.client.get_service("AdGroupAdService")
            response = ad_group_ad_service_client.mutate_ad_group_ads(
                customer_id=self.customer_id,
                operations=[ad_group_ad_operation]
            )
            
            ad_group_ad_resource_name = response.results[0].resource_name
            ad_id = ad_group_ad_resource_name.split('/')[-1]
            
            return {
                'id': ad_id,
                'ad_group_id': ad_group_id,
                'type': 'RESPONSIVE_SEARCH_AD',
                'headlines': headlines,
                'descriptions': descriptions,
                'final_urls': final_urls,
                'status': 'ENABLED',
                'resource_name': ad_group_ad_resource_name,
                'created_at': '2024-01-01T00:00:00Z'
            }
            
        except GoogleAdsException as ex:
            print(f"Google Ads API error: {ex}")
            raise Exception(f"Failed to create responsive search ad: {ex}")
        except Exception as e:
            print(f"Unexpected error creating responsive search ad: {e}")
            raise Exception(f"Failed to create responsive search ad: {e}")
    
    def add_keywords(self, ad_group_id: str, keywords: List[str], 
                    match_types: List[str] = None) -> Dict[str, Any]:
        """Add keywords to an ad group"""
        if not self.client:
            raise Exception("Google Ads API not initialized")
        
        try:
            from google.ads.googleads.v22.services.services import ad_group_criterion_service
            from google.ads.googleads.v22.resources.types import ad_group_criterion
            from google.ads.googleads.v22.common.types import types
            from google.ads.googleads.v22.enums.types import keyword_match_type
            from google.ads.googleads.v22.enums.types import criterion_type
            
            if match_types is None:
                match_types = ['EXACT'] * len(keywords)
            
            operations = []
            keyword_data = []
            
            for i, keyword in enumerate(keywords):
                # Create keyword criterion operation
                criterion_operation = ad_group_criterion_service.AdGroupCriterionOperation()
                criterion_operation.create = ad_group_criterion.AdGroupCriterion()
                
                # Set criterion properties
                criterion_obj = criterion_operation.create
                criterion_obj.ad_group = f"customers/{self.customer_id}/adGroups/{ad_group_id}"
                criterion_obj.status = types.AdGroupCriterionStatus.ENABLED
                
                # Create keyword info
                keyword_info = types.KeywordInfo()
                keyword_info.text = keyword
                
                # Set match type
                match_type_enum = keyword_match_type.KeywordMatchType.EXACT
                if i < len(match_types):
                    if match_types[i].upper() == 'PHRASE':
                        match_type_enum = keyword_match_type.KeywordMatchType.PHRASE
                    elif match_types[i].upper() == 'BROAD':
                        match_type_enum = keyword_match_type.KeywordMatchType.BROAD
                
                keyword_info.match_type = match_type_enum
                criterion_obj.keyword = keyword_info
                criterion_obj.type_ = criterion_type.CriterionType.KEYWORD
                
                operations.append(criterion_operation)
                
                keyword_data.append({
                    'keyword': keyword,
                    'match_type': match_types[i] if i < len(match_types) else 'EXACT',
                    'status': 'ENABLED',
                    'cpc_bid': 2.50
                })
            
            # Execute the operations
            criterion_service_client = self.client.get_service("AdGroupCriterionService")
            response = criterion_service_client.mutate_ad_group_criteria(
                customer_id=self.customer_id,
                operations=operations
            )
            
            return {'added_keywords': keyword_data}
            
        except GoogleAdsException as ex:
            print(f"Google Ads API error: {ex}")
            raise Exception(f"Failed to add keywords: {ex}")
        except Exception as e:
            print(f"Unexpected error adding keywords: {e}")
            raise Exception(f"Failed to add keywords: {e}")
    
    def get_performance_data(self, campaign_id: str, days: int = 30) -> Dict[str, Any]:
        """Get performance metrics for a campaign"""
        if not self.client:
            raise Exception("Google Ads API not initialized")
        
        try:
            from google.ads.googleads.v22.services.services import google_ads_service
            from google.ads.googleads.v22.enums.types import metrics
            from google.ads.googleads.v22.enums.types import segments
            from google.ads.googleads.v22.enums.types import resource_name
            from google.ads.googleads.v22.common.types import types
            from datetime import datetime, timedelta
            
            # Create query
            query = f"""
                SELECT
                    campaign.id,
                    campaign.name,
                    metrics.impressions,
                    metrics.clicks,
                    metrics.cost_micros,
                    metrics.conversions,
                    metrics.conversions_value,
                    metrics.ctr,
                    metrics.average_cpc,
                    metrics.conversion_rate,
                    metrics.value_per_conversion
                FROM campaign
                WHERE campaign.id = {campaign_id}
                AND segments.date BETWEEN '{datetime.now().strftime('%Y-%m-%d')}' AND '{(datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')}'
            """
            
            # Execute query
            ga_service = self.client.get_service("GoogleAdsService")
            response = ga_service.search(
                customer_id=self.customer_id,
                query=query
            )
            
            # Process results
            for row in response:
                cost = row.metrics.cost_micros / 1_000_000 if row.metrics.cost_micros else 0
                conversions_value = row.metrics.conversions_value if row.metrics.conversions_value else 0
                roas = conversions_value / cost if cost > 0 else 0
                
                return {
                    'campaign_id': str(row.campaign.id),
                    'campaign_name': row.campaign.name,
                    'date_range': f'Last {days} days',
                    'impressions': row.metrics.impressions,
                    'clicks': row.metrics.clicks,
                    'conversions': row.metrics.conversions,
                    'cost': cost,
                    'ctr': row.metrics.ctr,
                    'cpc': row.metrics.average_cpc,
                    'conversion_rate': row.metrics.conversion_rate,
                    'roas': roas,
                    'conversions_value': conversions_value
                }
            
            # Return default if no data found
            return {
                'campaign_id': campaign_id,
                'date_range': f'Last {days} days',
                'impressions': 0,
                'clicks': 0,
                'conversions': 0,
                'cost': 0.0,
                'ctr': 0.0,
                'cpc': 0.0,
                'conversion_rate': 0.0,
                'roas': 0.0,
                'conversions_value': 0.0
            }
            
        except GoogleAdsException as ex:
            print(f"Google Ads API error: {ex}")
            raise Exception(f"Failed to get performance data: {ex}")
        except Exception as e:
            print(f"Unexpected error getting performance data: {e}")
            raise Exception(f"Failed to get performance data: {e}")
    
    def get_campaign_performance(self, campaign_id: str) -> Dict[str, Any]:
        """Get real campaign performance data (alias for get_performance_data)"""
        return self.get_performance_data(campaign_id)
    
    def pause_campaign(self, campaign_id: str) -> bool:
        """Pause a campaign"""
        if not self.client:
            raise Exception("Google Ads API not initialized")
        
        try:
            from google.ads.googleads.v22.services.services import campaign_service
            from google.ads.googleads.v22.resources.types import campaign
            from google.ads.googleads.v22.enums.types import campaign_status
            from google.ads.googleads.v22.common import types
            
            # Create campaign operation
            campaign_operation = campaign_service.CampaignOperation()
            campaign_operation.update = campaign.Campaign()
            campaign_operation.update.resource_name = f"customers/{self.customer_id}/campaigns/{campaign_id}"
            campaign_operation.update.status = campaign_status.CampaignStatus.PAUSED
            campaign_operation.update_mask.CopyFrom(
                types.FieldMask(paths=["status"])
            )
            
            # Execute the operation
            campaign_service_client = self.client.get_service("CampaignService")
            response = campaign_service_client.mutate_campaigns(
                customer_id=self.customer_id,
                operations=[campaign_operation]
            )
            
            return True
            
        except GoogleAdsException as ex:
            print(f"Google Ads API error pausing campaign: {ex}")
            raise Exception(f"Failed to pause campaign: {ex}")
        except Exception as e:
            print(f"Unexpected error pausing campaign: {e}")
            raise Exception(f"Failed to pause campaign: {e}")
    
    def resume_campaign(self, campaign_id: str) -> bool:
        """Resume a campaign"""
        if not self.client:
            raise Exception("Google Ads API not initialized")
        
        try:
            from google.ads.googleads.v22.services.services import campaign_service
            from google.ads.googleads.v22.resources.types import campaign
            from google.ads.googleads.v22.enums.types import campaign_status
            from google.ads.googleads.v22.common import types
            
            # Create campaign operation
            campaign_operation = campaign_service.CampaignOperation()
            campaign_operation.update = campaign.Campaign()
            campaign_operation.update.resource_name = f"customers/{self.customer_id}/campaigns/{campaign_id}"
            campaign_operation.update.status = campaign_status.CampaignStatus.ENABLED
            campaign_operation.update_mask.CopyFrom(
                types.FieldMask(paths=["status"])
            )
            
            # Execute the operation
            campaign_service_client = self.client.get_service("CampaignService")
            response = campaign_service_client.mutate_campaigns(
                customer_id=self.customer_id,
                operations=[campaign_operation]
            )
            
            return True
            
        except GoogleAdsException as ex:
            print(f"Google Ads API error resuming campaign: {ex}")
            raise Exception(f"Failed to resume campaign: {ex}")
        except Exception as e:
            print(f"Unexpected error resuming campaign: {e}")
            raise Exception(f"Failed to resume campaign: {e}")
    
    def list_campaigns(self) -> List[Dict[str, Any]]:
        """List all campaigns for the customer"""
        if not self.client:
            raise Exception("Google Ads API not initialized")
        
        try:
            from google.ads.googleads.v22.services.services import google_ads_service
            from google.ads.googleads.v22.enums.types import resource_name
            
            # Create query
            query = """
                SELECT
                    campaign.id,
                    campaign.name,
                    campaign.status,
                    campaign_budget.amount_micros,
                    campaign.start_date,
                    campaign.end_date
                FROM campaign
                ORDER BY campaign.id
            """
            
            # Execute query
            ga_service = self.client.get_service("GoogleAdsService")
            response = ga_service.search(
                customer_id=self.customer_id,
                query=query
            )
            
            campaigns = []
            for row in response:
                campaigns.append({
                    'id': str(row.campaign.id),
                    'name': row.campaign.name,
                    'status': row.campaign.status.name,
                    'budget': row.campaign_budget.amount_micros / 1_000_000 if row.campaign_budget.amount_micros else 0,
                    'start_date': row.campaign.start_date,
                    'end_date': row.campaign.end_date
                })
            
            return campaigns
            
        except GoogleAdsException as ex:
            print(f"Google Ads API error listing campaigns: {ex}")
            raise Exception(f"Failed to list campaigns: {ex}")
        except Exception as e:
            print(f"Unexpected error listing campaigns: {e}")
            raise Exception(f"Failed to list campaigns: {e}")
    
    def optimize_bidding(self, campaign_id: str, target_roas: float = 400) -> Dict[str, Any]:
        """Optimize bidding strategy based on performance"""
        try:
            performance = self.get_performance_data(campaign_id)
            
            # Simple optimization logic
            current_roas = performance.get('roas', 0)
            optimization_suggestions = []
            
            if current_roas < target_roas / 100:
                optimization_suggestions.append("Increase bid adjustments for high-performing keywords")
                optimization_suggestions.append("Pause low-performing keywords")
                optimization_suggestions.append("Improve ad relevance and landing page experience")
            else:
                optimization_suggestions.append("Campaign performing well - consider increasing budget")
                optimization_suggestions.append("Expand to similar keywords")
            
            return {
                'campaign_id': campaign_id,
                'current_roas': current_roas,
                'target_roas': target_roas / 100,
                'optimization_suggestions': optimization_suggestions,
                'recommended_actions': [
                    "Review and update ad copy",
                    "Analyze search term reports",
                    "Adjust keyword bids based on performance"
                ]
            }
            
        except Exception as e:
            print(f"Error optimizing campaign: {e}")
            raise Exception(f"Failed to optimize campaign: {e}")


class GoogleAdsSimulator:
    """Simulates Google Ads API operations for development and testing"""
    
    def __init__(self):
        self.campaigns = {}
        self.ads = {}
        self.keywords = {}
        self.performance_data = {}
    
    def create_campaign(self, campaign_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new Google Ads campaign"""
        campaign_id = f"campaign_{len(self.campaigns) + 1}"
        
        campaign = {
            'id': campaign_id,
            'name': campaign_data.get('name', 'Eco-Lodge Bogotá Getaway'),
            'status': 'ACTIVE',
            'budget': campaign_data.get('budget', 1000),
            'bidding_strategy': campaign_data.get('bidding_strategy', 'TARGET_ROAS'),
            'target_roas': campaign_data.get('target_roas', 400),
            'target_locations': campaign_data.get('locations', ['Nilo, Cundinamarca', 'Bogotá, Colombia']),
            'target_languages': campaign_data.get('languages', ['Spanish']),
            'created_at': '2024-01-01T00:00:00Z'
        }
        
        self.campaigns[campaign_id] = campaign
        return campaign
    
    def create_ad_group(self, campaign_id: str, ad_group_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create an ad group within a campaign"""
        ad_group_id = f"adgroup_{len(self.ads) + 1}"
        
        ad_group = {
            'id': ad_group_id,
            'campaign_id': campaign_id,
            'name': ad_group_data.get('name', 'Eco-Lodge Bogotá Getaway'),
            'status': 'ACTIVE',
            'cpc_bid': ad_group_data.get('cpc_bid', 2.80),
            'keywords': ad_group_data.get('keywords', []),
            'created_at': '2024-01-01T00:00:00Z'
        }
        
        self.ads[ad_group_id] = ad_group
        return ad_group
    
    def create_responsive_search_ad(self, ad_group_id: str, ad_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a responsive search ad"""
        ad_id = f"ad_{len(self.ads) + 1}"
        
        # Validate headlines (max 3, 30 chars each)
        headlines = ad_data.get('headlines', [])
        if len(headlines) > 3:
            headlines = headlines[:3]
        
        # Validate descriptions (max 2, 90 chars each)
        descriptions = ad_data.get('descriptions', [])
        if len(descriptions) > 2:
            descriptions = descriptions[:2]
        
        ad = {
            'id': ad_id,
            'ad_group_id': ad_group_id,
            'type': 'RESPONSIVE_SEARCH_AD',
            'headlines': headlines,
            'descriptions': descriptions,
            'final_urls': ad_data.get('final_urls', ['https://eco-lodge-nilo.com']),
            'status': 'ACTIVE',
            'created_at': '2024-01-01T00:00:00Z'
        }
        
        self.ads[ad_id] = ad
        return ad
    
    def add_keywords(self, ad_group_id: str, keywords: List[str], 
                    match_types: List[str] = None) -> Dict[str, Any]:
        """Add keywords to an ad group"""
        if match_types is None:
            match_types = ['EXACT'] * len(keywords)
        
        keyword_data = []
        for i, keyword in enumerate(keywords):
            keyword_info = {
                'keyword': keyword,
                'match_type': match_types[i] if i < len(match_types) else 'EXACT',
                'status': 'ACTIVE',
                'cpc_bid': 2.50
            }
            keyword_data.append(keyword_info)
        
        if ad_group_id in self.ads:
            self.ads[ad_group_id]['keywords'].extend(keyword_data)
        
        return {'added_keywords': keyword_data}
    
    def get_performance_data(self, campaign_id: str, days: int = 30) -> Dict[str, Any]:
        """Get performance metrics for a campaign"""
        # Simulate performance data
        performance = {
            'campaign_id': campaign_id,
            'date_range': f'Last {days} days',
            'impressions': 50000 + (hash(campaign_id) % 10000),
            'clicks': 1500 + (hash(campaign_id) % 500),
            'conversions': 45 + (hash(campaign_id) % 20),
            'cost': 3750.50 + (hash(campaign_id) % 1000),
            'ctr': 3.2 + (hash(campaign_id) % 100) / 1000,
            'cpc': 2.50 + (hash(campaign_id) % 100) / 100,
            'conversion_rate': 3.0 + (hash(campaign_id) % 100) / 100,
            'roas': 4.2 + (hash(campaign_id) % 100) / 100,
            'quality_score': 7.5 + (hash(campaign_id) % 25) / 10
        }
        
        self.performance_data[campaign_id] = performance
        return performance
    
    def optimize_bidding(self, campaign_id: str, target_roas: float = 400) -> Dict[str, Any]:
        """Optimize bidding strategy based on performance"""
        performance = self.get_performance_data(campaign_id)
        
        # Simple optimization logic
        current_roas = performance['roas']
        optimization_suggestions = []
        
        if current_roas < target_roas / 100:
            optimization_suggestions.append("Increase bid adjustments for high-performing keywords")
            optimization_suggestions.append("Pause low-performing keywords")
            optimization_suggestions.append("Improve ad relevance and landing page experience")
        else:
            optimization_suggestions.append("Campaign performing well - consider increasing budget")
            optimization_suggestions.append("Expand to similar keywords")
        
        return {
            'campaign_id': campaign_id,
            'current_roas': current_roas,
            'target_roas': target_roas / 100,
            'optimization_suggestions': optimization_suggestions,
            'recommended_actions': [
                "Review and update ad copy",
                "Analyze search term reports",
                "Adjust keyword bids based on performance"
            ]
        }

# Global instances
google_ads_simulator = GoogleAdsSimulator()
google_ads_api = GoogleAdsAPI()

def get_google_ads_client():
    """Get the appropriate Google Ads client (real API or simulator)"""
    use_simulators = os.getenv('USE_SIMULATORS', 'false').lower() == 'true'
    
    if use_simulators or not google_ads_api.client:
        print("🔧 Using Google Ads simulator")
        return google_ads_simulator
    else:
        print("🔧 Using real Google Ads API")
        return google_ads_api

def create_google_ad(keywords: List[str], headlines: List[str], descriptions: List[str], 
                    bidding_strategy: str = 'TARGET_ROAS', roas: float = 400) -> str:
    """Create a Google Ads campaign with the provided parameters"""
    try:
        client = get_google_ads_client()
        
        # Create campaign
        campaign_data = {
            'name': 'Eco-Lodge Bogotá Getaway',
            'budget': 1000,
            'bidding_strategy': bidding_strategy,
            'target_roas': roas,
            'locations': ['Nilo, Cundinamarca', 'Bogotá, Colombia']
        }
        
        campaign = client.create_campaign(campaign_data)
        
        # Create ad group
        ad_group_data = {
            'name': 'Bogotá Weekend Nature Escape',
            'keywords': keywords,
            'cpc_bid': 2.80
        }
        
        ad_group = client.create_ad_group(campaign['id'], ad_group_data)
        
        # Create responsive search ad
        ad_data = {
            'headlines': headlines,
            'descriptions': descriptions,
            'final_urls': ['https://eco-lodge-nilo.com']
        }
        
        ad = client.create_responsive_search_ad(ad_group['id'], ad_data)
        
        # Add keywords
        client.add_keywords(ad_group['id'], keywords)
        
        return f"Successfully created Google Ads campaign: {campaign['id']} with ad group: {ad_group['id']} and ad: {ad['id']}"
        
    except Exception as e:
        return f"Error creating Google Ad: {str(e)}"

def get_ad_performance(campaign_id: str) -> str:
    """Get performance data for a campaign"""
    try:
        client = get_google_ads_client()
        # Use the correct method name based on client type
        if hasattr(client, 'get_performance_data'):
            performance = client.get_performance_data(campaign_id)
        else:
            performance = client.get_campaign_performance(campaign_id)
        return f"Campaign {campaign_id} performance: {json.dumps(performance, indent=2)}"
    except Exception as e:
        return f"Error getting performance data: {str(e)}"

def optimize_campaign(campaign_id: str, target_roas: float = 400) -> str:
    """Optimize a campaign's bidding strategy"""
    try:
        optimization = google_ads_simulator.optimize_bidding(campaign_id, target_roas)
        return json.dumps(optimization, indent=2)
    except Exception as e:
        return f"Error optimizing campaign: {str(e)}"