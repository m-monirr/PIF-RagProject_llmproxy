"""
Streamlit custom styling - Saudi-themed design with floating chat
"""

import streamlit as st

def apply_custom_css():
    """Apply Saudi-themed custom CSS with floating chat support"""
    
    st.markdown("""
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;700&display=swap');
    
    /* Global styles */
    * {
        font-family: 'Montserrat', 'Arial', sans-serif;
    }
    
    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display:none;}
    
    /* Main background with particles effect */
    .stApp {
        background: linear-gradient(135deg, #F5F3ED 60%, #FFFFFF 100%);
    }
    
    /* Floating Chat Button */
    .chat-button {
        position: fixed;
        bottom: 32px;
        right: 32px;
        width: 70px;
        height: 70px;
        background: linear-gradient(135deg, #006C35 0%, #004D25 100%);
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        box-shadow: 0 8px 24px rgba(0, 108, 53, 0.4);
        z-index: 1000;
        transition: all 0.3s ease;
        animation: float 3s ease-in-out infinite;
    }
    
    .chat-button:hover {
        transform: translateY(-5px) scale(1.1);
        box-shadow: 0 12px 32px rgba(0, 108, 53, 0.6);
    }
    
    .chat-button img {
        width: 35px;
        height: 35px;
        filter: brightness(0) invert(1);
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
    }
    
    /* Floating Chat Container */
    .chat-container {
        position: fixed;
        bottom: 120px;
        right: 32px;
        width: 450px;
        max-width: 90vw;
        height: 600px;
        max-height: 80vh;
        background: white;
        border-radius: 20px;
        box-shadow: 0 12px 48px rgba(0, 108, 53, 0.3);
        z-index: 999;
        display: flex;
        flex-direction: column;
        overflow: hidden;
        animation: slideUp 0.3s ease-out;
    }
    
    @keyframes slideUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    /* Chat Header */
    .chat-header {
        background: linear-gradient(135deg, #006C35 0%, #004D25 50%, #006C35 100%);
        color: white;
        padding: 20px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        border-radius: 20px 20px 0 0;
    }
    
    .chat-header-title {
        display: flex;
        align-items: center;
        gap: 12px;
        font-size: 1.2rem;
        font-weight: 600;
    }
    
    .chat-header-title img {
        width: 32px;
        height: 32px;
    }
    
    .chat-close-btn {
        background: rgba(255, 255, 255, 0.2);
        border: none;
        color: white;
        width: 32px;
        height: 32px;
        border-radius: 50%;
        cursor: pointer;
        display: flex;
        align-items: center;
        justify-content: center;
        transition: all 0.2s;
    }
    
    .chat-close-btn:hover {
        background: rgba(255, 255, 255, 0.3);
        transform: rotate(90deg);
    }
    
    /* Chat Messages Area */
    .chat-messages {
        flex: 1;
        overflow-y: auto;
        padding: 16px;
        background: #F8F9FA;
    }
    
    /* Message Bubbles */
    .message-user {
        background: #006C35;
        color: white;
        padding: 12px 16px;
        border-radius: 18px 18px 4px 18px;
        margin: 8px 0 8px auto;
        max-width: 80%;
        width: fit-content;
        box-shadow: 0 2px 8px rgba(0, 108, 53, 0.2);
        animation: slideIn 0.3s ease-out;
    }
    
    .message-assistant {
        background: white;
        color: #222;
        padding: 12px 16px;
        border-radius: 18px 18px 18px 4px;
        margin: 8px auto 8px 0;
        max-width: 80%;
        width: fit-content;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        border-left: 4px solid #006C35;
        animation: slideIn 0.3s ease-out;
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
    
    /* Chat Input Area */
    .chat-input-container {
        padding: 16px;
        background: white;
        border-top: 1px solid #E5E7EB;
    }
    
    /* Follow-up buttons */
    .follow-up-container {
        display: flex;
        gap: 8px;
        flex-wrap: wrap;
        margin-top: 8px;
    }
    
    .follow-up-btn {
        background: #006C35;
        color: white;
        border: 1px solid white;
        border-radius: 16px;
        padding: 6px 14px;
        font-size: 0.85rem;
        cursor: pointer;
        transition: all 0.2s;
        white-space: nowrap;
    }
    
    .follow-up-btn:hover {
        background: white;
        color: #006C35;
        border-color: #006C35;
        transform: translateY(-2px);
    }
    
    /* Hero Section */
    .hero-section {
        text-align: center;
        padding: 60px 20px;
        max-width: 1200px;
        margin: 0 auto;
    }
    
    .hero-logo {
        width: 180px;
        height: auto;
        margin-bottom: 24px;
        animation: fadeIn 1s ease-out;
    }
    
    .hero-title {
        font-size: 3rem;
        font-weight: 700;
        color: #222;
        margin: 24px 0 16px 0;
        animation: slideDown 1s ease-out;
    }
    
    .hero-subtitle {
        font-size: 1.3rem;
        color: #006C35;
        margin-bottom: 48px;
        animation: fadeIn 1.5s ease-out;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    
    @keyframes slideDown {
        from {
            opacity: 0;
            transform: translateY(-30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    /* Stats Cards */
    .stats-container {
        display: flex;
        justify-content: center;
        gap: 32px;
        flex-wrap: wrap;
        margin: 48px 0;
    }
    
    .stat-card {
        background: white;
        border-radius: 20px;
        padding: 32px;
        text-align: center;
        min-width: 240px;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.08);
        transition: all 0.3s ease;
        animation: fadeIn 1s ease-out;
    }
    
    .stat-card:hover {
        transform: translateY(-12px);
        box-shadow: 0 16px 48px rgba(0, 108, 53, 0.15);
    }
    
    .stat-icon {
        font-size: 3rem;
        margin-bottom: 16px;
    }
    
    .stat-value {
        font-size: 2.5rem;
        font-weight: 700;
        color: #006C35;
        margin: 12px 0;
    }
    
    .stat-label {
        font-size: 1.1rem;
        color: #666;
    }
    
    /* Features Section */
    .features-container {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
        gap: 24px;
        margin: 48px 0;
        max-width: 1200px;
        margin-left: auto;
        margin-right: auto;
        padding: 0 20px;
    }
    
    .feature-card {
        background: white;
        border-radius: 16px;
        padding: 28px;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.06);
        transition: all 0.3s ease;
    }
    
    .feature-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 12px 32px rgba(0, 108, 53, 0.12);
    }
    
    .feature-icon {
        font-size: 2.5rem;
        margin-bottom: 16px;
    }
    
    .feature-title {
        font-size: 1.3rem;
        font-weight: 600;
        color: #006C35;
        margin-bottom: 12px;
    }
    
    .feature-desc {
        color: #666;
        line-height: 1.6;
    }
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .hero-title {
            font-size: 2rem;
        }
        
        .hero-subtitle {
            font-size: 1.1rem;
        }
        
        .chat-container {
            width: calc(100vw - 32px);
            right: 16px;
            bottom: 100px;
        }
        
        .chat-button {
            width: 60px;
            height: 60px;
            bottom: 24px;
            right: 24px;
        }
        
        .stat-card {
            min-width: 100%;
        }
    }
    
    /* Scrollbar styling */
    .chat-messages::-webkit-scrollbar {
        width: 6px;
    }
    
    .chat-messages::-webkit-scrollbar-track {
        background: #f1f1f1;
    }
    
    .chat-messages::-webkit-scrollbar-thumb {
        background: #006C35;
        border-radius: 3px;
    }
    
    .chat-messages::-webkit-scrollbar-thumb:hover {
        background: #004D25;
    }
    </style>
    """, unsafe_allow_html=True)
