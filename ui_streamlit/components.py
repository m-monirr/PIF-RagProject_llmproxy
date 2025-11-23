"""
Streamlit UI Components for PIF RAG Chat
"""

import streamlit as st
from .styles import get_saudi_colors

def render_header():
    """Render the application header"""
    st.markdown("""
    <div style="text-align: center; padding: 20px 0;">
        <h1 style="color: #006C35; font-size: 2.5rem; margin: 0;">
            🇸🇦 PIF RAG Chat
        </h1>
        <p style="color: #666; font-size: 1.1rem; margin: 8px 0 0 0;">
            Powered by AI | Ask About Saudi Investments
        </p>
    </div>
    """, unsafe_allow_html=True)

def render_hero_section():
    """Render the hero section with stats"""
    
    st.markdown("""
    <div class="hero-title">
        Pioneering investments send ripples of real impact through Saudi Arabia and the world
    </div>
    <div class="hero-subtitle">
        Ask any question about PIF annual reports and get instant answers powered by AI
    </div>
    """, unsafe_allow_html=True)
    
    # Stats cards
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="stat-card">
            <div style="font-size: 2.5rem;">💰</div>
            <div class="stat-value">925BN+ USD</div>
            <div class="stat-label">Assets Under Management</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="stat-card">
            <div style="font-size: 2.5rem;">👥</div>
            <div class="stat-value">1.1+ Million</div>
            <div class="stat-label">Direct & Indirect Jobs</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="stat-card">
            <div style="font-size: 2.5rem;">🏢</div>
            <div class="stat-value">220+</div>
            <div class="stat-label">Portfolio Companies</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)

def render_sidebar():
    """Render the sidebar with controls"""
    
    st.markdown("### ⚙️ Settings")
    
    # Debug mode toggle
    st.session_state.debug_mode = st.toggle(
        "🐛 Debug Mode",
        value=st.session_state.debug_mode,
        help="Show source information and confidence scores"
    )
    
    # Clear chat button
    if st.button("🔄 Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.session_state.user_name = None
        st.session_state.chat_initialized = False
        st.rerun()
    
    st.markdown("---")
    
    # Tips section
    with st.expander("💡 Tips for Better Answers"):
        st.markdown("""
        **Be Specific**: Instead of "What is PIF?", try "What are PIF's main investment sectors?"
        
        **Use Keywords**: Include terms like:
        - Investment, portfolio, assets
        - NEOM, Vision 2030, projects
        - Financial, revenue, performance
        
        **Ask Follow-ups**: Click suggested questions
        
        **Try Both Languages**: Arabic and English supported
        """)
    
    st.markdown("---")
    
    # Stats
    st.markdown("### 📊 Chat Statistics")
    st.metric("Messages", len(st.session_state.messages))
    if st.session_state.user_name:
        st.info(f"👤 User: {st.session_state.user_name}")
    
    st.markdown("---")
    
    # About
    with st.expander("ℹ️ About"):
        st.markdown("""
        **PIF RAG Chat** uses:
        - 🧠 Ollama Cloud for LLM
        - 🔍 Qdrant for vector search
        - 📚 3 years of PIF reports (2021-2023)
        - 🌐 Bilingual support (EN/AR)
        """)

def render_chat_input():
    """Render the chat input area"""
    
    # Determine placeholder based on initialization
    if st.session_state.user_name is None:
        placeholder = "What's your name?"
    else:
        placeholder = "Ask about PIF investments..."
    
    # Chat input
    user_input = st.chat_input(placeholder)
    
    if user_input:
        from app import handle_user_input
        handle_user_input(user_input)

def render_follow_up_buttons(follow_ups, message_idx):
    """Render follow-up question buttons"""
    
    if not follow_ups:
        return
    
    st.markdown("<div style='margin-top: 12px;'>", unsafe_allow_html=True)
    
    cols = st.columns(len(follow_ups))
    for idx, follow_up in enumerate(follow_ups):
        with cols[idx]:
            if st.button(
                follow_up,
                key=f"follow_up_{message_idx}_{idx}",
                use_container_width=True
            ):
                from app import handle_user_input
                handle_user_input(follow_up)
    
    st.markdown("</div>", unsafe_allow_html=True)
