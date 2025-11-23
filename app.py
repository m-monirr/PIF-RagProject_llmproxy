"""
PIF RAG Chat - Streamlit Application
Modern, production-ready interface for PIF annual reports Q&A
"""

import streamlit as st
from streamlit_chat import message
import time
from api_code.rag_query import get_rag_answer, get_rag_answer_with_sources
from ui_streamlit.styles import apply_custom_css, get_saudi_colors
from ui_streamlit.components import (
    render_header,
    render_hero_section,
    render_chat_input,
    render_sidebar,
    render_follow_up_buttons
)
from ui_streamlit.utils import (
    extract_name_from_input,
    generate_follow_up_questions,
    validate_question_input
)

# Page configuration
st.set_page_config(
    page_title="PIF RAG Chat – Ask About Saudi Investments",
    page_icon="🇸🇦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply custom CSS
apply_custom_css()

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'user_name' not in st.session_state:
    st.session_state.user_name = None
if 'debug_mode' not in st.session_state:
    st.session_state.debug_mode = False
if 'chat_initialized' not in st.session_state:
    st.session_state.chat_initialized = False

def main():
    """Main application"""
    
    # Render header
    render_header()
    
    # Sidebar
    with st.sidebar:
        render_sidebar()
    
    # Hero section (only if chat not initialized)
    if not st.session_state.chat_initialized:
        render_hero_section()
    
    # Chat container
    chat_container = st.container()
    
    with chat_container:
        # Display chat messages
        for idx, msg in enumerate(st.session_state.messages):
            if msg['role'] == 'user':
                message(msg['content'], is_user=True, key=f"user_{idx}")
            else:
                message(msg['content'], is_user=False, key=f"assistant_{idx}")
                
                # Show follow-up buttons after assistant messages
                if 'follow_ups' in msg and msg['follow_ups']:
                    render_follow_up_buttons(msg['follow_ups'], idx)
    
    # Chat input at the bottom
    render_chat_input()

def handle_user_input(user_input):
    """Process user input and generate response"""
    
    # First interaction - get name
    if st.session_state.user_name is None:
        st.session_state.user_name = extract_name_from_input(user_input)
        st.session_state.chat_initialized = True
        
        # Add user message
        st.session_state.messages.append({
            'role': 'user',
            'content': user_input
        })
        
        # Add welcome message
        welcome_msg = f"🎉 Wonderful to meet you, {st.session_state.user_name}! I'm excited to help you explore PIF's amazing world of investments.\n\n" \
                     f"What would you like to know about today? I can tell you about:\n\n" \
                     f"• 💰 Investment strategies and portfolio performance\n" \
                     f"• 🏗️ Vision 2030 projects like NEOM\n" \
                     f"• 📊 Financial achievements and targets\n" \
                     f"• 🌱 Sustainability initiatives\n" \
                     f"• 🚀 Technology and innovation investments\n\n" \
                     f"Just ask me anything!"
        
        st.session_state.messages.append({
            'role': 'assistant',
            'content': welcome_msg,
            'follow_ups': []
        })
        
        st.rerun()
        return
    
    # Validate input
    is_valid, error_msg = validate_question_input(user_input)
    if not is_valid:
        st.error(error_msg)
        return
    
    # Add user message
    st.session_state.messages.append({
        'role': 'user',
        'content': user_input
    })
    
    # Show typing indicator
    with st.spinner('🔍 Searching PIF documents...'):
        try:
            # Get answer
            if st.session_state.debug_mode:
                rag_result = get_rag_answer_with_sources(user_input)
                answer = rag_result['answer']
                
                if rag_result['sources']:
                    debug_info = f"\n\n**🔍 Debug Info:**\n"
                    debug_info += f"• Found {len(rag_result['sources'])} relevant sources\n"
                    debug_info += f"• Confidence: {rag_result['confidence']:.2f}\n"
                    sources_str = ', '.join([f"{s['year']} (score: {s['score']:.2f})" for s in rag_result['sources']])
                    debug_info += f"• Sources: {sources_str}\n"
                    answer += debug_info
            else:
                answer = get_rag_answer(user_input)
            
            if not answer or answer.strip() == "":
                answer = "I apologize, but I couldn't find a specific answer to your question. Could you please rephrase your question or ask about a different aspect of PIF's investments?"
            
            # Generate follow-up questions
            follow_ups = generate_follow_up_questions(user_input, answer)
            
            # Add assistant message
            st.session_state.messages.append({
                'role': 'assistant',
                'content': answer,
                'follow_ups': follow_ups[:2]  # Limit to 2
            })
            
        except Exception as e:
            st.error(f"Error: {str(e)[:100]}")
            st.session_state.messages.append({
                'role': 'assistant',
                'content': f"I'm experiencing technical difficulties. Please try again.\n\n_Error: {str(e)[:100]}_",
                'follow_ups': []
            })
    
    st.rerun()

if __name__ == "__main__":
    main()
