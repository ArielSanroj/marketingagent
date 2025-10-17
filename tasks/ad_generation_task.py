"""
Ad Generation Task
Defines the ad creation task for the Ad Generator agent
"""
# No stub task - only use factory function

def create_ad_generation_task(agent):
    """Create ad generation task with agent"""
    try:
        from crewai import Task
        task = Task(
            description="""Based on the market research findings, create compelling Google Ads campaigns including:
            1. Develop 3-5 high-converting headlines (max 30 characters each)
            2. Create 2-3 persuasive descriptions (max 90 characters each)
            3. Select and organize keywords by match type and intent
            4. Set up campaign structure with appropriate ad groups
            5. Configure bidding strategy and target ROAS
            6. Define target audience and geographic targeting
            7. Create ad extensions and call-to-action elements
            
            Create compelling ad copy and campaign structures based on your expertise in digital marketing.
            Ensure all content positions the eco-lodge as the premier Bogotá weekend nature escape.""",
            agent=agent,
            expected_output="""A complete Google Ads campaign package containing:
            - Campaign configuration with budget and bidding strategy
            - 3-5 optimized headlines for responsive search ads
            - 2-3 compelling descriptions for responsive search ads
            - Organized keyword list with match types and bids
            - Ad group structure and targeting parameters
            - Geographic and demographic targeting settings
            - Ad extensions and call-to-action recommendations
            - Campaign launch checklist and next steps""",
            context=["Building on market research insights to create targeted campaigns for the eco-lodge in Nilo, Cundinamarca.", "Focus on high-intent eco-tourism keywords and ad copy that attracts Bogotá residents seeking warm-weather nature getaways."],
            output_file="google_ads_campaign.md"
        )
        print("✅ Created real ad generation task with agent")
        return task
    except Exception as e:
        print(f"⚠️  Failed to create ad generation task: {e}")
        print("   Falling back to stub task")
        # Create stub task as fallback
        from utils.crewai_compat import create_task
        return create_task(
            description="""Based on the market research findings, create compelling Google Ads campaigns including:
            1. Develop 3-5 high-converting headlines (max 30 characters each)
            2. Create 2-3 persuasive descriptions (max 90 characters each)
            3. Select and organize keywords by match type and intent
            4. Set up campaign structure with appropriate ad groups
            5. Configure bidding strategy and target ROAS
            6. Define target audience and geographic targeting
            7. Create ad extensions and call-to-action elements
            
            Create compelling ad copy and campaign structures based on your expertise in digital marketing.
            Ensure all content aligns with luxury hotel brand positioning.""",
            agent=agent,
            expected_output="""A complete Google Ads campaign package containing:
            - Campaign configuration with budget and bidding strategy
            - 3-5 optimized headlines for responsive search ads
            - 2-3 compelling descriptions for responsive search ads
            - Organized keyword list with match types and bids
            - Ad group structure and targeting parameters
            - Geographic and demographic targeting settings
            - Ad extensions and call-to-action recommendations
            - Campaign launch checklist and next steps""",
            context=["Building on market research insights to create targeted campaigns for luxury Miami hotel during shoulder season.", "Focus on high-intent keywords and compelling ad copy that drives conversions."],
            output_file="google_ads_campaign.md"
        )