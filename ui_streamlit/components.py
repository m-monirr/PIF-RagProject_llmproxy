"""
Streamlit UI Components for PIF RAG Chat
All reusable UI components in one place
"""

import streamlit as st

# PIF Logo URL
PIF_LOGO_URL = "https://cdn.brandfetch.io/idnYHC3i7K/theme/dark/logo.svg?c=1bxid64Mup7aczewSAYMX&t=1754092788470"

def render_sidebar():
    """Render the modern sidebar with all controls"""
    
    with st.sidebar:
        # Logo and branding
        st.markdown(f'''
        <div style="text-align: center; padding: 20px 0;">
            <img src="{PIF_LOGO_URL}" style="width: 140px; filter: brightness(1.5); margin-bottom: 12px;">
            <h3 style="margin: 0; font-size: 1.1rem; font-weight: 600;">PIF Chat Assistant</h3>
            <p style="margin: 4px 0 0 0; font-size: 0.85rem; opacity: 0.9;">Powered by AI</p>
        </div>
        ''', unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Navigation Section (only in chat mode)
        if st.session_state.show_chat:
            st.markdown("## 🧭 Navigation")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("🏠 Home", use_container_width=True, key="sidebar_home"):
                    st.session_state.show_chat = False
                    st.rerun()
            
            with col2:
                if st.button("🔄 Restart", use_container_width=True, key="sidebar_restart"):
                    st.session_state.messages = []
                    st.session_state.user_name = None
                    st.session_state.last_streamed_idx = -1
                    st.rerun()
            
            if st.button("🗑️ Clear All", use_container_width=True, type="secondary", key="sidebar_clear"):
                st.session_state.messages = []
                st.session_state.user_name = None
                st.session_state.last_streamed_idx = -1
                st.session_state.show_chat = False
                st.rerun()
            
            st.markdown("---")
        
        # Settings Section
        st.markdown("## ⚙️ Settings")
        
        # Debug Mode Toggle
        st.session_state.debug_mode = st.checkbox(
            "🐛 Debug Mode",
            value=st.session_state.debug_mode,
            help="Show source information and confidence scores",
            key="debug_toggle"
        )
        
        # Advanced Settings Expander
        with st.expander("🔧 Advanced Options", expanded=False):
            st.markdown("**Response Settings**")
            
            temperature = st.slider(
                "Creativity Level",
                min_value=0.0,
                max_value=1.0,
                value=0.3,
                step=0.1,
                help="Higher values make responses more creative"
            )
            
            max_tokens = st.slider(
                "Response Length",
                min_value=100,
                max_value=1000,
                value=500,
                step=50,
                help="Maximum length of responses"
            )
            
            st.markdown("---")
            st.markdown("**Search Settings**")
            
            num_sources = st.slider(
                "Number of Sources",
                min_value=1,
                max_value=10,
                value=5,
                step=1,
                help="How many sources to retrieve"
            )
        
        st.markdown("---")
        
        # Statistics Section
        st.markdown("## 📊 Statistics")
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric(
                "Messages",
                len(st.session_state.messages),
                delta=None
            )
        
        with col2:
            st.metric(
                "Session",
                "Active" if st.session_state.show_chat else "Idle",
                delta=None
            )
        
        if st.session_state.user_name:
            st.success(f"👤 {st.session_state.user_name}")
        
        st.markdown("---")
        
        # Tips Section
        with st.expander("💡 Tips for Better Results", expanded=False):
            st.markdown("""
            **Ask Specific Questions:**
            - ✅ "PIF's investment in NEOM 2023"
            - ✅ "Job creation statistics for 2022"
            - ❌ "Tell me about PIF" (too broad)
            
            **Use Keywords:**
            - Investment, portfolio, sectors
            - NEOM, Vision 2030
            - Financial, revenue, jobs
            
            **Supported Languages:**
            - 🇬🇧 English
            - 🇸🇦 Arabic (العربية)
            
            **Year-Specific Queries:**
            - Mention years: 2021, 2022, 2023
            - Compare across years
            """)
        
        # About Section
        with st.expander("ℹ️ About", expanded=False):
            st.markdown("""
            **PIF RAG Chat v2.0**
            
            AI-powered assistant for exploring Saudi Arabia's Public Investment Fund annual reports.
            
            **Data Sources:**
            - PIF Annual Report 2021
            - PIF Annual Report 2022
            - PIF Annual Report 2023
            
            **Technology:**
            - Semantic Search (RAG)
            - Multi-Provider LLM
            - Vector Database (Qdrant)
            
            **Models:**
            - Embeddings: Qwen3
            - Generation: Groq/Ollama Cloud
            """)
        
        # Footer
        st.markdown("---")
        st.markdown(
            '<div style="text-align: center; font-size: 0.8rem; opacity: 0.7;">'
            '© 2024 PIF RAG Chat<br>'
            'Built with ❤️ using Streamlit'
            '</div>',
            unsafe_allow_html=True
        )

def render_landing_page():
    """Render the landing page with hero section, stats, and features"""
    
    st.markdown(f'<div class="logo-container"><img src="{PIF_LOGO_URL}" alt="PIF Logo"></div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-title">Pioneering Investments Send Ripples of Real Impact</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-subtitle">💬 Ask any question about PIF annual reports and get instant AI-powered answers</div>', unsafe_allow_html=True)
    
    # Stats Cards
    st.markdown("""
    <div class="stats-row">
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
    <div class="features-grid">
        <div class="feature-card">
            <div class="feature-icon">🔍</div>
            <div class="feature-title">Semantic Search</div>
            <div class="feature-desc">Advanced AI-powered search across 3 years of PIF reports</div>
        </div>
        <div class="feature-card">
            <div class="feature-icon">🌐</div>
            <div class="feature-title">Bilingual Support</div>
            <div class="feature-desc">Ask questions in English or Arabic</div>
        </div>
        <div class="feature-card">
            <div class="feature-icon">⚡</div>
            <div class="feature-title">Instant Answers</div>
            <div class="feature-desc">Get comprehensive answers with source attribution</div>
        </div>
        <div class="feature-card">
            <div class="feature-icon">🤖</div>
            <div class="feature-title">AI-Powered</div>
            <div class="feature-desc">Powered by Ollama Cloud with auto-fallback</div>
        </div>
        <div class="feature-card">
            <div class="feature-icon">💡</div>
            <div class="feature-title">Smart Follow-ups</div>
            <div class="feature-desc">Contextual suggestions for deeper exploration</div>
        </div>
        <div class="feature-card">
            <div class="feature-icon">📊</div>
            <div class="feature-title">Multi-Year Data</div>
            <div class="feature-desc">Search across 2021, 2022, and 2023 reports</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("💬 Start Chatting", type="primary", use_container_width=True):
            st.session_state.show_chat = True
            st.rerun()

def render_chat_interface():
    """Render the chat interface with messages and input"""
    
    # Chat header
    st.markdown(f'<div class="logo-container"><img src="{PIF_LOGO_URL}" alt="PIF Logo" style="width: 150px;"></div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-title" style="font-size: 2rem; margin-bottom: 30px;">PIF Chat Assistant</div>', unsafe_allow_html=True)
    
    # Display all messages
    render_chat_messages()
    
    # Chat input
    render_chat_input()

def render_chat_messages():
    """Render all chat messages with streaming support"""
    
    for idx, msg in enumerate(st.session_state.messages):
        with st.chat_message(msg["role"], avatar="🇸🇦" if msg["role"] == "assistant" else "👤"):
            should_stream = (
                msg["role"] == "assistant" and 
                idx == len(st.session_state.messages) - 1 and 
                idx > st.session_state.last_streamed_idx
            )
            
            if should_stream:
                from .utils import stream_text_output
                placeholder = st.empty()
                stream_text_output(placeholder, msg["content"])
                st.session_state.last_streamed_idx = idx
            else:
                st.markdown(msg["content"])
            
            # Copy button for assistant messages
            if msg["role"] == "assistant":
                if st.button("📋 Copy", key=f"copy_msg_{idx}", help="Copy to clipboard"):
                    st.code(msg["content"], language="markdown")
                    st.toast("✅ Message ready to copy!", icon="📋")
            
            # Render follow-up buttons
            if 'follow_ups' in msg and msg['follow_ups']:
                cols = st.columns(len(msg['follow_ups']))
                for i, follow_up in enumerate(msg['follow_ups']):
                    with cols[i]:
                        if st.button(follow_up, key=f"followup_{idx}_{i}", use_container_width=True):
                            from .utils import handle_user_input
                            handle_user_input(follow_up)

def render_chat_input():
    """Render chat input field"""
    
    placeholder = "What's your name?" if not st.session_state.user_name else "Ask about PIF investments..."
    
    if prompt := st.chat_input(placeholder):
        from .utils import handle_user_input
        handle_user_input(prompt)
