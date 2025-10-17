"""
Performance Optimizer Agent
Optimizes ad campaigns based on performance data and market feedback
"""
from utils.memory import memory
from utils.google_ads import create_google_ad, get_ad_performance, optimize_campaign
from utils.crewai_compat import create_agent

# No stub agent - only use factory function

def create_optimizer_agent(llm):
    """Create optimizer agent with LLM"""
    try:
        from crewai import Agent
        agent = Agent(
            role='Digital Marketing Performance Optimizer',
            goal='Optimize Google Ads campaigns for maximum ROAS, CTR, and conversion rates',
            backstory="""You are a data-driven marketing optimization expert with 12 years of experience in digital advertising. 
            You specialize in analyzing campaign performance, identifying optimization opportunities, and implementing 
            data-backed improvements. Your expertise includes bid management, keyword optimization, ad copy testing, 
            and landing page optimization. You have a track record of improving campaign ROAS by 50%+ through 
            systematic testing and optimization. You excel at interpreting complex performance data and translating 
            insights into actionable optimization strategies.""",
            memory=True,
            verbose=True,
            allow_delegation=False,
            max_iter=3,
            max_execution_time=300,
            llm=llm
        )
        print("✅ Created real optimizer agent with LLM")
        return agent
    except Exception as e:
        print(f"⚠️  Failed to create optimizer agent: {e}")
        print("   Falling back to stub agent")
        # Create stub agent as fallback
        from utils.crewai_compat import create_agent
        return create_agent(
            role='Digital Marketing Performance Optimizer',
            goal='Optimize Google Ads campaigns for maximum ROAS, CTR, and conversion rates',
            backstory="""You are a data-driven marketing optimization expert with 12 years of experience in digital advertising. 
            You specialize in analyzing campaign performance, identifying optimization opportunities, and implementing 
            data-backed improvements. Your expertise includes bid management, keyword optimization, ad copy testing, 
            and landing page optimization. You have a track record of improving campaign ROAS by 50%+ through 
            systematic testing and optimization. You excel at interpreting complex performance data and translating 
            insights into actionable optimization strategies.""",
            tools=[create_google_ad, get_ad_performance, optimize_campaign],
            memory=True,
            verbose=True,
            allow_delegation=False,
            max_iter=3,
            max_execution_time=300
        )

def optimize_ad_performance(campaign_id: str, performance_data: dict) -> str:
    """Optimize ad campaign based on performance data"""
    try:
        # Analyze performance metrics
        current_roas = performance_data.get('roas', 0)
        current_ctr = performance_data.get('ctr', 0)
        current_cpc = performance_data.get('cpc', 0)
        
        # Generate optimization recommendations
        optimizations = []
        
        if current_roas < 4.0:
            optimizations.append("Increase bid adjustments for high-converting keywords")
            optimizations.append("Pause low-performing keywords with high CPC")
            optimizations.append("Improve ad relevance scores")
        
        if current_ctr < 3.0:
            optimizations.append("Test new ad headlines and descriptions")
            optimizations.append("Improve keyword match types")
            optimizations.append("Enhance ad extensions")
        
        if current_cpc > 3.0:
            optimizations.append("Lower bids for low-converting keywords")
            optimizations.append("Focus on long-tail keywords")
            optimizations.append("Improve Quality Score through better ad relevance")
        
        # Get optimization suggestions from Google Ads tool
        optimization_result = optimize_campaign(campaign_id, 400)
        
        # Save optimization data to memory
        optimization_data = {
            'campaign_id': campaign_id,
            'current_metrics': performance_data,
            'optimizations': optimizations,
            'optimization_result': optimization_result
        }
        
        memory.save_to_memory(f"Optimization completed for campaign {campaign_id}", {
            'type': 'optimization',
            'optimization_data': optimization_data
        })
        
        return f"Optimization complete. Key recommendations: {'; '.join(optimizations[:3])}"
        
    except Exception as e:
        return f"Error optimizing campaign: {str(e)}"