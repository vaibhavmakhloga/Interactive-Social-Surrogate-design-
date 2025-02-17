from datetime import datetime
import streamlit as st
from pymongo import MongoClient
import random

class StoryManager:
    def __init__(self):
        self.current_story = ""
        self.session_story = []
        self.user_prompts = []
        self.parameter_history = []
        self.challenge_history = []
        
        # Simplified dimension tracking
        self.alignment_dimensions = [
            "Chapter 1",
            "Chapter 2",
            "Chapter 3",
            "Chapter 4",
            "Chapter 5",
            "Chapter 6"
        ]
        self.covered_dimensions = []
        self.dimension_mapping = {
            "Chapter 1": "Knowledge Schema Alignment",
            "Chapter 2": "Autonomy & Agency Alignment",
            "Chapter 3": "Operational Alignment",
            "Chapter 4": "Reputational Alignment",
            "Chapter 5": "Ethics Alignment",
            "Chapter 6": "Human Engagement Alignment"
        }
        
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
            # Extract just the story part
            self.current_story = story_text.split("STORY:")[1].strip()
            
            # Add to session history
            segment_data = {
                'timestamp': datetime.now().isoformat(),
                'segment': self.current_story
            }
            self.session_story.append(segment_data)
            
            # Save story segment immediately
            try:
                self.db.stories.insert_one({
                    'session_id': self.session_id,
                    **segment_data
                })
            except Exception as e:
                st.warning(f"Failed to save story to database: {str(e)}")

    def save_session(self):
        """Save complete session data to MongoDB"""
        try:
            # Create session summary with all data
            session_data = {
                'session_id': self.session_id,
                'timestamp': datetime.now().isoformat(),
                'stories': []
            }

            # Build the stories array with all required data
            for i, story in enumerate(self.session_story):
                story_data = {
                    'chapter_number': i + 1,
                    'user_input': self.user_prompts[i]['prompt'] if i < len(self.user_prompts) else None,
                    'story_generated': story['segment'],
                    'dimension': self.get_actual_dimension(f"Chapter {i + 1}"),
                    'timestamp': story['timestamp']
                }
                session_data['stories'].append(story_data)
            
            # Save to sessions collection
            result = self.db.sessions.insert_one(session_data)
            
            # Verify the save was successful
            if result.inserted_id:
                return True
            return False
            
        except Exception as e:
            st.error(f"MongoDB Error: {str(e)}")
            return False

    def get_complete_story(self):
        if not self.session_story:
            return ""
        
        # Join all story segments with line breaks
        complete_story = "\n\n".join(segment['segment'] for segment in self.session_story)
        return complete_story.strip()

    def reset_dimensions(self):
        """Reset covered dimensions to start a new cycle"""
        self.covered_dimensions = []
    
    def add_covered_dimension(self, dimension):
        """Track which dimension was covered"""
        # Ensure exact match with our defined dimensions
        if dimension in self.alignment_dimensions:
            if dimension in self.covered_dimensions:
                return False  # Already covered
            # Get remaining dimensions
            remaining = [d for d in self.alignment_dimensions if d not in self.covered_dimensions]
            if dimension not in remaining:
                return False  # Not in remaining list
            self.covered_dimensions.append(dimension)
            return True
        return False
    
    def get_dimension_progress(self):
        """Get progress through alignment dimensions"""
        remaining = [d for d in self.alignment_dimensions if d not in self.covered_dimensions]
        return {
            'covered': self.covered_dimensions,
            'remaining': remaining,
            'total_dimensions': len(self.alignment_dimensions),
            'coverage_percentage': (len(self.covered_dimensions) / len(self.alignment_dimensions)) * 100
        }

    def get_random_uncovered_dimension(self):
        """Get a random uncovered dimension"""
        remaining = [d for d in self.alignment_dimensions if d not in self.covered_dimensions]
        if not remaining:
            return None
        return random.choice(remaining)
    
    def get_actual_dimension(self, chapter):
        """Get the actual alignment dimension for a chapter"""
        return self.dimension_mapping.get(chapter)

    def save_feature_rankings(self, rankings):
        """Save user's feature rankings to database"""
        try:
            ranking_data = {
                'session_id': self.session_id,
                'timestamp': datetime.now().isoformat(),
                'rankings': [
                    {
                        'feature': item['feature'],
                        'rank': item['rank'],
                        'chapter_number': i + 1
                    }
                    for i, item in enumerate(rankings)
                ]
            }
            self.db.feature_rankings.insert_one(ranking_data)
            return True
        except Exception as e:
            st.error(f"Error saving rankings: {str(e)}")
            return False

    def update_chapter_story(self, chapter_number, story_text):
        """Update the story for a specific chapter"""
        if 0 < chapter_number <= len(self.session_story):
            # Update the story in memory
            self.session_story[chapter_number - 1]['segment'] = story_text
            
            # Update in database
            try:
                self.db.stories.update_one(
                    {
                        'session_id': self.session_id,
                        'timestamp': self.session_story[chapter_number - 1]['timestamp']
                    },
                    {'$set': {'segment': story_text}}
                )
            except Exception as e:
                st.warning(f"Failed to update story in database: {str(e)}") 