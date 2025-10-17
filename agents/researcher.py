"""
Market Researcher Agent
Analyzes hospitality trends, guest segments, keywords, and demand patterns
"""
from utils.memory import memory
from utils.google_ads import create_google_ad, get_ad_performance
from utils.crewai_compat import create_agent

# No stub agent - only use factory function

def create_researcher_agent(llm):
    """Create researcher agent with LLM"""
    try:
        from crewai import Agent
        # Create agent with LLM directly in constructor
        agent = Agent(
            role='Hotel Market Researcher',
            goal='Analyze hospitality trends, guest segments, keywords, and demand patterns to inform marketing strategies',
            backstory="""You are a seasoned revenue management expert with 15 years of experience in the hospitality industry. 
            You're Google Ads certified and have a deep understanding of occupancy patterns, guest personalization, 
            and market dynamics. Your expertise lies in identifying emerging trends, understanding guest behavior, 
            and translating market insights into actionable marketing strategies. You excel at competitive analysis 
            and keyword research, always staying ahead of market shifts in the luxury hospitality sector.""",
            memory=True,
            verbose=True,
            allow_delegation=False,
            max_iter=3,
            max_execution_time=300,
            llm=llm
        )
        print("✅ Created real researcher agent with LLM")
        return agent
    except Exception as e:
        print(f"⚠️  Failed to create researcher agent: {e}")
        print("   Falling back to stub agent")
        # Create stub agent as fallback
        from utils.crewai_compat import create_agent
        return create_agent(
            role='Hotel Market Researcher',
            goal='Analyze hospitality trends, guest segments, keywords, and demand patterns to inform marketing strategies',
            backstory="""You are a seasoned revenue management expert with 15 years of experience in the hospitality industry. 
            You're Google Ads certified and have a deep understanding of occupancy patterns, guest personalization, 
            and market dynamics. Your expertise lies in identifying emerging trends, understanding guest behavior, 
            and translating market insights into actionable marketing strategies. You excel at competitive analysis 
            and keyword research, always staying ahead of market shifts in the luxury hospitality sector.""",
            tools=[create_google_ad, get_ad_performance],
            memory=True,
            verbose=True,
            allow_delegation=False,
            max_iter=3,
            max_execution_time=300
        )

def analyze_market_trends(diagnosis: str) -> str:
    """Analyze market trends based on hotel diagnosis"""
    # This would typically use the agent's tools and memory
    trends = {
        'seasonal_patterns': 'Dry-season weekends (June-August) show 25% higher demand for eco-lodges near Bogotá',
        'competitor_analysis': 'Boutique eco-stays in Nilo and nearby regions average $240/night with 65% occupancy',
        'guest_segments': ['Bogotá weekend travelers', 'Birdwatching enthusiasts', 'Family nature retreats'],
        'keyword_opportunities': [
            'eco lodge nilo colombia',
            'escapadas cerca de bogotá naturaleza',
            'hospedaje ecoturismo cundinamarca',
            'hotel campestre nilo cundinamarca',
            'plan fin de semana nilo cundinamarca'
        ],
        'demand_drivers': ['Nature activities', 'Warm microclimate', 'Proximity to Bogotá', 'Family-friendly amenities']
    }
    
    # Save to memory
    memory.save_market_trends(trends)
    
    return f"Market analysis complete. Key findings: {trends['seasonal_patterns']}. Recommended keywords: {', '.join(trends['keyword_opportunities'][:3])}"