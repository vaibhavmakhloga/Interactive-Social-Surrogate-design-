import streamlit as st
from swarm import Swarm
from agents import create_agents
from story_manager import StoryManager
import pandas as pd
from datetime import datetime
import time

def set_custom_style():
    st.markdown("""
        <style>
        /* Modern, high-contrast theme */
        .stApp {
            max-width: 1400px;
            margin: 0 auto;
            background-color: #ffffff !important;
        }
        
        /* Updated Story box with paper-like appearance */
        .story-box {        
            background-color: #fff9f0;  /* Slightly off-white, paper-like color */
            border-radius: 3px;
            padding: 30px;
            margin: 15px 0;
            font-family: 'Crimson Text', Georgia, serif;  /* More story-like font */
            box-shadow: 0 0 15px rgba(0,0,0,0.1);
            color: #2c3e50;
            font-size: 18px;
            line-height: 1.8;
            border: none;
            position: relative;
            background-image: linear-gradient(#e5e5e5 1px, transparent 1px);
            background-size: 100% 1.8em;
            min-height: 200px;
            text-align: left;
        }
        
        /* Paper texture and edges */
        .story-box::before {
            content: '';
            position: absolute;
            left: 0;
            top: 0;
            width: 100%;
            height: 100%;
            background-image: 
                url('data:image/png;base64,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');
            opacity: 0.03;
            pointer-events: none;
        }
        
        .story-box::after {
            content: '';
            position: absolute;
            left: -5px;
            top: 0;
            width: 4px;
            height: 100%;
            background: linear-gradient(to right, #d4d4d4, transparent);
            border-left: 1px solid #e0e0e0;
        }
        
        /* Story line animation with pen-writing effect */
        .story-line {
            opacity: 0;
            animation: fadeInLine 1s ease-out forwards;
            position: relative;
            margin-bottom: 1.8em;
            padding-left: 10px;
        }
        
        /* Pen cursor effect */
        .story-line::before {
            content: '✎';
            position: absolute;
            left: -20px;
            opacity: 0;
            color: #3498db;
            animation: writingCursor 0.5s ease-in-out forwards;
            animation-delay: inherit;
        }
        
        @keyframes writingCursor {
            0% {
                opacity: 0;
                transform: translateX(-10px);
            }
            50% {
                opacity: 1;
            }
            100% {
                opacity: 0;
                transform: translateX(5px);
            }
        }
        
        /* Enhanced typing animation */
        @keyframes fadeInLine {
            0% {
                opacity: 0;
                transform: translateY(10px);
            }
            100% {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        .delay-1 { animation-delay: 0.3s; }
        .delay-2 { animation-delay: 0.6s; }
        .delay-3 { animation-delay: 0.9s; }
        .delay-4 { animation-delay: 1.2s; }
        .delay-5 { animation-delay: 1.5s; }
        
        /* Story header styling */
        .header-style {
            font-family: 'Crimson Text', Georgia, serif;
            color: #2c3e50;
            font-size: 28px;
            font-weight: 600;
            margin: 25px 0 15px 0;
            padding-bottom: 8px;
            border-bottom: 2px solid #3498db;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
        }
        
        /* Challenge box */
        .challenge-box {
            background-color: #f8f9fa;
            border-radius: 8px;
            padding: 15px 20px;
            margin: 12px 0;
            font-family: 'Inter', sans-serif;
            box-shadow: 0 2px 6px rgba(0,0,0,0.08);
            color: #2c3e50;
            border-left: 4px solid #e74c3c;
        }
        
        /* Headers */
        .header-style {
            color: #2c3e50;
            font-size: 24px;
            font-weight: 600;
            margin: 25px 0 15px 0;
            font-family: 'Inter', sans-serif;
            border-bottom: 2px solid #3498db;
            padding-bottom: 8px;
        }
        
        /* Info boxes */
        .stAlert {
            background-color: #f8f9fa !important;
            color: #2c3e50 !important;
            border: 1px solid #e0e0e0 !important;
            border-radius: 8px !important;
        }
        
        /* Buttons */
        .stButton button {
            background-color: #3498db !important;
            color: white !important;
            font-weight: 500 !important;
            border: none !important;
            padding: 10px 20px !important;
            border-radius: 8px !important;
        }
        
        /* Text areas */
        .stTextArea textarea {
            background-color: #ffffff !important;
            border-radius: 8px !important;
            border: 2px solid #e0e0e0 !important;
            padding: 12px !important;
            font-size: 16px !important;
            color: #2c3e50 !important;
        }
        
        /* Text area placeholder */
        .stTextArea textarea::placeholder {
            color: #95a5a6 !important;
            opacity: 1 !important;
        }
        
        /* Text area focus state */
        .stTextArea textarea:focus {
            border-color: #3498db !important;
            box-shadow: 0 0 0 1px #3498db !important;
        }
        
        /* Sidebar */
        .css-1d391kg {
            background-color: #f8f9fa !important;
        }
        
        /* Text colors */
        p, h1, h2, h3, h4, h5, h6, .stMarkdown {
            color: #2c3e50 !important;
        }
        
        /* Example text */
        em {
            color: #666666 !important;
        }
        
        /* Typing animation */
        @keyframes typing {
            from { width: 0 }
            to { width: 100% }
        }
        
        .typing-effect {
            overflow: hidden;
            white-space: pre-wrap;
            animation: typing 2s steps(40, end);
        }
        
        /* Section dividers */
        hr {
            margin: 30px 0;
            border: none;
            border-top: 2px solid #e0e0e0;
        }
        
        /* Toggle switch styling */
        .stCheckbox {
            background-color: white !important;
            padding: 10px !important;
            border-radius: 8px !important;
            border: 1px solid #e0e0e0 !important;
        }
        
        .stCheckbox label {
            color: #2c3e50 !important;
            font-weight: 500 !important;
        }
        
        /* Info text under design input */
        .stAlert > div {
            color: #2c3e50 !important;
            background-color: #f8f9fa !important;
            border: 1px solid #e0e0e0 !important;
        }
        
        /* Improved typing animation */
        @keyframes fadeInLine {
            from { 
                opacity: 0;
                transform: translateY(10px);
            }
            to { 
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        .story-line {
            opacity: 0;
            animation: fadeInLine 0.5s ease-out forwards;
        }
        
        .delay-1 { animation-delay: 0.5s; }
        .delay-2 { animation-delay: 1.0s; }
        .delay-3 { animation-delay: 1.5s; }
        /* Add more delays as needed */
        
        .instruction-box {
            background-color: #f8f9fa;
            border-left: 4px solid #3498db;
            padding: 20px 25px;
            margin: 20px 0;
            border-radius: 5px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        
        .instruction-box h3 {
            color: #2c3e50;
            margin-bottom: 15px;
            font-size: 1.3em;
        }
        
        .instruction-box h4 {
            color: #3498db;
            margin: 20px 0 10px 0;
            font-size: 1.1em;
        }
        
        .instruction-box ol, .instruction-box ul {
            margin-left: 20px;
            color: #2c3e50;
        }
        
        .instruction-box li {
            margin: 8px 0;
            line-height: 1.5;
        }
        
        .instruction-box p {
            color: #2c3e50;
            line-height: 1.6;
        }
        
        .feature-box {
            background-color: #1e1e1e;
            border-left: 3px solid #3498db;
            padding: 15px;
            margin-bottom: 15px;
            border-radius: 5px;
        }
        
        .feature-number {
            color: #3498db;
            font-weight: bold;
            font-size: 1.1em;
            margin-right: 10px;
        }
        
        .feature-text {
            color: #ffffff;
            margin-top: 5px;
            font-size: 0.95em;
            line-height: 1.4;
        }
        
        /* Specific styling for ranking feature text to prevent color conflict */
        .ranking-feature-text {
            background-color: #f8f9fa;
            border-left: 4px solid #3498db;
            padding: 12px 15px;
            margin: 8px 0;
            border-radius: 4px;
            font-size: 15px;
            color: #2c3e50;
            line-height: 1.4;
        }
        
        /* Style the number input */
        div[data-testid="stNumberInput"] input {
            font-size: 16px;
            font-weight: bold;
            text-align: center;
        }
        
        /* Add space between ranking rows */
        .stForm > div > div > div {
            margin-bottom: 8px;
        }
        
        /* Custom styling for the Prolific ID input */
        [data-testid="stTextInput"] input {
            border: 1px solid #e0e0e0 !important;
            border-radius: 6px !important;
            padding: 12px 15px !important;
            font-size: 16px !important;
            transition: border-color 0.3s ease !important;
            background-color: #f9f9fa !important;
            color: #2c3e50 !important;  /* Adding dark text color for visibility */
        }
        [data-testid="stTextInput"] input::placeholder {
            color: #95a5a6 !important;  /* Adding placeholder color for better contrast */
            opacity: 1 !important;
        }
        [data-testid="stTextInput"] input:focus {
            border-color: #3498db !important;
            box-shadow: 0 0 0 1px #3498db !important;
        }
        /* Style the warning message */
        .stAlert > div {
            border-radius: 6px !important;
            padding: 10px 15px !important;
        }
        
        /* Style to identify our special text area */
        .no-paste-text-area textarea {
            border: 1px solid #e0e0e0 !important;
            border-radius: 8px !important;
            padding: 12px !important;
            font-size: 16px !important;
            background-color: #ffffff !important;
            color: #2c3e50 !important;
            height: 100px;
            width: 100%;
        }
        </style>
    """, unsafe_allow_html=True)

def display_story_with_animation(story_text, container):
    # Split story into lines
    lines = story_text.split('\n')
    story_html = ""
    
    for i, line in enumerate(lines):
        if line.strip():  # Only process non-empty lines
            # Convert markdown-style bold to HTML bold
            line = line.replace('**', '<strong>')  # First occurrence
            line = line.replace('**', '</strong>', 1)  # Second occurrence
            
            delay_class = f"delay-{i}"
            story_html += f'<div class="story-line {delay_class}">{line}</div>'
    
    container.markdown(
        f"""<div class="story-box">
            {story_html}
        </div>""",
        unsafe_allow_html=True
    )

def display_instructions():
    # Professional Prolific ID input with clean styling
    st.markdown("""
        <style>
        .prolific-container {
            background-color: #ffffff;
            border: 1px solid #e0e0e0;
            border-radius: 8px;
            padding: 20px;
            margin-bottom: 30px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        }
        .prolific-label {
            font-weight: 600;
            font-size: 16px;
            margin-bottom: 10px;
            color: #2c3e50;
            display: flex;
            align-items: center;
        }
        .required-asterisk {
            color: #e74c3c;
            font-weight: bold;
            font-size: 18px;
            margin-left: 4px;
        }
        .prolific-input {
            margin-top: 5px;
        }
        .prolific-note {
            font-size: 14px;
            color: #7f8c8d;
            margin-top: 8px;
            font-style: italic;
        }
        </style>
        <div class="prolific-container">
            <div class="prolific-label">
                Prolific ID <span class="required-asterisk">*</span>
            </div>
            <div class="prolific-note">Required for study participation</div>
        </div>
    """, unsafe_allow_html=True)
    
    # Get prolific_id from session state or initialize it
    prolific_id = st.session_state.get('prolific_id', '')
    
    # Add the input field within the custom container
    prolific_id = st.text_input(
        "",  # No label (we use the custom one above)
        key="prolific_id_input",
        placeholder="Enter your Prolific ID"
    )
    
    # Store in session state
    st.session_state.prolific_id = prolific_id
    
    # Simple validation message with cleaner styling
    if not prolific_id:
        st.warning("Please enter your Prolific ID to continue.")
    
    st.markdown("""
    ### About the Interactive Story Experience
    <div style='width: 100%; height: 3px; background: linear-gradient(to right, #3498db, #f8f9fa); margin: 10px 0 25px 0;'></div>
    
    You are participating in a research study about designing social proxy robots. These are physical robots that can represent you in remote locations, acting as your physical presence when you can't be there in person. For example, imagine a robot that could attend a work meeting on your behalf, moving, gesturing, and speaking as you have programmed it to.

    Through this study, you'll be transported to a near future where social proxy robots have become part of everyday life. Your journey will span 6 chapters, each exploring different aspects of robot-human interaction. As you suggest features for these robots, our AI storyteller will weave your ideas into engaging scenarios, showing how your design choices might play out in real situations.

    ### Your Task
    <div style='width: 100%; height: 2px; background: linear-gradient(to right, #3498db, transparent); margin: 10px 0 20px 0;'></div>
    
    1. You will progress through 6 chapters
    2. In each chapter:
       - Suggest a new features for the social proxy robot
       - Explain your reasoning behind this feature (why you think it's important)
    3. Review how your feature impacts the story
    4. You can revisit previous chapters to add more features
    5. The session will automatically complete after Chapter 6
    
    ### Guidelines
    <div style='width: 100%; height: 2px; background: linear-gradient(to right, #3498db, transparent); margin: 10px 0 20px 0;'></div>
    
    * When adding the features, include both WHAT and WHY:
      - What features you want to add
      - Why you think the features are important
    * There are no right or wrong answers - we're interested in your creative ideas
    * Consider both technical and social aspects of the robot
    * Feel free to build upon previous features or address challenges that come up
    * You can navigate between chapters using the arrows at the top
    """, unsafe_allow_html=True)
    
    # Add space before the button
    st.markdown("<div style='margin: 30px 0;'></div>", unsafe_allow_html=True)
    
    # Center the start button using columns
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        # Only enable the button if Prolific ID is provided
        if prolific_id:
            start_button = st.button("Start Experience", use_container_width=True, type="primary")
            if start_button:
                # Show loading progress bar while initializing - use a simpler approach
                st.markdown("<p style='text-align:center; color:#3498db;'>Initializing your experience...</p>", unsafe_allow_html=True)
                progress_bar = st.progress(0)
                
                # Use fewer steps to reduce potential for ElementNode errors
                for percent_complete in [0, 25, 50, 75, 100]:
                    progress_bar.progress(percent_complete)
                    time.sleep(0.2)  # Slower updates are less likely to cause rendering issues
                
                # Store Prolific ID in session state
                st.session_state.prolific_id = prolific_id
                return True
        else:
            # Disabled button (for visual consistency)
            st.button("Start Experience", use_container_width=True, type="primary", disabled=True)
    
    return False

def end_session():
    """Handle end of session and save data"""
    try:
        # Save session data first
        session_saved = st.session_state.story_manager.save_session()
        
        # Clear the screen by setting session state
        st.session_state.ended = True
        st.session_state.save_status = session_saved  # Track save status
        st.rerun()
        
    except Exception as e:
        st.error(f"Error saving session data: {str(e)}")

def main():
    st.set_page_config(
        page_title="Interactive Social Proxy Story Generator",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    st.markdown("""
        <link href="https://fonts.googleapis.com/css2?family=Crimson+Text:ital,wght@0,400;0,600;1,400&display=swap" rel="stylesheet">
    """, unsafe_allow_html=True)
    
    set_custom_style()
    
    # Initialize new session state every time
    if 'story_manager' not in st.session_state or not st.session_state.get('started', False):
        st.session_state.started = False
        st.session_state.initialized = False
        st.session_state.story_manager = StoryManager()
        st.session_state.client = Swarm()
        # Unpack all 4 agents
        st.session_state.agent_a, st.session_state.agent_b, st.session_state.agent_d, st.session_state.agent_intro = create_agents()
        st.session_state.input_key = 0
        st.session_state.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Sidebar content - show this regardless of started state
    with st.sidebar:
        st.image("https://img.icons8.com/color/96/000000/robot-2.png", width=100)
        
        # Only show Quick Tips
        st.markdown("""
        <div style='background-color: #1a1a1a; padding: 20px; border-radius: 10px;'>
            <h3 style='color: #3498db; margin-bottom: 10px;'>Quick Tips</h3>
            <ul style='color: #ffffff; list-style-type: none; padding-left: 0;'>
                <li style='margin-bottom: 10px;'>💡 Be specific about your features and reasoning</li>
                <li style='margin-bottom: 10px;'>🔄 Build on previous stories</li>
                <li style='margin-bottom: 10px;'>🎯 Focus on one feature at a time</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Main content
    st.markdown("<h1 style='text-align: center; color: #1f77b4;'>Interactive Social Proxy Story Generator</h1>", unsafe_allow_html=True)
    
    # Check if session has ended
    if st.session_state.get('ended', False):
        # Clean, centered layout
        st.markdown("""
            <style>
            .session-complete {
                text-align: center;
                max-width: 800px;
                margin: 0 auto;
                padding: 20px;
            }
            .completion-code {
                background-color: #f5f5f5;
                border: 1px solid #e0e0e0;
                border-radius: 5px;
                padding: 15px;
                margin: 20px auto;
                font-size: 18px;
                font-weight: bold;
                max-width: 400px;
            }
            .feature-card {
                background-color: #f8f9fa;
                border-left: 4px solid #3498db;
                padding: 12px 15px;
                margin: 8px 0;
                border-radius: 4px;
                cursor: grab;
                transition: all 0.2s ease;
            }
            .feature-card:hover {
                box-shadow: 0 2px 5px rgba(0,0,0,0.1);
                transform: translateX(3px);
            }
            .rank-instructions {
                background-color: #f9f9f9;
                padding: 15px;
                border-radius: 5px;
                margin: 20px 0;
                text-align: left;
                color: #2c3e50;
            }
            .rank-instructions p {
                color: #2c3e50 !important;
                margin-bottom: 10px;
            }
            .ranking-container {
                margin: 20px 0;
            }
            </style>
        """, unsafe_allow_html=True)
        
        st.markdown("<div class='session-complete'>", unsafe_allow_html=True)
        
        # Get all features from the session
        if st.session_state.story_manager.user_prompts and st.session_state.get('save_status', False):
            st.markdown("<h2>Rank Your Features</h2>", unsafe_allow_html=True)
            
            st.markdown("""
            <div class="rank-instructions">
                <p>Please rank your features from most valuable (1) to least valuable.</p>
                <p>Consider which features you think would be most important for a social proxy robot.</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Create a list of features for ranking
            features = [prompt['prompt'] for prompt in st.session_state.story_manager.user_prompts]
            
            # Use session state to maintain rankings between reruns
            if 'feature_rankings' not in st.session_state:
                st.session_state.feature_rankings = list(range(1, len(features) + 1))
            
            # Create a simple ranking interface with number inputs
            ranking_data = []
            
            st.markdown("<div class='ranking-container'>", unsafe_allow_html=True)
            
            # Create a form for rankings to avoid auto-rerun issues
            with st.form("ranking_form"):
                for i, feature in enumerate(features):
                    col1, col2 = st.columns([1, 4])
                    with col1:
                        rank = st.number_input(
                            f"Rank", 
                            min_value=1, 
                            max_value=len(features),
                            value=st.session_state.feature_rankings[i] if i < len(st.session_state.feature_rankings) else i+1,
                            key=f"rank_{i}"
                        )
                    with col2:
                        st.markdown(f"<div class='ranking-feature-text'>{feature}</div>", unsafe_allow_html=True)
                    
                    ranking_data.append({"feature": feature, "rank": rank})
                
                # Save rankings button inside form
                submit_button = st.form_submit_button("Save Rankings", type="primary")
                
            if submit_button:
                # Get the ranks assigned to each feature
                ranks = [item["rank"] for item in ranking_data]
                
                # Check if there are duplicate ranks
                if len(set(ranks)) != len(ranks):
                    st.error("Please assign a unique rank to each feature (each feature must have a different rank number).")
                else:
                    # Update session state
                    st.session_state.feature_rankings = [item["rank"] for item in ranking_data]
                    
                    # Sort by rank for the final submission
                    final_rankings = sorted(ranking_data, key=lambda x: x["rank"])
                    
                    # Save rankings to session state for retrieval if needed
                    st.session_state.final_rankings = final_rankings
                    
                    # Attempt to save rankings
                    save_result = st.session_state.story_manager.save_feature_rankings(final_rankings)
                    
                    if save_result:
                        st.success("Rankings saved successfully!")
                        
                        # Log successful ranking submission
                        st.session_state.rankings_saved = True
                        
                        # Display completion code after rankings are saved
                        st.markdown("<h2>Study Complete</h2>", unsafe_allow_html=True)
                        st.markdown("<p>Thank you for participating in this study.</p>", unsafe_allow_html=True)
                        
                        # Verify all data has been saved successfully
                        st.markdown("""
                        <div style="background-color: #f0f9ff; border-left: 4px solid #3498db; padding: 15px; margin: 20px 0; border-radius: 4px;">
                            <h4 style="margin-top: 0; color: #2c3e50;">Data Summary</h4>
                            <p style="margin-bottom: 5px;"><strong>✓</strong> Session data saved</p>
                            <p style="margin-bottom: 5px;"><strong>✓</strong> Feature rankings saved</p>
                            <p style="margin-bottom: 0;"><strong>✓</strong> All data has been successfully recorded</p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Display completion code
                        st.markdown("<p>Please copy the completion code below and paste it in Prolific:</p>", unsafe_allow_html=True)
                        st.markdown("<div class='completion-code'>thankyoumelb</div>", unsafe_allow_html=True)
                    else:
                        st.error("There was an issue saving your rankings. Please try again or contact support.")
                        # Add retry button
                        if st.button("Retry Saving Rankings"):
                            # Attempt to save again
                            retry_save = st.session_state.story_manager.save_feature_rankings(final_rankings)
                            if retry_save:
                                st.success("Rankings saved successfully on retry!")
                                st.session_state.rankings_saved = True
                                st.rerun()
            
            st.markdown("</div>", unsafe_allow_html=True)
        else:
            # If no features or save failed, just show completion
            st.success("Session data successfully saved to database.")
            st.markdown("<h2>Study Complete</h2>", unsafe_allow_html=True)
            st.markdown("<p>Thank you for participating in this study.</p>", unsafe_allow_html=True)
            
            # Add data status information
            save_status = st.session_state.get('save_status', False)
            st.markdown(f"""
            <div style="background-color: {'#f0f9ff' if save_status else '#fff7f7'}; 
                        border-left: 4px solid {'#3498db' if save_status else '#e74c3c'}; 
                        padding: 15px; margin: 20px 0; border-radius: 4px;">
                <h4 style="margin-top: 0; color: #2c3e50;">Data Status</h4>
                <p style="margin-bottom: 5px;">
                    <strong>{'✓' if save_status else '✗'}</strong> Session data 
                    {'saved successfully' if save_status else 'could not be saved completely'}
                </p>
                <p style="margin-bottom: 0; font-size: 0.9em;">
                    {'' if save_status else 'Your submission has been recorded, but some data may be incomplete.'}
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            # Display completion code
            st.markdown("<p>Please copy the completion code below and paste it in Prolific:</p>", unsafe_allow_html=True)
            st.markdown("<div class='completion-code'>thankyoumelb</div>", unsafe_allow_html=True)
        
        # New session button
        st.markdown("<div style='margin-top: 40px;'>", unsafe_allow_html=True)
        if st.button("Start New Session", type="primary"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
        return
    
    # Generate background story
    if not st.session_state.started:
        if display_instructions():
            # Clear any existing session data
            st.session_state.story_manager = StoryManager()
            st.session_state.client = Swarm()
            st.session_state.agent_a, st.session_state.agent_b, st.session_state.agent_d, st.session_state.agent_intro = create_agents()
            st.session_state.input_key = 0
            
            # Generate intro story
            if not st.session_state.get('intro_story_generated'):
                # Show progress bar for intro story generation - simpler approach
                st.markdown("<p style='text-align:center; color:#3498db;'>Creating your opening story...</p>", unsafe_allow_html=True)
                progress_bar = st.progress(0)
                
                # Get random first dimension (25% progress)
                first_chapter = st.session_state.story_manager.get_random_uncovered_dimension()
                first_dimension = st.session_state.story_manager.get_actual_dimension(first_chapter)
                progress_bar.progress(25)
                time.sleep(0.1)  # Brief pause between updates
                
                # Get dimension information from Agent B (50% progress)
                response_b = st.session_state.client.run(
                    agent=st.session_state.agent_b,  # Agent B
                    messages=[{
                        "role": "system",
                        "content": f"""
                            Selected Dimension: {first_dimension}
                            Provide challenge information for creating an engaging story.
                        """
                    }]
                )
                progress_bar.progress(50)
                time.sleep(0.1)  # Brief pause between updates
                
                # Generate intro story with the challenge (75% progress)
                response_intro = st.session_state.client.run(
                    agent=st.session_state.agent_intro,  # Agent Intro (index 3 since we return intro_agent last)
                    messages=[{
                        "role": "system",
                        "content": f"""
                            Create an opening story that introduces social proxy robots.
                            Use these challenges as inspiration for your story:
                            {response_b.messages[-1]["content"]}
                        """
                    }]
                )
                progress_bar.progress(75)
                time.sleep(0.1)  # Brief pause between updates
                
                # Add the story and mark dimension as covered (100% progress)
                if "STORY:" in response_intro.messages[-1]["content"]:
                    story_text = response_intro.messages[-1]["content"].split("STORY:")[1].strip()
                    st.session_state.story_manager.add_story_segment(f"STORY: {story_text}")
                    st.session_state.story_manager.add_covered_dimension(first_chapter)
                    st.session_state.intro_story_generated = True
                
                # Complete the progress bar
                progress_bar.progress(100)
            
            # Set started state and rerun
            st.session_state.started = True
            st.session_state.initialized = True
            st.rerun()
        return

    # Only show the rest of the interface if started
    if st.session_state.started:
        # Initialize variables for interaction
        progress = st.session_state.story_manager.get_dimension_progress()
        
        # Create two columns
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Chapter Navigation
            nav_col1, nav_col2, nav_col3 = st.columns([1, 2, 1])
            
            # Get current chapter number and total chapters
            current_chapter = len(st.session_state.story_manager.covered_dimensions)
            total_chapters = len(st.session_state.story_manager.session_story)
            viewing_chapter = st.session_state.get('viewing_chapter', current_chapter)
            
            with nav_col1:
                if viewing_chapter > 1:  # Can go back if not at first chapter
                    if st.button("←"):
                        st.session_state.viewing_chapter = viewing_chapter - 1
                        st.rerun()
            
            with nav_col2:
                st.markdown(f"### Chapter {viewing_chapter}", unsafe_allow_html=True)
            
            with nav_col3:
                if viewing_chapter < total_chapters:  # Can go forward if not at last chapter
                    if st.button("→"):
                        st.session_state.viewing_chapter = viewing_chapter + 1
                        st.rerun()
            
            # Chapter Story Display
            if viewing_chapter > 0 and viewing_chapter <= total_chapters:
                story = st.session_state.story_manager.session_story[viewing_chapter - 1]['segment']
                display_story_with_animation(story, st)
            
            # Only show input section if we're on any chapter
            if viewing_chapter > 0:
                # Design input section
                st.markdown("<div class='header-style'>Design Input</div>", unsafe_allow_html=True)
                st.info(f"""
                **Before adding feature to Chapter {viewing_chapter}, please consider the following:**
                - How would you enhance the current functionality?
                - Why do you think this feature is important?
                
                
                **Example format:**
                - Add <FEATURE 1> because <REASON>
                - Add <FEATURE 2> because <REASON> and so on...
                
                **Please add more than one feature in the dialog box below.**

                """)
                
                # User input (without copy-paste warning)
                user_input = st.text_area(
                    "Enter your design idea:",
                    key=f"user_input_{st.session_state.input_key}_{viewing_chapter}",
                    height=100,
                    placeholder="Describe your design idea here..."
                )
                
                # Use Streamlit components.html for isolated JavaScript execution
                disable_paste_js = """
                <script>
                window.addEventListener('load', function() {
                    // Give Streamlit time to render
                    setTimeout(function() {
                        // Target only textareas
                        var textareas = parent.document.querySelectorAll('textarea');
                        textareas.forEach(function(textarea) {
                            // Disable paste
                            textarea.addEventListener('paste', function(e) {
                                e.preventDefault();
                                return false;
                            });
                            
                            // Disable cut
                            textarea.addEventListener('cut', function(e) {
                                e.preventDefault();
                                return false;
                            });
                            
                            // Disable keyboard shortcuts for paste (Ctrl+V)
                            textarea.addEventListener('keydown', function(e) {
                                if (e.ctrlKey && (e.key === 'v' || e.keyCode === 86)) {
                                    e.preventDefault();
                                    return false;
                                }
                            });
                            
                            // Disable context menu to prevent paste that way
                            textarea.addEventListener('contextmenu', function(e) {
                                e.preventDefault();
                                return false;
                            });
                        });
                    }, 1000);
                });
                </script>
                """
                
                # Use Streamlit's components.html for isolated JS execution
                import streamlit.components.v1 as components
                components.html(disable_paste_js, height=0)
                
                # Create columns for buttons - just one column for generate button
                generate_col1, generate_col2 = st.columns([1, 2])
                
                with generate_col1:
                    generate_button = st.button("🚀 Next Chapter", use_container_width=True)
                
                # Generate story logic here...
                if generate_button and user_input:
                    # Show progress bar with simpler implementation
                    st.markdown("<p style='text-align:center; color:#3498db;'>Generating your story...</p>", unsafe_allow_html=True)
                    progress_bar = st.progress(0)
                    
                    try:
                        # Add user prompt (25% progress)
                        st.session_state.story_manager.add_user_prompt(user_input)
                        progress_bar.progress(25)
                        time.sleep(0.1)  # Brief pause between updates
                        
                        # Use the dimension from the current viewing chapter
                        current_dimension = st.session_state.story_manager.get_actual_dimension(f"Chapter {viewing_chapter}")
                        
                        # Get dimension information from Agent B (50% progress)
                        response_b = st.session_state.client.run(
                            agent=st.session_state.agent_b,
                            messages=[{
                                "role": "system",
                                "content": f"""
                                    Selected Dimension: {current_dimension}
                                    Provide challenge information for creating an engaging story.
                                """
                            }]
                        )
                        progress_bar.progress(50)
                        time.sleep(0.1)  # Brief pause between updates
                        
                        # Pass user input and dimension info to Agent D (75% progress)
                        response_d = st.session_state.client.run(
                            agent=st.session_state.agent_d,
                            messages=[{
                                "role": "system",
                                "content": f"""
                                    New Feature: {user_input}
                                    
                                    Use these challenges as inspiration for your story:
                                    {response_b.messages[-1]["content"]}
                                    
                                """
                            }]
                        )
                        progress_bar.progress(75)
                        time.sleep(0.1)  # Brief pause between updates
                        
                        # Update story (100% progress)
                        if "STORY:" in response_d.messages[-1]["content"]:
                            story_text = response_d.messages[-1]["content"].split("STORY:")[1].strip()
                            
                            # If adding to a previous chapter, update that chapter's story
                            if viewing_chapter < current_chapter:
                                # Update the specific chapter's story
                                st.session_state.story_manager.update_chapter_story(
                                    viewing_chapter, 
                                    f"STORY: {story_text}"
                                )
                                # Keep the user on the same chapter
                                st.session_state.viewing_chapter = viewing_chapter
                            else:
                                # Adding to current chapter, create new chapter as before
                                st.session_state.story_manager.current_story = story_text
                                st.session_state.story_manager.add_story_segment(response_d.messages[-1]["content"])
                                st.session_state.story_manager.add_covered_dimension(viewing_chapter)
                                # Move to next chapter only when adding to current chapter
                                st.session_state.viewing_chapter = len(st.session_state.story_manager.session_story)
                            
                            # Complete the progress bar
                            progress_bar.progress(100)
                            
                            st.success("✨ Story generated successfully!")
                            
                            # Check if this was Chapter 6
                            if viewing_chapter == 6:
                                # End session automatically
                                end_session()
                                st.rerun()
                        
                        else:
                            st.error(f"Failed to generate a valid story. Response received: {response_d.messages[-1]['content']}")
                        
                        # Force a rerun to update the display
                        st.rerun()
                        
                        # Save session and increment input key
                        st.session_state.story_manager.save_session()
                        st.session_state.input_key += 1
                        
                    except Exception as e:
                        st.error(f"Error generating story: {str(e)}")

            # Add divider after story generation
            st.markdown("""
            <div style='margin: 20px 0; height: 2px; background: linear-gradient(to right, #3498db, transparent);'></div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown("<div class='header-style'>Feature History</div>", unsafe_allow_html=True)
            
            show_history = st.toggle("Show Previous Features", value=True)
            
            if show_history and st.session_state.story_manager.user_prompts:
                # Create a numbered list of all prompts
                for i, prompt_data in enumerate(st.session_state.story_manager.user_prompts, 1):
                    prompt = prompt_data['prompt']
                    st.markdown(
                        f"""<div class='feature-box'>
                            <span class='feature-number'>#{i}</span>
                            <div class='feature-text'>{prompt}</div>
                        </div>""", 
                        unsafe_allow_html=True
                    )

if __name__ == "__main__":
    main() 