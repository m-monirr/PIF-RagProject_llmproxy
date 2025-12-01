"""
PIF RAG Chat - Streamlit Application
Clean, modular interface using ui_streamlit package
"""

import streamlit as st
from ui_streamlit.styles import apply_custom_css
from ui_streamlit.components import (
    render_sidebar,
    render_landing_page,
    render_chat_interface
)
from ui_streamlit.utils import (
    extract_name_from_input,
    validate_question_input,
    generate_follow_up_questions,
    handle_user_input
)

# Page configuration
st.set_page_config(
    page_title="PIF RAG Chat",
    page_icon="🇸🇦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply custom styling
apply_custom_css()

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'user_name' not in st.session_state:
    st.session_state.user_name = None
if 'debug_mode' not in st.session_state:
    st.session_state.debug_mode = False
if 'show_chat' not in st.session_state:
    st.session_state.show_chat = False
if 'last_streamed_idx' not in st.session_state:
    st.session_state.last_streamed_idx = -1
if 'show_tips' not in st.session_state:
    st.session_state.show_tips = False

def main():
    """Main application entry point"""
    
    # Render sidebar (always visible)
    render_sidebar()
    
    # Render appropriate page
    if not st.session_state.show_chat:
        render_landing_page()
    else:
        render_chat_interface()

if __name__ == "__main__":
    main()