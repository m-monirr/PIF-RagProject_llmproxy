"""
Streamlit UI Components for PIF RAG Chat with Floating Chat
"""

import streamlit as st

# PIF Logo URL
PIF_LOGO_URL = "https://cdn.brandfetch.io/idnYHC3i7K/theme/dark/logo.svg?c=1bxid64Mup7aczewSAYMX&t=1754092788470"

def render_main_page():
    """Render the main landing page"""
    
    # Hero Section
    st.markdown(f"""
    <div class="hero-section">
        <img src="{PIF_LOGO_URL}" class="hero-logo" alt="PIF Logo">
        
        <div class="hero-title">
            Pioneering Investments Send Ripples of Real Impact
        </div>
        
        <div class="hero-subtitle">
            💬 Ask any question about PIF annual reports and get instant AI-powered answers
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Stats Cards
    st.markdown("""
    <div class="stats-container">
        <div class="stat-card">
            <div class="stat-icon">💰</div>
            <div class="stat-value">925BN+ USD</div>
            <div class="stat-label">Assets Under Management</div>
        </div>
        
        <div class="stat-card">
            <div class="stat-icon">👥</div>
            <div class="stat-value">1.1+ Million</div>
            <div class="stat-label">Direct & Indirect Jobs</div>
        </div>
        
        <div class="stat-card">
            <div class="stat-icon">🏢</div>
            <div class="stat-value">220+</div>
            <div class="stat-label">Portfolio Companies</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Features Section
    st.markdown("""
    <div class="features-container">
        <div class="feature-card">
            <div class="feature-icon">🔍</div>
            <div class="feature-title">Semantic Search</div>
            <div class="feature-desc">
                Advanced AI-powered search across 3 years of PIF annual reports
            </div>
        </div>
        
        <div class="feature-card">
            <div class="feature-icon">🌐</div>
            <div class="feature-title">Bilingual Support</div>
            <div class="feature-desc">
                Ask questions in English or Arabic and get accurate answers
            </div>
        </div>
        
        <div class="feature-card">
            <div class="feature-icon">⚡</div>
            <div class="feature-title">Instant Answers</div>
            <div class="feature-desc">
                Get comprehensive answers in seconds with source attribution
            </div>
        </div>
        
        <div class="feature-card">
            <div class="feature-icon">🤖</div>
            <div class="feature-title">AI-Powered</div>
            <div class="feature-desc">
                Powered by Ollama Cloud LLM with automatic fallback support
            </div>
        </div>
        
        <div class="feature-card">
            <div class="feature-icon">💡</div>
            <div class="feature-title">Smart Follow-ups</div>
            <div class="feature-desc">
                Contextual follow-up questions to explore topics deeper
            </div>
        </div>
        
        <div class="feature-card">
            <div class="feature-icon">📊</div>
            <div class="feature-title">Multi-Year Data</div>
            <div class="feature-desc">
                Search across reports from 2021, 2022, and 2023
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_floating_chat():
    """Render the floating chat interface"""
    
    # Chat toggle button
    if not st.session_state.chat_open:
        st.markdown(f"""
        <div class="chat-button" onclick="window.parent.postMessage({{type: 'streamlit:setComponentValue', value: 'toggle_chat'}}, '*')">
            <img src="{PIF_LOGO_URL}" alt="Chat">
        </div>
        """, unsafe_allow_html=True)
        
        # Use a button to trigger the toggle
        if st.button("", key="chat_toggle_btn", help="Open Chat", type="primary"):
            st.session_state.chat_open = True
            st.rerun()
    else:
        # Chat container
        st.markdown("""
        <div class="chat-container">
            <div class="chat-header">
                <div class="chat-header-title">
                    <img src="{}" alt="PIF">
                    <span>PIF Chat Assistant</span>
                </div>
            </div>
        </div>
        """.format(PIF_LOGO_URL), unsafe_allow_html=True)
        
        # Close button
        if st.button("✕", key="close_chat", help="Close Chat"):
            st.session_state.chat_open = False
            st.rerun()
        
        # Render chat messages
        render_chat_messages()
        
        # Chat input
        render_chat_input()

def render_chat_messages():
    """Render chat messages in the floating window"""
    
    # Welcome message if no messages
    if len(st.session_state.messages) == 0:
        st.markdown("""
        <div class="message-assistant">
            👋 Hello! I'm your PIF AI assistant. What's your name? 
            I'd love to personalize our conversation about PIF investments!
        </div>
        """, unsafe_allow_html=True)
        return
    
    # Render all messages
    for idx, msg in enumerate(st.session_state.messages):
        if msg['role'] == 'user':
            st.markdown(f"""
            <div class="message-user">
                {msg['content']}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="message-assistant">
                {msg['content']}
            </div>
            """, unsafe_allow_html=True)
            
            # Render follow-up buttons
            if 'follow_ups' in msg and msg['follow_ups']:
                cols = st.columns(len(msg['follow_ups']))
                for i, follow_up in enumerate(msg['follow_ups']):
                    with cols[i]:
                        if st.button(follow_up, key=f"followup_{idx}_{i}", use_container_width=True):
                            from app import handle_user_input
                            handle_user_input(follow_up)

def render_chat_input():
    """Render chat input area"""
    
    # Determine placeholder
    if st.session_state.user_name is None:
        placeholder = "What's your name?"
    else:
        placeholder = "Ask about PIF investments..."
    
    # Chat input with form to prevent page reload
    with st.form(key="chat_form", clear_on_submit=True):
        user_input = st.text_input(
            "Message",
            placeholder=placeholder,
            label_visibility="collapsed",
            key="chat_input"
        )
        
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            submit = st.form_submit_button("Send 📤", use_container_width=True, type="primary")
        
        if submit and user_input:
            from app import handle_user_input
            handle_user_input(user_input)
    
    # Debug toggle
    with st.expander("⚙️ Settings"):
        st.session_state.debug_mode = st.checkbox(
            "🐛 Debug Mode",
            value=st.session_state.debug_mode,
            help="Show source information"
        )
        
        if st.button("🔄 Clear Chat", use_container_width=True):
            st.session_state.messages = []
            st.session_state.user_name = None
            st.rerun()
