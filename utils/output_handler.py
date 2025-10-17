"""
Output File Handler
Handles creation and management of output files for the hotel sales system
"""
import os
import json
from datetime import datetime
from typing import Dict, Any, Optional
from dotenv import load_dotenv

load_dotenv()

class OutputHandler:
    """Handles output file creation and management"""
    
    def __init__(self):
        self.output_dir = os.getenv('OUTPUT_DIR', 'outputs')
        self.logs_dir = os.getenv('LOGS_DIR', 'logs')
        self._ensure_directories()
    
    def _ensure_directories(self):
        """Ensure output and logs directories exist"""
        os.makedirs(self.output_dir, exist_ok=True)
        os.makedirs(self.logs_dir, exist_ok=True)
    
    def save_markdown_report(self, filename: str, content: str, metadata: Optional[Dict[str, Any]] = None) -> str:
        """Save a markdown report to the outputs directory"""
        filepath = os.path.join(self.output_dir, filename)
        
        # Add metadata header if provided
        if metadata:
            header = self._create_markdown_header(metadata)
            content = f"{header}\n\n{content}"
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ Report saved: {filepath}")
            return filepath
        except Exception as e:
            print(f"❌ Error saving report {filename}: {e}")
            return ""
    
    def save_json_data(self, filename: str, data: Dict[str, Any]) -> str:
        """Save JSON data to the outputs directory"""
        filepath = os.path.join(self.output_dir, filename)
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            print(f"✅ JSON data saved: {filepath}")
            return filepath
        except Exception as e:
            print(f"❌ Error saving JSON {filename}: {e}")
            return ""
    
    def save_workflow_log(self, workflow_data: Dict[str, Any]) -> str:
        """Save workflow execution log"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"workflow_log_{timestamp}.json"
        filepath = os.path.join(self.logs_dir, filename)
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(workflow_data, f, indent=2, ensure_ascii=False)
            print(f"✅ Workflow log saved: {filepath}")
            return filepath
        except Exception as e:
            print(f"❌ Error saving workflow log: {e}")
            return ""
    
    def _create_markdown_header(self, metadata: Dict[str, Any]) -> str:
        """Create a markdown header with metadata"""
        header = "---\n"
        header += f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        
        for key, value in metadata.items():
            header += f"{key}: {value}\n"
        
        header += "---\n"
        return header
    
    def create_market_research_report(self, research_data: Dict[str, Any]) -> str:
        """Create a formatted market research report"""
        content = f"""# Market Research Report - Nilo Eco-Lodge

## Executive Summary
{research_data.get('summary', 'No summary provided')}

## Bogotá Weekend Travel Trends
{research_data.get('trends', 'No trends data available')}

## Competitive Landscape in Nilo & Surroundings
{research_data.get('competitors', 'No competitor data available')}

## Priority Guest Segments
{research_data.get('guest_segments', 'No guest segment data available')}

## Keyword Recommendations (ES & EN)
{research_data.get('keywords', 'No keyword recommendations available')}

## Seasonal Opportunities (Dry vs Rainy Season)
{research_data.get('seasonal', 'No seasonal analysis available')}

## Strategic Recommendations
{research_data.get('recommendations', 'No recommendations provided')}
"""
        
        metadata = {
            'report_type': 'market_research',
            'agent': 'researcher',
            'timestamp': datetime.now().isoformat()
        }
        
        return self.save_markdown_report('market_research_report.md', content, metadata)
    
    def create_google_ads_campaign_report(self, campaign_data: Dict[str, Any]) -> str:
        """Create a formatted Google Ads campaign report"""
        content = f"""# Google Ads Campaign Report - Bogotá to Nilo

## Campaign Overview
**Campaign Name:** {campaign_data.get('name', 'Eco-Lodge Bogotá Getaway')}
**Budget:** ${campaign_data.get('budget', 1000)}
**Bidding Strategy:** {campaign_data.get('bidding_strategy', 'TARGET_ROAS')}
**Target ROAS:** {campaign_data.get('target_roas', 400)}%

## Ad Group Structure
{campaign_data.get('ad_groups', 'No ad groups defined')}

## Responsive Search Ad Assets
{campaign_data.get('headlines', 'No headlines provided')}

## Ad Descriptions (ES)
{campaign_data.get('descriptions', 'No descriptions provided')}

## Keyword Themes
{campaign_data.get('keywords', 'No keywords provided')}

## Targeting Strategy
{campaign_data.get('targeting', 'No targeting information available')}

## Recommended Extensions
{campaign_data.get('extensions', 'No ad extensions defined')}

## Launch Checklist & Next Steps
{campaign_data.get('next_steps', 'No next steps provided')}
"""
        
        metadata = {
            'report_type': 'google_ads_campaign',
            'agent': 'ad_generator',
            'timestamp': datetime.now().isoformat()
        }
        
        return self.save_markdown_report('google_ads_campaign.md', content, metadata)
    
    def create_optimization_report(self, optimization_data: Dict[str, Any]) -> str:
        """Create a formatted optimization report"""
        content = f"""# Performance Optimization Report - Nilo Campaign

## Current Performance Snapshot
{optimization_data.get('current_performance', 'No performance data available')}

## Key Opportunities (Bogotá Weekend Travelers)
{optimization_data.get('opportunities', 'No optimization opportunities identified')}

## Keyword & Search Term Actions
{optimization_data.get('keyword_adjustments', 'No keyword adjustments recommended')}

## Creative Testing Roadmap
{optimization_data.get('ad_copy_testing', 'No ad copy testing recommendations')}

## Bidding & Budget Adjustments
{optimization_data.get('bidding_improvements', 'No bidding improvements recommended')}

## Allocation & Scaling Plan
{optimization_data.get('budget_reallocation', 'No budget reallocation recommended')}

## Quality Score + Landing Page Insights
{optimization_data.get('quality_score_improvements', 'No quality score improvements recommended')}

## Expected Impact & Timeline
{optimization_data.get('expected_results', 'No expected results provided')}

## Implementation Timeline
{optimization_data.get('implementation_timeline', 'No timeline provided')}
"""
        
        metadata = {
            'report_type': 'optimization',
            'agent': 'optimizer',
            'timestamp': datetime.now().isoformat()
        }
        
        return self.save_markdown_report('optimization_report.md', content, metadata)

# Global output handler instance
output_handler = OutputHandler()