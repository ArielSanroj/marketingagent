"""
Ad Generator Agent
Creates compelling Google Ads campaigns and ad copy
"""
from utils.memory import memory
from utils.google_ads import create_google_ad, get_ad_performance
from utils.crewai_compat import create_agent

# No stub agent - only use factory function

def create_ad_generator_agent(llm):
    """Create ad generator agent with LLM"""
    try:
        from crewai import Agent
        agent = Agent(
            role='Google Ads Creative Specialist',
            goal='Create compelling, high-converting Google Ads campaigns and ad copy for hotel marketing',
            backstory="""You are a creative Google Ads specialist with 10 years of experience in hospitality marketing. 
            You have a proven track record of creating ad campaigns that achieve 4x+ ROAS for luxury hotels. 
            Your expertise includes crafting compelling headlines, persuasive descriptions, and selecting high-intent keywords. 
            You understand the psychology of luxury travelers and know how to create urgency and desire through ad copy. 
            You're skilled at A/B testing and optimizing campaigns for maximum performance.""",
            memory=True,
            verbose=True,
            allow_delegation=False,
            max_iter=3,
            max_execution_time=300,
            llm=llm
        )
        print("✅ Created real ad generator agent with LLM")
        return agent
    except Exception as e:
        print(f"⚠️  Failed to create ad generator agent: {e}")
        print("   Falling back to stub agent")
        # Create stub agent as fallback
        from utils.crewai_compat import create_agent
        return create_agent(
            role='Google Ads Creative Specialist',
            goal='Create compelling, high-converting Google Ads campaigns and ad copy for hotel marketing',
            backstory="""You are a creative Google Ads specialist with 10 years of experience in hospitality marketing. 
            You have a proven track record of creating ad campaigns that achieve 4x+ ROAS for luxury hotels. 
            Your expertise includes crafting compelling headlines, persuasive descriptions, and selecting high-intent keywords. 
            You understand the psychology of luxury travelers and know how to create urgency and desire through ad copy. 
            You're skilled at A/B testing and optimizing campaigns for maximum performance.""",
            tools=[create_google_ad, get_ad_performance],
            memory=True,
            verbose=True,
            allow_delegation=False,
            max_iter=3,
            max_execution_time=300
        )

def generate_ad_campaign(market_insights: str) -> str:
    """Generate Google Ads campaign based on market insights"""
    # Extract insights and create campaign
    keywords = [
        'eco lodge nilo colombia',
        'hotel campestre nilo',
        'escapada cerca de bogotá naturaleza',
        'plan fin de semana nilo cundinamarca',
        'hospedaje ecoturismo cundinamarca'
    ]
    
    headlines = [
        'Eco-Lodge en Nilo',
        'Escapada Cerca de Bogotá',
        'Reserva Directo y Ahorra'
    ]
    
    descriptions = [
        'Disfruta naturaleza y clima cálido a solo 90 minutos de Bogotá.',
        'Reserva tu plan de fin de semana ecológico y vive experiencias únicas.'
    ]
    
    # Create the ad campaign
    result = create_google_ad(keywords, headlines, descriptions)
    
    # Save campaign data to memory
    campaign_data = {
        'keywords': keywords,
        'headlines': headlines,
        'descriptions': descriptions,
        'target_audience': 'Luxury travelers, family gatherings',
        'bidding_strategy': 'TARGET_ROAS',
        'target_roas': 400
    }
    
    memory.save_to_memory(f"Generated ad campaign: {result}", {
        'type': 'ad_campaign',
        'campaign_data': campaign_data
    })
    
    return f"Ad campaign generated successfully: {result}"