import streamlit as st
from swarm import Swarm
from agents import create_agents
from story_manager import StoryManager
import pandas as pd

def set_custom_style():
    st.markdown("""
        <style>
        /* Modern, high-contrast theme */
        .stApp {
            max-width: 1400px;
            margin: 0 auto;
            background-color: #ffffff !important;
        }
        
        /* Story box with typewriter effect */
        .story-box {        
            background-color: #f8f9fa;
            border-radius: 12px;
            padding: 25px;
            margin: 15px 0;
            font-family: 'Inter', sans-serif;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            color: #2c3e50;
            font-size: 16px;
            line-height: 1.6;
            border-left: 5px solid #3498db;
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
        </style>
    """, unsafe_allow_html=True)

def end_session():
    """Handle end of session and display final summary"""
    st.markdown("<div class='header-style'>Session Complete</div>", unsafe_allow_html=True)
    
    # Display final story
    st.markdown("### 📖 Complete Story Generated")
    st.markdown(f"<div class='story-box'>{st.session_state.story_manager.get_complete_story()}</div>", 
               unsafe_allow_html=True)
    
    # Display session stats
    st.markdown("### 📊 Session Statistics")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Stories Generated", len(st.session_state.story_manager.session_story))
    with col2:
        st.metric("Parameters Identified", len(st.session_state.story_manager.parameter_history))
    
    # Show file saves
    json_file, csv_file = st.session_state.story_manager.save_session()
    st.success(f"Session data saved to:\n- {json_file}\n- {csv_file}")
    
    # Option for new session
    if st.button("Start New Session", type="primary"):
        # Reset session state
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

def display_story_with_animation(story_text, container):
    # Split story into lines
    lines = story_text.split('\n')
    story_html = ""
    
    for i, line in enumerate(lines):
        if line.strip():  # Only process non-empty lines
            delay_class = f"delay-{i}"
            story_html += f'<div class="story-line {delay_class}">{line}</div>'
    
    container.markdown(
        f"""<div class="story-box">
            {story_html}
        </div>""",
        unsafe_allow_html=True
    )

def main():
    st.set_page_config(
        page_title="Interactive Social Surrogate Story Generator",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    set_custom_style()
    
    # Initialize session state
    if 'story_manager' not in st.session_state:
        st.session_state.story_manager = StoryManager()
        st.session_state.client = Swarm()
        st.session_state.agents = create_agents()
        st.session_state.input_key = 0
    
    # Sidebar content
    with st.sidebar:
        st.image("https://img.icons8.com/color/96/000000/robot-2.png", width=100)
        
        # About section with bigger, white heading
        st.markdown("""
        <h1 style='color: white; font-size: 32px; margin-bottom: 20px; padding: 10px; background-color: #2c3e50; border-radius: 8px; text-align: center;'>
            About
        </h1>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style='background-color: #f8f9fa; padding: 20px; border-radius: 10px; margin-bottom: 20px; border-left: 4px solid #3498db;'>
            <p style='color: #2c3e50; font-size: 15px; line-height: 1.6;'>
                Design better social surrogate robots through interactive storytelling. Social surrogates are embodied robots that act as physical proxies, enabling remote users to maintain meaningful connections with family and friends through real-world interactions.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Session stats with matching style
        if 'story_manager' in st.session_state and st.session_state.story_manager.session_story:
            st.markdown("""
            <div style='background-color: #1a1a1a; padding: 20px; border-radius: 10px;'>
                <h3 style='color: #3498db; margin-bottom: 10px;'>Session Stats</h3>
                <ul style='color: #ffffff; list-style-type: none; padding-left: 0;'>
                    <li style='margin-bottom: 5px;'>📊 Stories Generated: {}</li>
                    <li style='margin-bottom: 5px;'>🎯 Parameters Identified: {}</li>
                </ul>
            </div>
            """.format(
                len(st.session_state.story_manager.session_story),
                len(st.session_state.story_manager.parameter_history)
            ), unsafe_allow_html=True)
    
    # Main content
    st.markdown("<h1 style='text-align: center; color: #1f77b4;'>Interactive Social Surrogate Story Generator</h1>", unsafe_allow_html=True)
    
    # Create two columns
    col1, col2 = st.columns([2, 1])
    
    with col1:
        if st.session_state.story_manager.current_story:
            st.markdown("<div class='header-style'>Story Progress</div>", unsafe_allow_html=True)
            display_story_with_animation(st.session_state.story_manager.current_story, st)
            
            st.markdown("<div class='header-style'>Design Input</div>", unsafe_allow_html=True)
            st.info("""
            Consider:
            - What new feature would you add?
            - How would you enhance existing functionality?
            - What aspect would you like to develop further?
            - Type 'exit' to end session
            """)
            user_input = st.text_area(
                "Enter your design idea:",
                key=f"user_input_{st.session_state.input_key}",
                height=100,
                placeholder="Describe your design idea here... (or type 'exit' to end session)"
            )
        else:
            st.markdown("<div class='header-style'>Initial Design Parameter</div>", unsafe_allow_html=True)
            st.info("Start by defining an important feature for the social surrogate robot.")
            st.markdown("*Example: 'It should maintain eye contact during conversations'*")
            user_input = st.text_area(
                "Enter feature:",
                key=f"user_input_{st.session_state.input_key}",
                height=100,
                placeholder="Describe the feature here... (or type 'exit' to end session)"
            )
        
        # Check for exit command
        if user_input and user_input.lower().strip() == 'exit':
            end_session()
            return
        
        generate_col1, generate_col2 = st.columns([1, 2])
        with generate_col1:
            generate_button = st.button("🚀 Generate Story", use_container_width=True)
    
    with col2:
        st.markdown("<div class='header-style'>Design Challenges</div>", unsafe_allow_html=True)
        
        show_challenges = st.toggle("Show Design Challenges", value=True)
        
        if show_challenges and st.session_state.story_manager.challenge_history:
            # Get only the most recent challenge
            latest_challenge = st.session_state.story_manager.challenge_history[-1]
            challenge_text = latest_challenge['challenge']
            
            # Display only the current challenge
            st.markdown(
                f"""<div class='challenge-box'>
                    {challenge_text}
                </div>""", 
                unsafe_allow_html=True
            )
        
        if st.session_state.story_manager.session_story:
            st.markdown("<hr>", unsafe_allow_html=True)
            show_story = st.toggle("Show Complete Story", value=True)
            
            if show_story:
                st.markdown("<div class='header-style'>Complete Story</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='story-box'>{st.session_state.story_manager.get_complete_story()}</div>", 
                          unsafe_allow_html=True)
    
    # Generate button logic
    if generate_button and user_input and user_input.lower().strip() != 'exit':
        with st.spinner("🤖 Generating story..."):
            agent_a, agent_b, agent_c = st.session_state.agents
            
            # Add user prompt
            st.session_state.story_manager.add_user_prompt(user_input)
            
            # Prepare message
            initial_message = {
                "role": "user",
                "content": user_input + (" [NEW STORY]" if not st.session_state.story_manager.current_story else " [CONTINUATION]")
            }
            
            if st.session_state.story_manager.current_story:
                initial_message["content"] += f"\n\nPrevious story:\n{st.session_state.story_manager.get_complete_story()}"
            
            # Run agents
            response_a = st.session_state.client.run(agent=agent_a, messages=[initial_message])
            parameter_info = response_a.messages[-1]["content"]
            st.session_state.story_manager.add_parameter(parameter_info)
            
            response_c = st.session_state.client.run(
                agent=agent_c,
                messages=[
                    initial_message,
                    {"role": "assistant", "content": parameter_info}
                ]
            )
            challenge_info = response_c.messages[-1]["content"]
            st.session_state.story_manager.add_challenge(challenge_info)
            
            response_b = st.session_state.client.run(
                agent=agent_b,
                messages=[
                    initial_message,
                    {"role": "system", "content": f"Parameter Info: {parameter_info}\nContext Info: {challenge_info}\nFull previous story: {st.session_state.story_manager.get_complete_story()}"}
                ]
            )
            
            # Update story
            st.session_state.story_manager.add_story_segment(response_b.messages[-1]["content"])
            
            # Save session after each generation
            json_file, csv_file = st.session_state.story_manager.save_session()
            st.success(f"Session logged successfully")
            
            # Show success message with animation
            success_placeholder = st.empty()
            success_placeholder.success("✨ Story generated successfully!")
            
            # Increment input key and rerun
            st.session_state.input_key += 1
            st.rerun()

if __name__ == "__main__":
    main() 