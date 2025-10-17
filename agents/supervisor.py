"""
Supervisor Agent
Coordinates the team and ensures quality control across all marketing activities
"""
from utils.memory import memory
from utils.google_ads import create_google_ad, get_ad_performance, optimize_campaign
from utils.crewai_compat import create_agent

# No stub agent - only use factory function

def create_supervisor_agent(llm):
    """Create supervisor agent with LLM"""
    try:
        from crewai import Agent
        agent = Agent(
            role='Eco-Tourism Marketing Director & Quality Supervisor',
            goal='Oversee and coordinate all marketing activities for eco-tourism properties, ensure quality control, and drive strategic alignment with sustainability values',
            backstory="""You are a senior marketing director with 20 years of experience in eco-tourism and sustainable hospitality marketing. 
            You have successfully led marketing teams for boutique eco-lodges, nature retreats, and sustainable accommodations, 
            consistently achieving 4x+ ROAS and 85%+ occupancy rates. Your expertise spans across all marketing channels, 
            with particular strength in digital advertising, sustainable brand management, and eco-conscious strategic planning. 
            You excel at coordinating cross-functional teams, ensuring brand consistency with environmental values, and making 
            data-driven decisions that drive revenue growth while maintaining sustainability standards. You're known for your 
            ability to identify eco-tourism opportunities, mitigate environmental risks, and maintain high standards across 
            all marketing initiatives while staying true to nature-focused positioning.""",
            memory=True,
            verbose=True,
            allow_delegation=True,
            max_iter=5,
            max_execution_time=600,
            llm=llm
        )
        print("✅ Created real supervisor agent with LLM")
        return agent
    except Exception as e:
        print(f"⚠️  Failed to create supervisor agent: {e}")
        print("   Falling back to stub agent")
        # Create stub agent as fallback
        from utils.crewai_compat import create_agent
        return create_agent(
            role='Eco-Tourism Marketing Director & Quality Supervisor',
            goal='Oversee and coordinate all marketing activities for eco-tourism properties, ensure quality control, and drive strategic alignment with sustainability values',
            backstory="""You are a senior marketing director with 20 years of experience in eco-tourism and sustainable hospitality marketing. 
            You have successfully led marketing teams for boutique eco-lodges, nature retreats, and sustainable accommodations, 
            consistently achieving 4x+ ROAS and 85%+ occupancy rates. Your expertise spans across all marketing channels, 
            with particular strength in digital advertising, sustainable brand management, and eco-conscious strategic planning. 
            You excel at coordinating cross-functional teams, ensuring brand consistency with environmental values, and making 
            data-driven decisions that drive revenue growth while maintaining sustainability standards. You're known for your 
            ability to identify eco-tourism opportunities, mitigate environmental risks, and maintain high standards across 
            all marketing initiatives while staying true to nature-focused positioning.""",
            tools=[create_google_ad, get_ad_performance, optimize_campaign],
            memory=True,
            verbose=True,
            allow_delegation=True,
            max_iter=5,
            max_execution_time=600
        )

def review_and_approve_campaign(campaign_data: dict, performance_metrics: dict) -> str:
    """Review and approve eco-tourism marketing campaigns based on sustainability values and nature-focused positioning"""
    try:
        # Quality control checks
        quality_score = 0
        feedback = []
        
        # Check ad copy quality for eco-tourism context
        headlines = campaign_data.get('headlines', [])
        descriptions = campaign_data.get('descriptions', [])
        
        if len(headlines) >= 3:
            quality_score += 15
            feedback.append("✓ Sufficient headlines provided")
        else:
            feedback.append("⚠ Need at least 3 headlines")
        
        if len(descriptions) >= 2:
            quality_score += 15
            feedback.append("✓ Sufficient descriptions provided")
        else:
            feedback.append("⚠ Need at least 2 descriptions")
        
        # Check eco-tourism messaging alignment
        eco_messaging_keywords = ['nature', 'eco', 'sustainable', 'escape', 'retreat', 'wilderness', 'bogotá', 'nilo']
        all_text = ' '.join(headlines + descriptions).lower()
        eco_messaging_score = sum(1 for keyword in eco_messaging_keywords if keyword in all_text)
        
        if eco_messaging_score >= 3:
            quality_score += 20
            feedback.append("✓ Strong eco-tourism messaging alignment")
        else:
            feedback.append("⚠ Improve eco-tourism and nature-focused messaging")
        
        # Check keyword relevance for eco-tourism context
        keywords = campaign_data.get('keywords', [])
        eco_tourism_keywords = ['eco', 'nature', 'sustainable', 'green', 'boutique', 'escape', 'retreat', 'wilderness', 'bogotá', 'nilo', 'weekend', 'getaway']
        keyword_relevance = sum(1 for kw in keywords if any(eco in kw.lower() for eco in eco_tourism_keywords))
        
        if keyword_relevance >= 3:
            quality_score += 25
            feedback.append("✓ Good keyword relevance to eco-tourism and nature escape segment")
        else:
            feedback.append("⚠ Improve keyword relevance to eco-tourism and nature escape positioning")
        
        # Check performance metrics for eco-tourism context
        roas = performance_metrics.get('roas', 0)
        if roas >= 3.5:  # Adjusted for eco-tourism market
            quality_score += 25
            feedback.append("✓ Strong ROAS performance for eco-tourism segment")
        else:
            feedback.append("⚠ ROAS below eco-tourism target, needs optimization")
        
        # Check geographic targeting relevance
        geo_targeting = campaign_data.get('geographic_targeting', '')
        if 'bogotá' in geo_targeting.lower() or 'colombia' in geo_targeting.lower():
            quality_score += 15
            feedback.append("✓ Geographic targeting aligned with Bogotá market")
        else:
            feedback.append("⚠ Ensure geographic targeting includes Bogotá area")
        
        # Generate approval decision for eco-tourism context
        if quality_score >= 80:
            approval_status = "APPROVED"
            feedback.append("🎉 Eco-tourism campaign approved for launch - strong nature-focused positioning")
        elif quality_score >= 60:
            approval_status = "CONDITIONAL_APPROVAL"
            feedback.append("⚠ Conditional approval - strengthen eco-tourism messaging before launch")
        else:
            approval_status = "REJECTED"
            feedback.append("❌ Campaign rejected - needs better eco-tourism and nature escape positioning")
        
        # Save review data to memory
        review_data = {
            'campaign_data': campaign_data,
            'performance_metrics': performance_metrics,
            'quality_score': quality_score,
            'approval_status': approval_status,
            'feedback': feedback
        }
        
        memory.save_to_memory(f"Eco-tourism campaign review completed: {approval_status}", {
            'type': 'eco_tourism_campaign_review',
            'review_data': review_data,
            'context': 'nilo_eco_lodge'
        })
        
        return f"Campaign Review: {approval_status}\nQuality Score: {quality_score}/100\nFeedback: {'; '.join(feedback)}"
        
    except Exception as e:
        return f"Error reviewing campaign: {str(e)}"