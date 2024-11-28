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
• Write a simple story (about 100 words) that:
  - Uses easy, everyday English
  - Features grandparents using the social surrogate robot
  - Must explicitly show how the parameter from user input is being used
  - Must include at least one clear interaction showcasing this parameter
  - Structure the story to:
    1. Introduce the surrogate with grandparents
    2. Show the parameter in action
    3. Then either:
       a) Show a challenge with this specific parameter, or (60%)
       b) Show success with this parameter but hint at a different need, or (10%)
       c) Show how this parameter leads to discovering another aspect (30%)
• If continuing story:
  - Follow the same structure as above
  - Build naturally from the previous part
  - Must explicitly show how the new parameter or solution is being used
  - Show clear interaction with this new parameter
  - End with either a challenge, success with new need, or discovered aspect
• Format response as:
  "STORY:
   [your simple story in everyday English]
   " """,
    )
    
    return agent_a, agent_b, agent_c 