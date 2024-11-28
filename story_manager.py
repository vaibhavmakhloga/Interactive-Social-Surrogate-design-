from datetime import datetime
import streamlit as st
from pymongo import MongoClient

class StoryManager:
    def __init__(self):
        self.current_story = ""
        self.session_story = []
        self.user_prompts = []
        self.parameter_history = []
        self.challenge_history = []
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Initialize MongoDB connection
        self.mongo_client = MongoClient(st.secrets["mongo_uri"])
        self.db = self.mongo_client.social_surrogate_db
        
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
        try:
            # Prepare session data
            session_data = {
                'session_id': self.session_id,
                'timestamp': datetime.now().isoformat(),
                'user_prompts': self.user_prompts,
                'parameters': self.parameter_history,
                'challenges': self.challenge_history,
                'story_segments': self.session_story,
                'complete_story': self.get_complete_story()
            }
            
            # Save to MongoDB
            self.db.sessions.insert_one(session_data)
            
            return "Session saved to MongoDB", "Data saved successfully"
                
        except Exception as e:
            return f"Error saving to MongoDB: {str(e)}", f"Error: {str(e)}"

    def get_complete_story(self):
        return "\n".join(segment['segment'] for segment in self.session_story) 