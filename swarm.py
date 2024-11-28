import os
from anthropic import Anthropic

class Agent:
    def __init__(self, name, instructions, functions=None):
        self.name = name
        self.instructions = instructions
        self.functions = functions or []

class Swarm:
    def __init__(self):
        self.client = Anthropic(api_key=os.getenv('OPENAI_API_KEY'))
        
    def run(self, agent, messages):
        # Prepare the conversation
        conversation = []
        for msg in messages:
            conversation.append({
                "role": msg["role"],
                "content": msg["content"]
            })
        
        # Add agent instructions
        system_message = f"You are {agent.name}. {agent.instructions}"
        
        # Make the API call
        response = self.client.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=1000,
            messages=[
                {"role": "system", "content": system_message},
                *conversation
            ]
        )
        
        # Check if we should transfer to another agent
        if agent.functions and response.content[0].text.lower().find("transfer") != -1:
            next_agent = agent.functions[0]()
            return self.run(next_agent, messages + [{"role": "assistant", "content": response.content[0].text}])
        
        return type('Response', (), {'messages': messages + [{"role": "assistant", "content": response.content[0].text}]}) 