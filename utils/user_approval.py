"""
User Approval Interface
Handles user review and approval of marketing strategies
"""
import json
import os
from typing import Dict, List, Any, Optional
from datetime import datetime
from dataclasses import dataclass, asdict

@dataclass
class MarketingStrategy:
    """Marketing strategy data structure"""
    hotel_name: str
    target_audience: List[str]
    key_selling_points: List[str]
    competitive_advantages: List[str]
    marketing_opportunities: List[str]
    content_suggestions: List[str]
    budget_recommendation: Dict[str, Any]
    timeline: Dict[str, Any]
    kpis: List[str]
    status: str = "pending"  # pending, approved, modified, rejected
    user_notes: str = ""
    modifications: List[str] = None
    
    def __post_init__(self):
        if self.modifications is None:
            self.modifications = []

class UserApprovalInterface:
    """Handles user approval workflow for marketing strategies"""
    
    def __init__(self):
        self.approvals_dir = "outputs/approvals"
        self.strategies_dir = "outputs/strategies"
        os.makedirs(self.approvals_dir, exist_ok=True)
        os.makedirs(self.strategies_dir, exist_ok=True)
    
    def create_strategy_from_analysis(self, hotel_analysis: Dict[str, Any], 
                                    instagram_analysis: Optional[Dict[str, Any]] = None) -> MarketingStrategy:
        """Create marketing strategy from hotel analysis"""
        
        # Extract hotel information
        hotel_name = hotel_analysis.get('hotel_name', 'Unknown Hotel')
        insights = hotel_analysis.get('marketing_insights', {})
        
        # Build strategy components
        target_audience = insights.get('target_audience', ['General travelers'])
        key_selling_points = insights.get('key_selling_points', ['Quality service'])
        competitive_advantages = insights.get('competitive_advantages', [])
        marketing_opportunities = insights.get('marketing_opportunities', [])
        content_suggestions = insights.get('content_suggestions', [])
        
        # Add Instagram insights if available
        if instagram_analysis and instagram_analysis.get('analysis_status') == 'success':
            instagram_insights = instagram_analysis.get('marketing_insights', {})
            if instagram_insights.get('content_gaps'):
                content_suggestions.extend(instagram_insights['content_gaps'])
            if instagram_insights.get('visual_quality') == 'High':
                competitive_advantages.append('Strong visual content')
        
        # Generate budget recommendation
        price_range = hotel_analysis.get('price_range', {})
        avg_price = price_range.get('average', 200) if price_range else 200
        
        budget_recommendation = self._generate_budget_recommendation(avg_price, hotel_name)
        
        # Generate timeline
        timeline = self._generate_timeline()
        
        # Generate KPIs
        kpis = self._generate_kpis()
        
        return MarketingStrategy(
            hotel_name=hotel_name,
            target_audience=target_audience,
            key_selling_points=key_selling_points,
            competitive_advantages=competitive_advantages,
            marketing_opportunities=marketing_opportunities,
            content_suggestions=content_suggestions,
            budget_recommendation=budget_recommendation,
            timeline=timeline,
            kpis=kpis
        )
    
    def _generate_budget_recommendation(self, avg_price: float, hotel_name: str) -> Dict[str, Any]:
        """Generate budget recommendation based on hotel analysis"""
        # Budget as percentage of average room rate
        if avg_price > 300:
            budget_percentage = 0.15  # 15% for luxury hotels
            budget_tier = "Premium"
        elif avg_price > 150:
            budget_percentage = 0.12  # 12% for mid-range hotels
            budget_tier = "Standard"
        else:
            budget_percentage = 0.10  # 10% for budget hotels
            budget_tier = "Budget"
        
        monthly_budget = avg_price * budget_percentage * 30  # 30 days
        
        return {
            "tier": budget_tier,
            "monthly_budget": round(monthly_budget, 2),
            "daily_budget": round(monthly_budget / 30, 2),
            "percentage_of_room_rate": round(budget_percentage * 100, 1),
            "allocation": {
                "google_ads": round(monthly_budget * 0.6, 2),
                "social_media": round(monthly_budget * 0.25, 2),
                "content_creation": round(monthly_budget * 0.15, 2)
            }
        }
    
    def _generate_timeline(self) -> Dict[str, Any]:
        """Generate implementation timeline"""
        return {
            "phase_1": {
                "name": "Setup & Launch",
                "duration": "Week 1-2",
                "tasks": [
                    "Google Ads account setup",
                    "Campaign creation",
                    "Landing page optimization",
                    "Tracking implementation"
                ]
            },
            "phase_2": {
                "name": "Optimization",
                "duration": "Week 3-4",
                "tasks": [
                    "Performance analysis",
                    "Bid optimization",
                    "Ad copy testing",
                    "Keyword refinement"
                ]
            },
            "phase_3": {
                "name": "Scale & Expand",
                "duration": "Month 2+",
                "tasks": [
                    "Budget scaling",
                    "New campaign types",
                    "Advanced targeting",
                    "Conversion optimization"
                ]
            }
        }
    
    def _generate_kpis(self) -> List[str]:
        """Generate key performance indicators"""
        return [
            "Click-through rate (CTR)",
            "Cost per click (CPC)",
            "Conversion rate",
            "Return on ad spend (ROAS)",
            "Cost per acquisition (CPA)",
            "Booking rate",
            "Revenue per visitor",
            "Quality score"
        ]
    
    def display_strategy_for_approval(self, strategy: MarketingStrategy) -> str:
        """Display strategy in a user-friendly format for approval"""
        output = []
        output.append("🏨 MARKETING STRATEGY FOR APPROVAL")
        output.append("=" * 50)
        output.append(f"Hotel: {strategy.hotel_name}")
        output.append(f"Status: {strategy.status.upper()}")
        output.append("")
        
        # Target Audience
        output.append("🎯 TARGET AUDIENCE:")
        output.append("-" * 20)
        for audience in strategy.target_audience:
            output.append(f"• {audience}")
        output.append("")
        
        # Key Selling Points
        output.append("⭐ KEY SELLING POINTS:")
        output.append("-" * 25)
        for point in strategy.key_selling_points:
            output.append(f"• {point}")
        output.append("")
        
        # Competitive Advantages
        if strategy.competitive_advantages:
            output.append("🚀 COMPETITIVE ADVANTAGES:")
            output.append("-" * 28)
            for advantage in strategy.competitive_advantages:
                output.append(f"• {advantage}")
            output.append("")
        
        # Marketing Opportunities
        if strategy.marketing_opportunities:
            output.append("💡 MARKETING OPPORTUNITIES:")
            output.append("-" * 30)
            for opportunity in strategy.marketing_opportunities:
                output.append(f"• {opportunity}")
            output.append("")
        
        # Content Suggestions
        if strategy.content_suggestions:
            output.append("📝 CONTENT SUGGESTIONS:")
            output.append("-" * 25)
            for suggestion in strategy.content_suggestions:
                output.append(f"• {suggestion}")
            output.append("")
        
        # Budget Recommendation
        output.append("💰 BUDGET RECOMMENDATION:")
        output.append("-" * 25)
        budget = strategy.budget_recommendation
        output.append(f"Tier: {budget['tier']}")
        output.append(f"Monthly Budget: ${budget['monthly_budget']:,.2f}")
        output.append(f"Daily Budget: ${budget['daily_budget']:,.2f}")
        output.append("")
        output.append("Allocation:")
        for channel, amount in budget['allocation'].items():
            output.append(f"  • {channel.replace('_', ' ').title()}: ${amount:,.2f}")
        output.append("")
        
        # Timeline
        output.append("📅 IMPLEMENTATION TIMELINE:")
        output.append("-" * 30)
        for phase_key, phase in strategy.timeline.items():
            output.append(f"{phase['name']} ({phase['duration']}):")
            for task in phase['tasks']:
                output.append(f"  • {task}")
            output.append("")
        
        # KPIs
        output.append("📊 KEY PERFORMANCE INDICATORS:")
        output.append("-" * 35)
        for kpi in strategy.kpis:
            output.append(f"• {kpi}")
        output.append("")
        
        # User Notes
        if strategy.user_notes:
            output.append("📝 USER NOTES:")
            output.append("-" * 15)
            output.append(strategy.user_notes)
            output.append("")
        
        # Modifications
        if strategy.modifications:
            output.append("✏️ MODIFICATIONS:")
            output.append("-" * 18)
            for modification in strategy.modifications:
                output.append(f"• {modification}")
            output.append("")
        
        return "\n".join(output)
    
    def save_strategy(self, strategy: MarketingStrategy, filename: Optional[str] = None) -> str:
        """Save strategy to file"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"strategy_{strategy.hotel_name.replace(' ', '_')}_{timestamp}.json"
        
        filepath = os.path.join(self.strategies_dir, filename)
        
        strategy_data = asdict(strategy)
        strategy_data['created_at'] = datetime.now().isoformat()
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(strategy_data, f, indent=2, ensure_ascii=False)
        
        return filepath
    
    def load_strategy(self, filepath: str) -> MarketingStrategy:
        """Load strategy from file"""
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Remove created_at if present
        data.pop('created_at', None)
        
        return MarketingStrategy(**data)
    
    def approve_strategy(self, strategy: MarketingStrategy, user_notes: str = "") -> MarketingStrategy:
        """Approve a strategy"""
        strategy.status = "approved"
        strategy.user_notes = user_notes
        return strategy
    
    def modify_strategy(self, strategy: MarketingStrategy, modifications: List[str], 
                       user_notes: str = "") -> MarketingStrategy:
        """Modify a strategy based on user feedback"""
        strategy.status = "modified"
        strategy.modifications.extend(modifications)
        strategy.user_notes = user_notes
        return strategy
    
    def reject_strategy(self, strategy: MarketingStrategy, reason: str) -> MarketingStrategy:
        """Reject a strategy"""
        strategy.status = "rejected"
        strategy.user_notes = reason
        return strategy

def create_strategy_from_analysis(hotel_analysis: Dict[str, Any], 
                                instagram_analysis: Optional[Dict[str, Any]] = None) -> MarketingStrategy:
    """Convenience function to create strategy from analysis"""
    interface = UserApprovalInterface()
    return interface.create_strategy_from_analysis(hotel_analysis, instagram_analysis)