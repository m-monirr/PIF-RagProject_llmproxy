"""
PIF RAG Chat - Streamlit Application
Beautiful, responsive interface for PIF annual reports Q&A
"""

import streamlit as st
import time
import re
from api_code.rag_query import get_rag_answer, get_rag_answer_with_sources

# Page configuration
st.set_page_config(
    page_title="PIF RAG Chat",
    page_icon="🇸🇦",
    layout="wide",
    initial_sidebar_state="auto"
)

# PIF Logo URL
PIF_LOGO_URL = "https://cdn.brandfetch.io/idnYHC3i7K/theme/dark/logo.svg?c=1bxid64Mup7aczewSAYMX&t=1754092788470"

# Apply PIF-themed CSS (Black, Green, Gold)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;700&display=swap');
    
    * {
        font-family: 'Montserrat', sans-serif;
    }
    
    /* Main container - Black background */
    .main {
        background: linear-gradient(135deg, #0A0A0A 0%, #1A1A1A 100%);
        color: #FFFFFF;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display:none;}
    header {visibility: hidden;}
    
    /* Logo container */
    .logo-container {
        text-align: center;
        padding: 40px 0 20px 0;
    }
    
    .logo-container img {
        width: 200px;
        height: auto;
        filter: brightness(1.2);
    }
    
    /* Hero title - Gold */
    .hero-title {
        text-align: center;
        font-size: 2.5rem;
        font-weight: 700;
        color: #D4AF37;
        margin: 30px 0 15px 0;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.5);
    }
    
    .hero-subtitle {
        text-align: center;
        font-size: 1.2rem;
        color: #00A651;
        margin-bottom: 40px;
    }
    
    /* Stats container */
    .stats-row {
        display: flex;
        justify-content: center;
        gap: 30px;
        margin: 40px 0;
        flex-wrap: wrap;
    }
    
    .stat-card {
        background: linear-gradient(135deg, #1A1A1A 0%, #2A2A2A 100%);
        border: 2px solid #00A651;
        border-radius: 16px;
        padding: 30px;
        text-align: center;
        min-width: 250px;
        box-shadow: 0 8px 24px rgba(0, 166, 81, 0.2);
        transition: all 0.3s ease;
    }
    
    .stat-card:hover {
        transform: translateY(-10px);
        box-shadow: 0 16px 48px rgba(212, 175, 55, 0.3);
        border-color: #D4AF37;
    }
    
    .stat-icon {
        font-size: 3rem;
        margin-bottom: 15px;
    }
    
    .stat-value {
        font-size: 2.2rem;
        font-weight: 700;
        color: #D4AF37;
        margin: 10px 0;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.5);
    }
    
    .stat-label {
        font-size: 1rem;
        color: #CCCCCC;
    }
    
    /* Features grid */
    .features-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 25px;
        margin: 50px auto;
        max-width: 1200px;
        padding: 0 20px;
    }
    
    .feature-card {
        background: linear-gradient(135deg, #1A1A1A 0%, #2A2A2A 100%);
        border: 1px solid #00A651;
        border-radius: 16px;
        padding: 30px;
        box-shadow: 0 4px 16px rgba(0, 166, 81, 0.15);
        transition: all 0.3s ease;
    }
    
    .feature-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 12px 32px rgba(212, 175, 55, 0.25);
        border-color: #D4AF37;
    }
    
    .feature-icon {
        font-size: 2.5rem;
        margin-bottom: 15px;
    }
    
    .feature-title {
        font-size: 1.2rem;
        font-weight: 600;
        color: #D4AF37;
        margin-bottom: 10px;
    }
    
    .feature-desc {
        color: #CCCCCC;
        line-height: 1.6;
    }
    
    /* Floating action buttons - Fixed position */
    .floating-buttons {
        position: fixed;
        top: 20px;
        right: 20px;
        z-index: 1000;
        display: flex;
        gap: 10px;
    }
    
    .floating-btn {
        background: linear-gradient(135deg, #00A651 0%, #007A3D 100%);
        color: white;
        border: 2px solid #D4AF37;
        border-radius: 50%;
        width: 60px;
        height: 60px;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        box-shadow: 0 4px 12px rgba(0, 166, 81, 0.4);
        transition: all 0.3s ease;
        font-size: 1.5rem;
    }
    
    .floating-btn:hover {
        transform: scale(1.1);
        box-shadow: 0 6px 20px rgba(212, 175, 55, 0.5);
        background: linear-gradient(135deg, #D4AF37 0%, #B8941F 100%);
    }
    
    /* Chat messages - Dark theme */
    .stChatMessage {
        border-radius: 12px;
        padding: 15px;
        margin: 10px 0;
        animation: slideIn 0.3s ease-out;
        background: #1A1A1A !important;
        border: 1px solid #00A651;
    }
    
    [data-testid="stChatMessage"][data-is-user="true"] {
        background: linear-gradient(135deg, #00A651 0%, #007A3D 100%) !important;
        color: white !important;
        border-color: #D4AF37;
    }
    
    [data-testid="stChatMessage"][data-is-user="false"] {
        background: #2A2A2A !important;
        color: #FFFFFF !important;
        border-color: #00A651;
    }
    
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateY(10px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    /* Sidebar - Green gradient */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #00A651 0%, #007A3D 100%);
    }
    
    [data-testid="stSidebar"] * {
        color: white !important;
    }
    
    /* Buttons - Gold accent */
    .stButton > button {
        background: linear-gradient(135deg, #D4AF37 0%, #B8941F 100%);
        color: #0A0A0A;
        font-weight: 600;
        border: none;
        border-radius: 12px;
        padding: 12px 24px;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(212, 175, 55, 0.4);
    }
    
    /* Input - Dark theme */
    .stTextInput > div > div > input,
    .stChatInput > div > div > input {
        background: #2A2A2A;
        color: white;
        border: 2px solid #00A651;
        border-radius: 12px;
    }
    
    .stTextInput > div > div > input:focus,
    .stChatInput > div > div > input:focus {
        border-color: #D4AF37;
        box-shadow: 0 0 0 3px rgba(212, 175, 55, 0.2);
    }
    
    /* Responsive */
    @media (max-width: 768px) {
        .hero-title {
            font-size: 1.8rem;
        }
        .hero-subtitle {
            font-size: 1rem;
        }
        .floating-buttons {
            top: 10px;
            right: 10px;
        }
        .floating-btn {
            width: 50px;
            height: 50px;
            font-size: 1.2rem;
        }
    }
</style>

<script>
// Enable clipboard copy functionality
function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(function() {
        console.log('Copied to clipboard successfully!');
    }, function(err) {
        console.error('Could not copy text: ', err);
    });
}
</script>
""", unsafe_allow_html=True)

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

# Helper functions
def extract_name_from_input(user_input):
    """Extract name from user input"""
    input_lower = user_input.lower().strip()
    
    greetings = ['hello', 'hi', 'hey', 'good morning', 'good afternoon', 'مرحبا', 'السلام عليكم', 'أهلا', 'صباح الخير']
    for greeting in greetings:
        if input_lower.startswith(greeting):
            input_lower = input_lower[len(greeting):].strip()
    
    phrases = ['my name is', 'i am', 'i\'m', 'اسمي', 'أنا']
    for phrase in phrases:
        if phrase in input_lower:
            input_lower = input_lower.replace(phrase, '').strip()
    
    name = ' '.join(input_lower.split())
    return name.title() if name else user_input.strip()

def validate_question_input(question):
    """Validate user question"""
    if not question:
        return False, 'Please enter a question!'
    if len(question) < 3:
        return False, 'Question too short! Please enter at least 3 characters.'
    if len(question) > 500:
        return False, 'Question too long! Please keep it under 500 characters.'
    return True, None

def generate_follow_up_questions(question, answer):
    """Generate contextual follow-up questions"""
    follow_ups = []
    arabic_pattern = re.compile(r'[\u0600-\u06FF]')
    is_arabic = bool(arabic_pattern.search(question))
    
    if is_arabic:
        if 'استثمار' in question or 'قطاع' in question:
            follow_ups.append('ما هي القطاعات الاستثمارية الأخرى؟')
            follow_ups.append('كم قيمة الاستثمارات الإجمالية؟')
        elif 'وظيفة' in question or 'وظائف' in question:
            follow_ups.append('ما هي مبادرات التوظيف الأخرى؟')
        elif 'نيوم' in question or 'NEOM' in question:
            follow_ups.append('ما هي مشاريع رؤية 2030 الأخرى؟')
    else:
        if 'investment' in question.lower() or 'sector' in question.lower():
            follow_ups.append('What other sectors does PIF invest in?')
            follow_ups.append('What is the total value of investments?')
        elif 'job' in question.lower():
            follow_ups.append('What are other job creation initiatives?')
        elif 'neom' in question.lower():
            follow_ups.append('What other Vision 2030 projects exist?')
        elif '2023' in question:
            follow_ups.append('How does this compare to 2022?')
    
    if not follow_ups:
        if is_arabic:
            follow_ups = ['أخبرني المزيد عن استراتيجية الصندوق', 'ما هي الإنجازات المالية الأخيرة؟']
        else:
            follow_ups = ['Tell me more about PIF\'s strategy', 'What are the recent financial achievements?']
    
    return follow_ups[:2]

def stream_text_output(placeholder, text):
    """Stream text word by word"""
    words = text.split()
    displayed_text = ""
    for word in words:
        displayed_text += word + " "
        placeholder.markdown(displayed_text + "▌")
        time.sleep(0.03)
    placeholder.markdown(displayed_text.strip())

def handle_user_input(user_input):
    """Process user input"""
    
    if st.session_state.user_name is None:
        st.session_state.user_name = extract_name_from_input(user_input)
        st.session_state.messages.append({'role': 'user', 'content': user_input})
        welcome_msg = f"🎉 Wonderful to meet you, **{st.session_state.user_name}**!\n\nI'm excited to help you explore PIF's investments.\n\n**What would you like to know?**\n\n• 💰 Investment strategies\n• 🏗️ Vision 2030 projects\n• 📊 Financial achievements\n• 🌱 Sustainability initiatives\n• 🚀 Technology investments"
        st.session_state.messages.append({'role': 'assistant', 'content': welcome_msg, 'follow_ups': []})
        st.rerun()
        return
    
    is_valid, error_msg = validate_question_input(user_input)
    if not is_valid:
        st.error(error_msg)
        return
    
    st.session_state.messages.append({'role': 'user', 'content': user_input})
    
    with st.spinner('🔍 Searching PIF documents...'):
        try:
            if st.session_state.debug_mode:
                rag_result = get_rag_answer_with_sources(user_input)
                answer = rag_result['answer']
                
                if rag_result['sources']:
                    debug_info = f"\n\n**🔍 Debug Info:**\n"
                    debug_info += f"• Sources: {len(rag_result['sources'])}\n"
                    debug_info += f"• Confidence: {rag_result['confidence']:.2f}\n"
                    sources_str = ', '.join([f"{s['year']} ({s['score']:.2f})" for s in rag_result['sources']])
                    debug_info += f"• Years: {sources_str}"
                    answer += debug_info
            else:
                answer = get_rag_answer(user_input)
            
            if not answer or answer.strip() == "":
                answer = "I couldn't find specific information. Please rephrase your question."
            
            follow_ups = generate_follow_up_questions(user_input, answer)
            st.session_state.messages.append({'role': 'assistant', 'content': answer, 'follow_ups': follow_ups[:2]})
        except Exception as e:
            st.session_state.messages.append({'role': 'assistant', 'content': f"Error: {str(e)[:100]}", 'follow_ups': []})
    
    st.rerun()

def main():
    """Main application"""
    
    # Floating action buttons (always visible in chat)
    if st.session_state.show_chat:
        st.markdown("""
        <div class="floating-buttons">
            <div class="floating-btn" title="Back to Home" id="back-home-btn">⬅️</div>
            <div class="floating-btn" title="Restart Chat" id="restart-chat-btn">🔄</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Handle floating button clicks with hidden buttons
        col_back, col_restart = st.columns(2)
        with col_back:
            if st.button("", key="floating_back", help="Back to Home", type="secondary"):
                st.session_state.show_chat = False
                st.rerun()
        with col_restart:
            if st.button("", key="floating_restart", help="Restart Chat", type="secondary"):
                st.session_state.messages = []
                st.session_state.user_name = None
                st.session_state.last_streamed_idx = -1
                st.rerun()
    
    with st.sidebar:
        # PIF Logo in sidebar
        st.markdown(f'<div style="text-align:center; padding:20px;"><img src="{PIF_LOGO_URL}" style="width:120px; filter:brightness(1.5);"></div>', unsafe_allow_html=True)
        
        st.markdown("## ⚙️ Settings")
        
        if st.session_state.show_chat:
            if st.button("🏠 Back to Home", use_container_width=True, key="sidebar_back"):
                st.session_state.show_chat = False
                st.rerun()
            
            if st.button("🔄 Restart Chat", use_container_width=True, key="sidebar_restart"):
                st.session_state.messages = []
                st.session_state.user_name = None
                st.session_state.last_streamed_idx = -1
                st.rerun()
            
            st.markdown("---")
        
        st.session_state.debug_mode = st.toggle("🐛 Debug Mode", value=st.session_state.debug_mode, help="Show source information")
        
        if st.button("🗑️ Clear All", use_container_width=True, key="clear_all"):
            st.session_state.messages = []
            st.session_state.user_name = None
            st.session_state.last_streamed_idx = -1
            st.session_state.show_chat = False
            st.rerun()
        
        st.markdown("---")
        
        with st.expander("💡 Tips for Better Results"):
            st.markdown("""
            **Be Specific**: 
            - ✅ "PIF's investment in NEOM 2023"
            - ❌ "Tell me about PIF"
            
            **Use Keywords**:
            - Investment, portfolio, sectors
            - NEOM, Vision 2030
            - Financial, revenue, jobs
            
            **Languages**: 
            - English & Arabic fully supported
            """)
        
        st.markdown("---")
        st.markdown("### 📊 Statistics")
        st.metric("Total Messages", len(st.session_state.messages))
        if st.session_state.user_name:
            st.success(f"👤 Welcome, {st.session_state.user_name}!")
    
    if not st.session_state.show_chat:
        # Landing page
        st.markdown(f'<div class="logo-container"><img src="{PIF_LOGO_URL}" alt="PIF Logo"></div>', unsafe_allow_html=True)
        st.markdown('<div class="hero-title">Pioneering Investments Send Ripples of Real Impact</div>', unsafe_allow_html=True)
        st.markdown('<div class="hero-subtitle">💬 Ask any question about PIF annual reports and get instant AI-powered answers</div>', unsafe_allow_html=True)
        
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
    
    else:
        # Chat interface header with logo
        st.markdown(f'<div class="logo-container"><img src="{PIF_LOGO_URL}" alt="PIF Logo" style="width: 150px;"></div>', unsafe_allow_html=True)
        st.markdown('<div class="hero-title" style="font-size: 2rem; margin-bottom: 30px;">PIF Chat Assistant</div>', unsafe_allow_html=True)
        
        # Display chat messages
        for idx, msg in enumerate(st.session_state.messages):
            with st.chat_message(msg["role"], avatar="🇸🇦" if msg["role"] == "assistant" else "👤"):
                # Stream ONLY if this is the latest message AND hasn't been streamed yet
                should_stream = (
                    msg["role"] == "assistant" and 
                    idx == len(st.session_state.messages) - 1 and 
                    idx > st.session_state.last_streamed_idx
                )
                
                if should_stream:
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
                
                # Follow-up buttons
                if "follow_ups" in msg and msg["follow_ups"]:
                    cols = st.columns(len(msg["follow_ups"]))
                    for i, follow_up in enumerate(msg["follow_ups"]):
                        with cols[i]:
                            if st.button(follow_up, key=f"followup_msg{idx}_opt{i}"):
                                handle_user_input(follow_up)
        
        # Chat input
        if prompt := st.chat_input("What's your name?" if not st.session_state.user_name else "Ask about PIF investments..."):
            handle_user_input(prompt)

if __name__ == "__main__":
    main()
