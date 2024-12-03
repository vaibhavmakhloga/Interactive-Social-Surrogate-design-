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
        
        # Generate initial background story automatically
        with st.spinner("🤖 Generating background story..."):
            initial_prompt = """Generate a brief, engaging background story (around 70 words) that explains what an Interactive Social Surrogate robot is, 
            its purpose in society, and how it helps people connect in the future.It is basically an embodied agent / robot that can be used for social proxy.
            These robots will represent the user and act as their physical presence in the world where they cannot be present. Focus on the human aspect and real-world applications.
            End with a statement like how would you design such a robot? or something similar and interesting."""
            
            agent_b = st.session_state.agents[1]  # Using storytelling agent
            
            response = st.session_state.client.run(
                agent=agent_b,
                messages=[{"role": "user", "content": initial_prompt}]
            )
            
            background_story = response.messages[-1]["content"]
            st.session_state.story_manager.add_story_segment(background_story)
    
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
            
            # Add visual separator after the first story
            if len(st.session_state.story_manager.session_story) == 1:
                st.markdown("<hr style='border-top: 2px dashed #3498db; margin: 20px 0;'>", unsafe_allow_html=True)
            
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