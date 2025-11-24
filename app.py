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
    
    /* Hero title - Muted Gold #8F7838 */
    .hero-title {
        text-align: center;
        font-size: 2.5rem;
        font-weight: 700;
        color: #8F7838;
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
        box-shadow: 0 16px 48px rgba(143, 120, 56, 0.3);
        border-color: #8F7838;
    }
    
    .stat-icon {
        font-size: 3rem;
        margin-bottom: 15px;
    }
    
    .stat-value {
        font-size: 2.2rem;
        font-weight: 700;
        color: #8F7838;
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
        box-shadow: 0 12px 32px rgba(143, 120, 56, 0.25);
        border-color: #8F7838;
    }
    
    .feature-icon {
        font-size: 2.5rem;
        margin-bottom: 15px;
    }
    
    .feature-title {
        font-size: 1.2rem;
        font-weight: 600;
        color: #8F7838;
        margin-bottom: 10px;
    }
    
    .feature-desc {
        color: #CCCCCC;
        line-height: 1.6;
    }
    
    /* Floating action buttons container - Fixed top-right */
    .floating-container {
        position: fixed;
        top: 20px;
        right: 20px;
        z-index: 9999;
        display: flex;
        flex-direction: column;
        gap: 12px;
    }
    
    /* Modern floating button style */
    .float-btn {
        width: 56px;
        height: 56px;
        border-radius: 16px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.4rem;
        cursor: pointer;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.4);
        border: 2px solid #8F7838;
    }
    
    .float-btn-back {
        background: linear-gradient(135deg, #1A1A1A 0%, #2A2A2A 100%);
        color: #8F7838;
    }
    
    .float-btn-back:hover {
        background: linear-gradient(135deg, #8F7838 0%, #6F5828 100%);
        color: #FFFFFF;
        transform: translateX(-4px) scale(1.05);
        box-shadow: 0 6px 24px rgba(143, 120, 56, 0.5);
    }
    
    .float-btn-restart {
        background: linear-gradient(135deg, #00A651 0%, #007A3D 100%);
        color: white;
    }
    
    .float-btn-restart:hover {
        background: linear-gradient(135deg, #00D46E 0%, #00A651 100%);
        transform: rotate(180deg) scale(1.05);
        box-shadow: 0 6px 24px rgba(0, 166, 81, 0.5);
    }
    
    /* Hide the actual Streamlit buttons that trigger actions */
    button[key="floating_back_actual"],
    button[key="floating_restart_actual"] {
        display: none !important;
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
        border-color: #8F7838;
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
    
    /* Buttons - Muted Gold accent */
    .stButton > button {
        background: linear-gradient(135deg, #8F7838 0%, #6F5828 100%);
        color: #FFFFFF;
        font-weight: 600;
        border: none;
        border-radius: 12px;
        padding: 12px 24px;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(143, 120, 56, 0.4);
        background: linear-gradient(135deg, #A08948 0%, #8F7838 100%);
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
        border-color: #8F7838;
        box-shadow: 0 0 0 3px rgba(143, 120, 56, 0.2);
    }
    
    /* Responsive */
    @media (max-width: 768px) {
        .hero-title {
            font-size: 1.8rem;
        }
        .hero-subtitle {
            font-size: 1rem;
        }
        .floating-container {
            top: 12px;
            right: 12px;
        }
        .float-btn {
            width: 48px;
            height: 48px;
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
    
    with st.sidebar:
        # PIF Logo in sidebar
        st.markdown(f'<div style="text-align:center; padding:20px;"><img src="{PIF_LOGO_URL}" style="width:120px; filter:brightness(1.5);"></div>', unsafe_allow_html=True)
        
        st.markdown("## ⚙️ Settings")
        
        if st.session_state.show_chat:
            # Sidebar navigation buttons
            col1, col2 = st.columns(2)
            with col1:
                if st.button("🏠 Home", use_container_width=True, key="sidebar_back"):
                    st.session_state.show_chat = False
                    st.rerun()
            with col2:
                if st.button("🔄 Restart", use_container_width=True, key="sidebar_restart"):
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
        # Chat interface
        
        # Floating action buttons with click handlers
        col1, col2 = st.columns([20, 1])
        
        with col2:
            # Back button
            if st.button("⬅", key="float_back", help="Back to Home", use_container_width=False):
                st.session_state.show_chat = False
                st.rerun()
            
            # Restart button
            if st.button("↻", key="float_restart", help="Restart Chat", use_container_width=False):
                st.session_state.messages = []
                st.session_state.user_name = None
                st.session_state.last_streamed_idx = -1
                st.rerun()
        
        # Add custom CSS to style these buttons as floating with enhanced animations
        st.markdown("""
        <style>
        /* Style the specific buttons */
        button[key="float_back"],
        button[key="float_restart"] {
            position: fixed !important;
            right: 20px !important;
            width: 56px !important;
            height: 56px !important;
            border-radius: 16px !important;
            min-height: 56px !important;
            padding: 0 !important;
            z-index: 9999 !important;
            font-size: 1.4rem !important;
            box-shadow: 0 4px 16px rgba(0, 0, 0, 0.4) !important;
            border: 2px solid #8F7838 !important;
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
            cursor: pointer !important;
        }
        
        /* First button (Back) - Muted Gold/Dark theme */
        button[key="float_back"] {
            top: 20px !important;
            background: linear-gradient(135deg, #1A1A1A 0%, #2A2A2A 100%) !important;
            color: #8F7838 !important;
        }
        
        button[key="float_back"]:hover {
            background: linear-gradient(135deg, #8F7838 0%, #6F5828 100%) !important;
            color: #FFFFFF !important;
            transform: translateX(-8px) scale(1.1) rotate(-5deg) !important;
            box-shadow: 0 8px 32px rgba(143, 120, 56, 0.6) !important;
            border-color: #FFFFFF !important;
        }
        
        button[key="float_back"]:active {
            transform: translateX(-6px) scale(1.05) !important;
            box-shadow: 0 4px 16px rgba(143, 120, 56, 0.4) !important;
        }
        
        /* Second button (Restart) - Green theme */
        button[key="float_restart"] {
            top: 88px !important;
            background: linear-gradient(135deg, #00A651 0%, #007A3D 100%) !important;
            color: white !important;
        }
        
        button[key="float_restart"]:hover {
            background: linear-gradient(135deg, #00D46E 0%, #00A651 100%) !important;
            transform: rotate(360deg) scale(1.15) !important;
            box-shadow: 0 8px 32px rgba(0, 166, 81, 0.6) !important;
            border-color: #FFFFFF !important;
        }
        
        button[key="float_restart"]:active {
            transform: rotate(180deg) scale(1.05) !important;
            box-shadow: 0 4px 16px rgba(0, 166, 81, 0.4) !important;
        }
        
        /* Pulse animation on page load */
        @keyframes pulse {
            0%, 100% {
                transform: scale(1);
                box-shadow: 0 4px 16px rgba(0, 0, 0, 0.4);
            }
            50% {
                transform: scale(1.05);
                box-shadow: 0 6px 24px rgba(143, 120, 56, 0.5);
            }
        }
        
        button[key="float_back"],
        button[key="float_restart"] {
            animation: pulse 2s ease-in-out infinite !important;
        }
        
        button[key="float_back"]:hover,
        button[key="float_restart"]:hover {
            animation: none !important;
        }
        
        /* Ripple effect on click */
        @keyframes ripple {
            0% {
                transform: scale(1);
                opacity: 1;
            }
            100% {
                transform: scale(1.5);
                opacity: 0;
            }
        }
        
        button[key="float_back"]::before,
        button[key="float_restart"]::before {
            content: '';
            position: absolute;
            top: 50%;
            left: 50%;
            width: 100%;
            height: 100%;
            border-radius: 50%;
            background: rgba(143, 120, 56, 0.3);
            transform: translate(-50%, -50%) scale(0);
            transition: transform 0.5s, opacity 0.5s;
        }
        
        button[key="float_back"]:active::before,
        button[key="float_restart"]:active::before {
            transform: translate(-50%, -50%) scale(1.5);
            opacity: 0;
        }
        
        /* Glow effect */
        button[key="float_back"]::after,
        button[key="float_restart"]::after {
            content: '';
            position: absolute;
            top: -2px;
            left: -2px;
            right: -2px;
            bottom: -2px;
            border-radius: 16px;
            background: linear-gradient(45deg, #8F7838, #00A651, #8F7838);
            z-index: -1;
            opacity: 0;
            transition: opacity 0.3s;
        }
        
        button[key="float_back"]:hover::after,
        button[key="float_restart"]:hover::after {
            opacity: 0.6;
            animation: rotate 2s linear infinite;
        }
        
        @keyframes rotate {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        /* Hide the column wrapper */
        div[data-testid="column"]:has(button[key="float_back"]),
        div[data-testid="column"]:has(button[key="float_restart"]) {
            position: fixed !important;
            right: 0 !important;
            top: 0 !important;
            width: auto !important;
            background: transparent !important;
            z-index: 9999 !important;
        }
        
        /* Tooltip on hover */
        button[key="float_back"]:hover::before {
            content: attr(aria-label);
            position: absolute;
            right: 100%;
            top: 50%;
            transform: translateY(-50%);
            background: rgba(26, 26, 26, 0.95);
            color: #8F7838;
            padding: 8px 12px;
            border-radius: 8px;
            white-space: nowrap;
            margin-right: 12px;
            font-size: 0.9rem;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
            border: 1px solid #8F7838;
        }
        
        button[key="float_restart"]:hover::before {
            content: attr(aria-label);
            position: absolute;
            right: 100%;
            top: 50%;
            transform: translateY(-50%);
            background: rgba(0, 166, 81, 0.95);
            color: white;
            padding: 8px 12px;
            border-radius: 8px;
            white-space: nowrap;
            margin-right: 12px;
            font-size: 0.9rem;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
            border: 1px solid white;
        }
        
        /* Mobile responsive */
        @media (max-width: 768px) {
            button[key="float_back"],
            button[key="float_restart"] {
                width: 48px !important;
                height: 48px !important;
                font-size: 1.2rem !important;
                right: 12px !important;
            }
            
            button[key="float_back"] {
                top: 12px !important;
            }
            
            button[key="float_restart"] {
                top: 72px !important;
            }
        }
        </style>
        """, unsafe_allow_html=True)
        
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
