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
        
        # Connect to MongoDB
        self.mongo_client = MongoClient(st.secrets["mongo_uri"])
        self.db = self.mongo_client.surrogate_stories
        
        # Try to load existing session data
        if 'session_id' in st.session_state:
            self.session_id = st.session_state.session_id
            self._load_session_data()
        else:
            self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
            st.session_state.session_id = self.session_id
    
    def _load_session_data(self):
        """Load existing session data from MongoDB"""
        try:
            # Load stories
            stories = self.db.stories.find({'session_id': self.session_id}).sort('timestamp', 1)
            for story in stories:
                self.session_story.append({
                    'timestamp': story['timestamp'],
                    'segment': story['segment']
                })
                self.current_story = story['segment']
            
            # Load other session data...
            prompts = self.db.prompts.find({'session_id': self.session_id}).sort('timestamp', 1)
            for prompt in prompts:
                self.user_prompts.append({
                    'timestamp': prompt['timestamp'],
                    'prompt': prompt['prompt']
                })
            
            # Similar loading for parameters and challenges...
            
        except Exception as e:
            st.error(f"Error loading session data: {str(e)}")

    def add_user_prompt(self, prompt):
        prompt_data = {
            'timestamp': datetime.now().isoformat(),
            'prompt': prompt
        }
        self.user_prompts.append(prompt_data)
        # Save prompt immediately
        self.db.prompts.insert_one({
            'session_id': self.session_id,
            **prompt_data
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
            segment_data = {
                'timestamp': datetime.now().isoformat(),
                'segment': self.current_story
            }
            self.session_story.append(segment_data)
            # Save story segment immediately
            self.db.stories.insert_one({
                'session_id': self.session_id,
                **segment_data
            })

    def save_session(self):
        try:
            # Save session summary
            session_data = {
                'session_id': self.session_id,
                'timestamp': datetime.now().isoformat(),
                'complete_story': self.get_complete_story(),
                'num_prompts': len(self.user_prompts),
                'num_segments': len(self.session_story)
            }
            
            self.db.sessions.insert_one(session_data)
            return "Session saved successfully", "Data saved to MongoDB"
            
        except Exception as e:
            return f"Error: {str(e)}", f"Error: {str(e)}"

    def get_complete_story(self):
        return "\n".join(segment['segment'] for segment in self.session_story) 