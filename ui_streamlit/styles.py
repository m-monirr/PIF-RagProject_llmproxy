"""
Streamlit custom styling - Saudi-themed design
"""

import streamlit as st

def get_saudi_colors():
    """Return Saudi-themed color palette"""
    return {
        'primary': '#006C35',      # PIF Green
        'secondary': '#8F7838',    # PIF Gold
        'background': '#F5F3ED',   # PIF Beige
        'white': '#FFFFFF',
        'dark_green': '#004D25',
        'light_green': '#00A651',
        'text': '#222222',
        'text_light': '#666666'
    }

def apply_custom_css():
    """Apply Saudi-themed custom CSS to Streamlit app"""
    
    colors = get_saudi_colors()
    
    st.markdown(f"""
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;700&display=swap');
    
    /* Global styles */
    * {{
        font-family: 'Montserrat', 'Arial', sans-serif;
    }}
    
    /* Main background */
    .stApp {{
        background: linear-gradient(135deg, {colors['background']} 60%, {colors['white']} 100%);
    }}
    
    /* Header styling */
    header {{
        background: linear-gradient(135deg, {colors['primary']} 0%, {colors['dark_green']} 50%, {colors['primary']} 100%) !important;
    }}
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {{
        background: linear-gradient(180deg, {colors['primary']} 0%, {colors['dark_green']} 100%);
    }}
    
    [data-testid="stSidebar"] * {{
        color: {colors['white']} !important;
    }}
    
    /* Chat message styling */
    .stChatMessage {{
        border-radius: 12px;
        padding: 16px;
        margin: 8px 0;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        animation: slideIn 0.5s ease-out;
    }}
    
    @keyframes slideIn {{
        from {{
            opacity: 0;
            transform: translateY(20px);
        }}
        to {{
            opacity: 1;
            transform: translateY(0);
        }}
    }}
    
    /* User message */
    [data-testid="stChatMessage"][data-is-user="true"] {{
        background: {colors['primary']};
        color: {colors['white']};
        border-left: 4px solid {colors['light_green']};
    }}
    
    /* Assistant message */
    [data-testid="stChatMessage"][data-is-user="false"] {{
        background: {colors['white']};
        color: {colors['text']};
        border-left: 4px solid {colors['primary']};
    }}
    
    /* Input styling */
    .stTextInput > div > div > input {{
        border-radius: 20px;
        border: 2px solid {colors['primary']};
        padding: 12px 20px;
        font-size: 14px;
        transition: all 0.3s ease;
    }}
    
    .stTextInput > div > div > input:focus {{
        border-color: {colors['light_green']};
        box-shadow: 0 0 0 3px rgba(0, 108, 53, 0.2);
    }}
    
    /* Button styling */
    .stButton > button {{
        background: {colors['primary']};
        color: {colors['white']};
        border: none;
        border-radius: 20px;
        padding: 10px 24px;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 12px rgba(0, 108, 53, 0.2);
    }}
    
    .stButton > button:hover {{
        background: {colors['light_green']};
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(0, 108, 53, 0.3);
    }}
    
    /* Follow-up button styling */
    .follow-up-btn {{
        background: {colors['primary']};
        color: {colors['white']};
        border: 1px solid {colors['white']};
        border-radius: 16px;
        padding: 8px 16px;
        font-size: 0.9rem;
        margin: 4px;
        display: inline-block;
        cursor: pointer;
        transition: all 0.3s ease;
    }}
    
    .follow-up-btn:hover {{
        background: {colors['white']};
        color: {colors['primary']};
        border-color: {colors['primary']};
    }}
    
    /* Stats card styling */
    .stat-card {{
        background: {colors['white']};
        border-radius: 16px;
        padding: 24px;
        text-align: center;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
    }}
    
    .stat-card:hover {{
        transform: translateY(-8px);
        box-shadow: 0 8px 24px rgba(0, 108, 53, 0.2);
    }}
    
    .stat-value {{
        font-size: 2rem;
        font-weight: 700;
        color: {colors['primary']};
        margin: 8px 0;
    }}
    
    .stat-label {{
        font-size: 1rem;
        color: {colors['text_light']};
    }}
    
    /* Hero section */
    .hero-title {{
        font-size: 2.5rem;
        font-weight: 700;
        color: {colors['text']};
        text-align: center;
        margin: 24px 0 16px 0;
        animation: fadeIn 1s ease-out;
    }}
    
    .hero-subtitle {{
        font-size: 1.2rem;
        color: {colors['primary']};
        text-align: center;
        margin-bottom: 32px;
        animation: fadeIn 1.5s ease-out;
    }}
    
    @keyframes fadeIn {{
        from {{ opacity: 0; }}
        to {{ opacity: 1; }}
    }}
    
    /* Spinner */
    .stSpinner > div {{
        border-top-color: {colors['primary']} !important;
    }}
    
    /* Success/Error messages */
    .stSuccess {{
        background-color: rgba(0, 166, 81, 0.1);
        border-left: 4px solid {colors['light_green']};
    }}
    
    .stError {{
        background-color: rgba(255, 67, 54, 0.1);
        border-left: 4px solid #FF4336;
    }}
    
    /* Hide Streamlit branding */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    header {{visibility: hidden;}}
    
    /* Responsive design */
    @media (max-width: 768px) {{
        .hero-title {{
            font-size: 1.8rem;
        }}
        .hero-subtitle {{
            font-size: 1rem;
        }}
        .stat-card {{
            margin: 8px 0;
        }}
    }}
    </style>
    """, unsafe_allow_html=True)
