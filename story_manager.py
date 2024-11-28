import csv
from datetime import datetime
import json
import os

class StoryManager:
    def __init__(self):
        self.current_story = ""
        self.session_story = []
        self.user_prompts = []
        self.parameter_history = []
        self.challenge_history = []
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Create logs directory if it doesn't exist
        os.makedirs('logs', exist_ok=True)
        
    def add_user_prompt(self, prompt):
        self.user_prompts.append({
            'timestamp': datetime.now().isoformat(),
            'prompt': prompt
        })

    def add_parameter(self, parameter):
        self.parameter_history.append({
            'timestamp': datetime.now().isoformat(),
            'parameter': parameter
        })

    def add_challenge(self, challenge):
        self.challenge_history.append({
            'timestamp': datetime.now().isoformat(),
            'challenge': challenge
        })

    def add_story_segment(self, story_text):
        if "STORY:" in story_text:
            self.current_story = story_text.split("STORY:")[1].strip()
            self.session_story.append({
                'timestamp': datetime.now().isoformat(),
                'segment': self.current_story
            })

    def save_session(self):
        # Save detailed JSON log
        json_filename = f"logs/session_{self.session_id}_detailed.json"
        detailed_log = {
            'session_id': self.session_id,
            'timestamp': datetime.now().isoformat(),
            'user_prompts': self.user_prompts,
            'parameters': self.parameter_history,
            'challenges': self.challenge_history,
            'story_segments': self.session_story
        }
        
        with open(json_filename, 'w', encoding='utf-8') as f:
            json.dump(detailed_log, f, indent=2)

        # Save CSV for easy reading
        csv_filename = f"logs/session_{self.session_id}_summary.csv"
        with open(csv_filename, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['Timestamp', 'Type', 'Content'])
            
            # Write user prompts
            for prompt in self.user_prompts:
                writer.writerow([prompt['timestamp'], 'User Prompt', prompt['prompt']])
            
            # Write parameters
            for param in self.parameter_history:
                writer.writerow([param['timestamp'], 'Parameter', param['parameter']])
            
            # Write challenges
            for challenge in self.challenge_history:
                writer.writerow([challenge['timestamp'], 'Challenge', challenge['challenge']])
            
            # Write story segments
            for segment in self.session_story:
                writer.writerow([segment['timestamp'], 'Story Segment', segment['segment']])

        return json_filename, csv_filename

    def get_complete_story(self):
        return "\n".join(segment['segment'] for segment in self.session_story) 