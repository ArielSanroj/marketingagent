"""
Optimization Task
Defines the optimization task for the Performance Optimizer agent
"""
# No stub task - only use factory function

def create_optimization_task(agent):
    """Create optimization task with agent"""
    try:
        from crewai import Task
        from utils.marketing_instructions import INSTRUCTIONS_JSON
        task = Task(
            description="""Analyze the created Google Ads campaign and optimize for maximum performance:
            1. Review campaign performance metrics and KPIs
            2. Identify underperforming keywords and ad groups
            3. Analyze click-through rates and conversion data
            4. Optimize bidding strategies and budget allocation
            5. Test and refine ad copy variations
            6. Adjust targeting parameters based on performance
            7. Implement A/B testing recommendations
            8. Monitor quality scores and ad relevance
            
            Provide data-driven optimization recommendations based on your expertise in digital marketing.
            Focus on improving ROAS, CTR, and conversion rates while reducing CPC.""",
            agent=agent,
            expected_output="""A comprehensive optimization report containing:
            - Current performance analysis with key metrics
            - Identified optimization opportunities
            - Specific recommendations for keyword adjustments
            - Ad copy testing suggestions
            - Bidding strategy improvements
            - Budget reallocation recommendations
            - Quality score improvement plan
            - Expected performance improvements
            - Implementation timeline and next steps""",
            context=[
                "Optimizing the newly created Google Ads campaign to maximize eco-lodge bookings near Bogotá.",
                "Focus on attracting nature-focused weekend travelers and keeping occupancy high during dry season weekends.",
                "Instructions:",
                INSTRUCTIONS_JSON
            ],
            output_file="optimization_report.md"
        )
        print("✅ Created real optimization task with agent")
        return task
    except Exception as e:
        print(f"⚠️  Failed to create optimization task: {e}")
        print("   Falling back to stub task")
        # Create stub task as fallback
        from utils.crewai_compat import create_task
        return create_task(
            description="""Analyze the created Google Ads campaign and optimize for maximum performance:
            1. Review campaign performance metrics and KPIs
            2. Identify underperforming keywords and ad groups
            3. Analyze click-through rates and conversion data
            4. Optimize bidding strategies and budget allocation
            5. Test and refine ad copy variations
            6. Adjust targeting parameters based on performance
            7. Implement A/B testing recommendations
            8. Monitor quality scores and ad relevance
            
            Provide data-driven optimization recommendations based on your expertise in digital marketing.
            Focus on improving ROAS, CTR, and conversion rates while reducing CPC.""",
            agent=agent,
            expected_output="""A comprehensive optimization report containing:
            - Current performance analysis with key metrics
            - Identified optimization opportunities
            - Specific recommendations for keyword adjustments
            - Ad copy testing suggestions
            - Bidding strategy improvements
            - Budget reallocation recommendations
            - Quality score improvement plan
            - Expected performance improvements
            - Implementation timeline and next steps""",
            context=["Optimizing the newly created Google Ads campaign to maximize performance during shoulder season.", "Focus on improving efficiency and driving higher quality traffic."],
            output_file="optimization_report.md"
        )