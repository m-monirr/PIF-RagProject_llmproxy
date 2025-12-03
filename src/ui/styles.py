"""
Streamlit custom styling - PIF-themed design (Black, Green, Gold)
"""

import streamlit as st

def apply_custom_css():
    """Apply PIF-themed custom CSS"""
    
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
        box-shadow: 0 8px 24px rgba(0,166,81,0.2);
        transition: all 0.3s ease;
    }
    
    .stat-card:hover {
        transform: translateY(-10px);
        box-shadow: 0 16px 48px rgba(143,120,56,0.3);
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
        box-shadow: 0 4px 16px rgba(0,166,81,0.15);
        transition: all 0.3s ease;
    }
    
    .feature-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 12px 32px rgba(143,120,56,0.25);
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
    
    /* Sidebar - Modern Green gradient with glassmorphism */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, 
            rgba(0, 166, 81, 0.95) 0%, 
            rgba(0, 122, 61, 0.98) 50%,
            rgba(0, 77, 37, 1) 100%
        );
        backdrop-filter: blur(20px);
        border-right: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 4px 0 24px rgba(0, 0, 0, 0.3);
    }
    
    [data-testid="stSidebar"] > div:first-child {
        background: transparent;
        padding-top: 1rem;
    }
    
    /* All text white */
    [data-testid="stSidebar"] * {
        color: white !important;
    }
    
    /* Section headers with elegant underline */
    [data-testid="stSidebar"] h2 {
        font-size: 1.4rem;
        font-weight: 700;
        color: #FFFFFF !important;
        margin: 32px 0 20px 0;
        padding-bottom: 12px;
        border-bottom: 3px solid rgba(255, 255, 255, 0.3);
        letter-spacing: 0.5px;
        text-transform: uppercase;
        position: relative;
    }
    
    [data-testid="stSidebar"] h2::after {
        content: '';
        position: absolute;
        bottom: -3px;
        left: 0;
        width: 60px;
        height: 3px;
        background: linear-gradient(90deg, #FFD700, #FFA500);
        border-radius: 2px;
    }
    
    /* Modern glass-morphism buttons */
    [data-testid="stSidebar"] .stButton > button {
        background: rgba(255, 255, 255, 0.12) !important;
        color: white !important;
        border: 1.5px solid rgba(255, 255, 255, 0.25) !important;
        border-radius: 14px !important;
        padding: 14px 20px !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
        letter-spacing: 0.3px !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        backdrop-filter: blur(10px) !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15) !important;
        position: relative;
        overflow: hidden;
    }
    
    /* Button hover effect with shimmer */
    [data-testid="stSidebar"] .stButton > button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(
            90deg,
            transparent,
            rgba(255, 255, 255, 0.2),
            transparent
        );
        transition: left 0.5s;
    }
    
    [data-testid="stSidebar"] .stButton > button:hover::before {
        left: 100%;
    }
    
    [data-testid="stSidebar"] .stButton > button:hover {
        background: rgba(255, 255, 255, 0.22) !important;
        border-color: rgba(255, 255, 255, 0.45) !important;
        transform: translateY(-3px) scale(1.02) !important;
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.25) !important;
    }
    
    [data-testid="stSidebar"] .stButton > button:active {
        transform: translateY(-1px) scale(0.98) !important;
    }
    
    /* Checkbox with modern toggle style */
    [data-testid="stSidebar"] .stCheckbox {
        background: rgba(255, 255, 255, 0.08);
        padding: 16px;
        border-radius: 12px;
        margin: 12px 0;
        border: 1px solid rgba(255, 255, 255, 0.15);
        transition: all 0.3s ease;
    }
    
    [data-testid="stSidebar"] .stCheckbox:hover {
        background: rgba(255, 255, 255, 0.12);
        border-color: rgba(255, 255, 255, 0.25);
        transform: translateX(4px);
    }
    
    /* Beautiful metric cards */
    [data-testid="stSidebar"] [data-testid="stMetric"] {
        background: linear-gradient(135deg, 
            rgba(255, 255, 255, 0.1) 0%, 
            rgba(255, 255, 255, 0.05) 100%
        );
        padding: 20px;
        border-radius: 16px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.2);
        transition: all 0.3s ease;
    }
    
    [data-testid="stSidebar"] [data-testid="stMetric"]:hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.3);
        border-color: rgba(255, 215, 0, 0.4);
    }
    
    [data-testid="stSidebar"] [data-testid="stMetricLabel"] {
        color: rgba(255, 255, 255, 0.85) !important;
        font-size: 0.9rem;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    [data-testid="stSidebar"] [data-testid="stMetricValue"] {
        color: #FFD700 !important;
        font-size: 2rem;
        font-weight: 800;
        text-shadow: 0 2px 8px rgba(255, 215, 0, 0.3);
    }
    
    /* Elegant expander headers */
    [data-testid="stSidebar"] .streamlit-expanderHeader {
        background: rgba(255, 255, 255, 0.1) !important;
        border-radius: 12px !important;
        padding: 14px 18px !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
        transition: all 0.3s ease !important;
    }
    
    [data-testid="stSidebar"] .streamlit-expanderHeader:hover {
        background: rgba(255, 255, 255, 0.18) !important;
        border-color: rgba(255, 255, 255, 0.3) !important;
        transform: translateX(4px);
    }
    
    [data-testid="stSidebar"] .streamlit-expanderContent {
        background: rgba(0, 0, 0, 0.1);
        border-radius: 12px;
        padding: 16px;
        margin-top: 10px;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    /* Divider styling */
    [data-testid="stSidebar"] hr {
        border: none !important;
        height: 2px !important;
        background: linear-gradient(
            90deg,
            transparent,
            rgba(255, 255, 255, 0.3),
            transparent
        ) !important;
        margin: 28px 0 !important;
    }
    
    /* Success message styling */
    [data-testid="stSidebar"] .stSuccess {
        background: rgba(255, 215, 0, 0.15) !important;
        border-left: 4px solid #FFD700 !important;
        border-radius: 8px !important;
        padding: 12px 16px !important;
        font-weight: 600 !important;
    }
    
    /* Remove broken toggle button styles - Streamlit handles sidebar natively */
    
    /* Animation for sidebar appearance */
    @keyframes slideInFromLeft {
        from {
            transform: translateX(-100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    [data-testid="stSidebar"] {
        animation: slideInFromLeft 0.3s ease-out;
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
    
    /* Control Panel Buttons - Clean design with modern simple icons */
    button[key^="ctrl_"] {
        width: 48px !important;
        height: 48px !important;
        min-width: 48px !important;
        min-height: 48px !important;
        max-width: 48px !important;
        max-height: 48px !important;
        padding: 0 !important;
        margin: 0 4px !important;
        border-radius: 12px !important;
        background: rgba(40, 44, 52, 1) !important;
        color: rgba(255, 255, 255, 0.9) !important;
        font-size: 1.8rem !important;
        font-weight: 300 !important;
        border: 1px solid rgba(60, 64, 72, 1) !important;
        transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.3) !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        position: relative !important;
        cursor: pointer !important;
        line-height: 1 !important;
    }
    
    button[key^="ctrl_"]:hover {
        background: rgba(55, 59, 67, 1) !important;
        border-color: rgba(80, 84, 92, 1) !important;
        transform: translateY(-2px) scale(1.05) !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.5) !important;
    }
    
    button[key^="ctrl_"]:active {
        transform: translateY(0px) scale(0.95) !important;
        box-shadow: 0 1px 2px rgba(0, 0, 0, 0.3) !important;
    }
    
    /* Specific button hover colors with modern look */
    button[key="ctrl_restart"]:hover {
        background: rgba(0, 166, 81, 0.25) !important;
        border-color: rgba(0, 166, 81, 0.6) !important;
        box-shadow: 0 4px 16px rgba(0, 166, 81, 0.4) !important;
    }
    
    button[key="ctrl_debug"]:hover {
        background: rgba(255, 152, 0, 0.25) !important;
        border-color: rgba(255, 152, 0, 0.6) !important;
        box-shadow: 0 4px 16px rgba(255, 152, 0, 0.4) !important;
    }
    
    button[key="ctrl_tips"]:hover {
        background: rgba(33, 150, 243, 0.25) !important;
        border-color: rgba(33, 150, 243, 0.6) !important;
        box-shadow: 0 4px 16px rgba(33, 150, 243, 0.4) !important;
    }
    
    button[key="ctrl_logout"]:hover {
        background: rgba(211, 47, 47, 0.25) !important;
        border-color: rgba(211, 47, 47, 0.6) !important;
        box-shadow: 0 4px 16px rgba(211, 47, 47, 0.4) !important;
    }
    
    /* Badge styling - with emoji */
    .control-badge {
        background: rgba(0, 166, 81, 1) !important;
        color: white !important;
        padding: 10px 20px !important;
        border-radius: 50px !important;
        font-size: 0.95rem !important;
        font-weight: 700 !important;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3) !important;
        display: inline-flex !important;
        align-items: center !important;
        justify-content: center !important;
        gap: 8px !important;
        min-width: 70px !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
    }
    /* Responsive */
    @media (max-width: 768px) {
        .hero-title {
            font-size: 1.8rem;
        }
        .hero-subtitle {
            font-size: 1rem;
        }
    }
    </style>
    """, unsafe_allow_html=True)