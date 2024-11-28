import csv
from datetime import datetime
import json
import os
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
        try:
            self.mongo_client = MongoClient(st.secrets["mongo_uri"])
            self.db = self.mongo_client.social_surrogate_db
            print("MongoDB connected successfully")
        except Exception as e:
            st.error(f"MongoDB connection error: {str(e)}")
        
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
                'user_prompts': [
                    {
                        'timestamp': prompt['timestamp'],
                        'prompt': prompt['prompt']
                    } for prompt in self.user_prompts
                ],
                'parameters': [
                    {
                        'timestamp': param['timestamp'],
                        'parameter': param['parameter']
                    } for param in self.parameter_history
                ],
                'challenges': [
                    {
                        'timestamp': challenge['timestamp'],
                        'challenge': challenge['challenge']
                    } for challenge in self.challenge_history
                ],
                'story_segments': [
                    {
                        'timestamp': segment['timestamp'],
                        'segment': segment['segment']
                    } for segment in self.session_story
                ],
                'complete_story': self.get_complete_story()
            }
            
            # Save to MongoDB
            result = self.db.sessions.insert_one(session_data)
            
            if result.inserted_id:
                return (
                    f"Session {self.session_id} saved successfully", 
                    "Data saved to MongoDB"
                )
            else:
                return "Failed to save session", "Error saving data"
                
        except Exception as e:
            error_msg = f"Error saving to MongoDB: {str(e)}"
            st.error(error_msg)
            return error_msg, error_msg

    def get_complete_story(self):
        return "\n".join(segment['segment'] for segment in self.session_story) 