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
        background: linear-gradient(180deg, #00A651 0%, #007A3D 100%);
        backdrop-filter: blur(10px);
    }
    
    [data-testid="stSidebar"] > div:first-child {
        background: transparent;
    }
    
    /* Sidebar content styling */
    [data-testid="stSidebar"] * {
        color: white !important;
    }
    
    /* Sidebar section headers */
    [data-testid="stSidebar"] h2 {
        font-size: 1.3rem;
        font-weight: 600;
        color: #FFFFFF !important;
        margin: 24px 0 16px 0;
        padding-bottom: 8px;
        border-bottom: 2px solid rgba(255, 255, 255, 0.2);
    }
    
    /* Sidebar buttons - Modern card style */
    [data-testid="stSidebar"] .stButton > button {
        background: rgba(255, 255, 255, 0.15) !important;
        color: white !important;
        border: 1px solid rgba(255, 255, 255, 0.3) !important;
        border-radius: 12px !important;
        padding: 12px 20px !important;
        font-weight: 500 !important;
        transition: all 0.3s ease !important;
        backdrop-filter: blur(10px) !important;
    }
    
    [data-testid="stSidebar"] .stButton > button:hover {
        background: rgba(255, 255, 255, 0.25) !important;
        border-color: rgba(255, 255, 255, 0.5) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2) !important;
    }
    
    /* Sidebar checkbox styling */
    [data-testid="stSidebar"] .stCheckbox {
        background: rgba(255, 255, 255, 0.1);
        padding: 12px;
        border-radius: 8px;
        margin: 8px 0;
    }
    
    /* Sidebar metrics */
    [data-testid="stSidebar"] [data-testid="stMetric"] {
        background: rgba(255, 255, 255, 0.1);
        padding: 16px;
        border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    [data-testid="stSidebar"] [data-testid="stMetricLabel"] {
        color: rgba(255, 255, 255, 0.9) !important;
        font-size: 0.9rem;
    }
    
    [data-testid="stSidebar"] [data-testid="stMetricValue"] {
        color: #FFFFFF !important;
        font-size: 1.8rem;
        font-weight: 700;
    }
    
    /* Sidebar expander */
    [data-testid="stSidebar"] .streamlit-expanderHeader {
        background: rgba(255, 255, 255, 0.1) !important;
        border-radius: 8px !important;
        padding: 12px 16px !important;
        font-weight: 500 !important;
    }
    
    [data-testid="stSidebar"] .streamlit-expanderHeader:hover {
        background: rgba(255, 255, 255, 0.15) !important;
    }
    
    [data-testid="stSidebar"] .streamlit-expanderContent {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 8px;
        padding: 12px;
        margin-top: 8px;
    }
    
    /* Sidebar divider */
    [data-testid="stSidebar"] hr {
        border-color: rgba(255, 255, 255, 0.2) !important;
        margin: 20px 0;
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
    }
    </style>
    """, unsafe_allow_html=True)
