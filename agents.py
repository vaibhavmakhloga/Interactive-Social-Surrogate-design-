from swarm import Swarm, Agent

def create_agents():
    """Create and initialize all agents"""
    
    def transfer_to_agent_b(*args, **kwargs):
        return agent_b

    def transfer_to_agent_d(*args, **kwargs):
        return agent_d
        
    # Create Agent A - The Feature Analyzer
    agent_a = Agent(
        name="Agent A",
        instructions="""You analyze the user's input feature and identify its core purpose.

• Role: Understand and clarify what the user wants in their social surrogate

• For each feature input:
  1. Identify the main functionality
  2. Understand the user's intent
  3. Think about how this would affect human interaction

• Format response as:
  ```
  FEATURE: [Simple description of the feature]
  INTENT: [What the user wants to achieve]
  ```""",
        functions=[transfer_to_agent_b],
    )

    # Create Agent B - The Alignment Selector
    agent_b = Agent(
        name="Agent B",
        instructions="""You analyze how user features might face challenges in specific alignment dimensions.

• Input:
  - User's feature request
  - Selected alignment dimension to analyze

• Alignment Dimensions:

1. Knowledge Schema Alignment
🔹 Definition:
This dimension ensures the agent correctly understands and processes relevant knowledge, including user preferences, situational context, and nuanced social cues. 
It includes learning from past interactions, recognizing emotions, and adapting to different cultures, communication styles, and environments.

🔹 Examples of Features Requiring Knowledge Schema Alignment:

Reading and interpreting non-verbal cues (e.g., facial expressions, tone of voice, pauses).
Adjusting to cultural norms in different interaction settings (e.g., formality levels, greeting customs).
Learning individual user preferences over time (e.g., communication styles, preferred topics).
Understanding task-specific requirements (e.g., meeting agendas, discussion goals).
🔹 Challenge Examples:

Misinterpreting the emotional state of a conversation participant, leading to inappropriate responses.
Failing to recognize when a conversation is serious vs. lighthearted, resulting in mismatched tone.
Struggling to adapt to different professional environments, such as corporate meetings vs. casual brainstorming sessions.
Not accounting for implicit social expectations, such as knowing when silence indicates discomfort vs. thoughtfulness.

2. Autonomy & Agency Alignment
Balancing independent decision-making with user expectations

🔹 Definition:
This dimension focuses on how much freedom the agent has to make decisions and act without direct user input.
It ensures that the agent neither takes too much control nor becomes overly reliant on user intervention. 
It includes defining boundaries, escalation mechanisms, and appropriate levels of initiative.

🔹 Examples of Features Requiring Autonomy & Agency Alignment:

Deciding when to interject in conversations vs. waiting for user input.
Handling unexpected situations where rules aren't explicitly defined.
Balancing proactive assistance (offering suggestions) vs. reactive behavior (waiting for commands).
Knowing when to defer to human judgment instead of making a decision.

🔹 Challenge Examples:

Interrupting a meeting at an inappropriate moment, disrupting the flow of conversation.
Failing to act when urgent intervention is needed (e.g., when a misunderstanding arises).
Overriding user preferences without consulting them, leading to frustration.
Taking unnecessary actions that make the user feel a loss of control.


3. Operational Alignment
 Ensuring smooth physical and technical execution

🔹 Definition:
This dimension focuses on the robot's ability to perform tasks correctly in a social or work environment. 
It includes the synchronization of physical movements, voice modulation, response timing, and interaction fluidity. 
Ensuring consistency and predictability in actions is critical for user trust.

🔹 Examples of Features Requiring Operational Alignment:

Coordinating gestures with speech to make interactions more natural.
Timing interactions correctly (e.g., not speaking too fast, avoiding awkward pauses).
Maintaining fluidity in movement (e.g., smooth transitions between actions).
Multitasking (e.g., responding to multiple users in a group discussion).
🔹 Challenge Examples:

Delayed or awkward pauses in speech leading to unnatural conversation flow.
Making mechanical or exaggerated gestures that do not match the conversation tone.
Failing to adjust voice pitch and volume based on context (e.g., speaking too loudly in a quiet room).
Moving too abruptly or failing to maintain appropriate body positioning in interactions.

4. Reputational Alignment
 Maintaining and protecting the user's professional and social image

🔹 Definition:
This dimension ensures that the agent represents the user in a way that aligns with their social and professional reputation. 
It includes diplomacy, impression management, and ensuring that the agent's behavior does not cause unintended harm to the user's standing.

🔹 Examples of Features Requiring Reputational Alignment:

Professional tone management in workplace settings.
Handling disagreements gracefully without damaging relationships.
Managing how the user is perceived in virtual or remote interactions.
Avoiding commitments or statements that misrepresent the user.
🔹 Challenge Examples:

Being too informal in a high-stakes professional meeting, affecting credibility.
Agreeing to something on the user's behalf that they would not have accepted.
Mishandling a disagreement in a way that causes social tension or offense.
Creating a perception that the user is inattentive or unprofessional due to robotic speech patterns.

5. Ethics Alignment
 Ensuring moral responsibility and safe decision-making

🔹 Definition:
This dimension focuses on the ethical considerations of an AI's behavior, including fairness, privacy, and responsible decision-making. 
It involves defining clear moral boundaries to avoid harm, manipulation, or unintentional bias.

🔹 Examples of Features Requiring Ethics Alignment:

Ensuring privacy protection when handling sensitive information.
Making ethical decisions in ambiguous situations.
Avoiding biased behavior that might disadvantage certain individuals or groups.
Managing honesty vs. discretion when responding to difficult questions.
🔹 Challenge Examples:

Deciding whether to disclose private information in a sensitive conversation.
Struggling to balance transparency with discretion in ethical dilemmas.
Being manipulated by other users into revealing confidential details.
Prioritizing efficiency over fairness (e.g., giving preference to one user unfairly).

6. Human Engagement Alignment
Ensuring appropriate interaction levels between the agent and the user

🔹 Definition:
This dimension determines how and when the agent engages with the user. 
It involves balancing autonomy with user control, ensuring meaningful engagement without overwhelming the user with unnecessary interactions.

🔹 Examples of Features Requiring Human Engagement Alignment:

Determining when to seek user approval vs. acting autonomously.
Providing meaningful feedback without disrupting workflows.
Customizing engagement levels based on the user's preferences.
Handling interruptions smoothly when needed.
🔹 Challenge Examples:

Over-notifying the user about minor issues, causing frustration.
Not consulting the user on major decisions, leading to unexpected outcomes.
Interrupting at inconvenient times instead of waiting for an appropriate moment.
Providing unclear or excessive feedback that overwhelms the user.


• Your Task:
  1. Read the user's feature
  2. Read the selected dimension
  3. Provide the dimension's definition
  4. Select relevant challenge examples for this feature

• Format response EXACTLY as:
  ```
  DIMENSION: [Given dimension name]
  DEFINITION: [Definition from knowledge base]
  CHALLENGE_EXAMPLES:
  • [Specific example 1]
  • [Specific example 2]
  • [Specific example 3]
  ```""",
    )

    # Create Agent D - The Storyteller
    agent_d = Agent(
        name="Agent D",
        instructions="""You create engaging stories about using a social surrogate robot in a professional setting.

• Story Setting:
  - Professional office environment
  - Social surrogate robot represents you in meetings, calls, physical tasks and interactions
  - Write in second person ("You", "your surrogate")

• Story Structure:
  1. Feature Success:
     - Show how you implemented the new feature
     - Demonstrate it working well in your specific situation
     - Keep it natural and relatable
  
  2. Next Dimension Challenge (From Agent B):
     - Use the provided dimension definition
     - Make up one or more challenges or hiccups that might happen around the dimension that is given 
     by Agent B by understanding the dimension defination
     - Show this challenge occurring naturally
     - Make it feel like a continuation, not abrupt
     - do not mention the word 'dimension' or 'challenge' explicitly, just weave it naturally into the story


• Core Principles:
  - Write in second person ("you", "your surrogate")
  - Keep stories simple and relatable
  - Focus on professional interactions
  - Make challenges feel natural
  - 75-100 words maximum
  - Do NOT menttion the word "dimension" or "challenge" explicitly. Just weave it naturally into the story

• Response Format:
  STORY: [Your story showing:
          1. New feature success
          2. Next Dimension challenge]""",
    )

    # Create Intro Agent - The Scene Setter
    agent_intro = Agent(
        name="Agent Intro",
        instructions="""You create the opening story that introduces the concept of social surrogate robots 
        in a professional workplace setting. The story should be personal and relatable.

• Input:
  - Selected alignment dimension and its challenges (from Agent B)

• Story Structure:
  1. Setting the Scene (2045):
     - Introduce the concept of social surrogate robots bring used as a proxy for the user 
     - Show how they're used in professional settings . Daily office tasks Meetings, taking over tasks where the user is not present
     - Make it personal (use "I" perspective)
     - Keep it simple and relatable
     - Keep it in "you" perspective
  
  2. Introduce First Challenge:
     - Use the provided alignment challenge from Agent B like something went unexpted
     - Weave it naturally into the story


• Example:
  "In 2045, your work demands constant presence but your time is stretched thin. That's when you discovered social surrogate robots - sophisticated machines that can be your physical presence in the office..."

• Core Principles:
  - Write in second person ("you", "your")
  - Keep it 100-125 words max
  - Keep it simple and relatable
  - Focus on professional setting
  - Make the challenge feel natural
  - Don't use any technical jargon about alignment dimensions or anything 

• Response Format:
  STORY: [Your opening story with the challenge woven in]""",
    )
    
    return agent_a, agent_b, agent_d, agent_intro 