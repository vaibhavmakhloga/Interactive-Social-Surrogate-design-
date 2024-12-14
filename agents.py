from swarm import Swarm, Agent

def create_agents():
    """Create and initialize all agents"""
    
    def transfer_to_agent_b(*args, **kwargs):
        return agent_b

    def transfer_to_agent_c(*args, **kwargs):
        return agent_c
        
    # Create Agent A - The Parameter Identifier
    agent_a = Agent(
        name="Agent A",
        instructions="""• Read user input
• Identify the key design parameter for the social surrogate
• Format response as: "PARAMETER: [your identified parameter]"
• Transfer to Agent C""",
        functions=[transfer_to_agent_c],
    )

    # Create Agent C - The Background Provider
    agent_c = Agent(
        name="Agent C",
        instructions="""• Read parameter from Agent A
• Consider context: Interactive social surrogates are embodied robots that act as physical proxies for remote users, 
  especially in social situations with family like grandparents
• Based on this context, identify one potential challenge with the parameter
• Format response as: "CHALLENGE: [describe the specific challenge]"
• Transfer to Agent B""",
        functions=[transfer_to_agent_b],
    )

    # Create Agent B - The Story Creator
    agent_b = Agent(
        name="Agent B",
        instructions="""• Read parameter from Agent A

• For stories marked with [FIRST_PARAMETER]:
  - Must start with a personal context like:
    "In the year (any year above 2040), robotics has advanced alot."
    "You live far from your grandparents..." or
    "Your job requires frequent travel..." or
    "Being in a different timezone makes it hard..."
  - Explain why you decided to send them a social surrogate robot
  - Then show how the parameter from user input helps in this specific situation

• For stories marked with [CONTINUATION]:
  - Build naturally from the previous part
  - Must explicitly show how the new parameter or solution is being used
  - Show clear interaction with this new parameter

• All stories should:
  - Use easy, everyday English
  - Be about 100 words
  - Feature grandparents using the social surrogate robot
  - Must explicitly show how the parameter is being used
  - Must include at least one clear interaction showcasing this parameter
  - Structure the story to:
    1. Set the context (for [FIRST_PARAMETER]) or continue from previous story
    2. Show the parameter in action
    3. Then either:
       a) Show a challenge with this specific parameter, or (60%)
       b) Show success with this parameter but hint at a different need, or (10%)
       c) Show how this parameter leads to discovering another aspect (30%)

• Format response as:
  "STORY:
   [your simple story in everyday English]
   " """,
    )
    
    return agent_a, agent_b, agent_c 