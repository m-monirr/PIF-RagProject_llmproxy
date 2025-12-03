"""
Utility functions for Streamlit UI
All business logic and helper functions
"""

import streamlit as st
import time
import re
from src.retrieval.rag_query import get_rag_answer, get_rag_answer_with_sources

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
    """Process user input and update chat"""
    
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
            # Prepare chat history (exclude welcome message and current question)
            chat_history = [msg for msg in st.session_state.messages[:-1] 
                          if msg.get('content') and not msg['content'].startswith('🎉')]
            
            if st.session_state.debug_mode:
                rag_result = get_rag_answer_with_sources(user_input, chat_history=chat_history)
                answer = rag_result['answer']
                
                if rag_result['sources']:
                    debug_info = f"\n\n**🔍 Debug Info:**\n"
                    debug_info += f"• Sources: {len(rag_result['sources'])}\n"
                    debug_info += f"• Confidence: {rag_result['confidence']:.2f}\n"
                    sources_str = ', '.join([f"{s['year']} ({s['score']:.2f})" for s in rag_result['sources']])
                    debug_info += f"• Years: {sources_str}\n"
                    debug_info += f"• History: {len(chat_history)} messages"
                    answer += debug_info
            else:
                answer = get_rag_answer(user_input, chat_history=chat_history)
            
            if not answer or answer.strip() == "":
                answer = "I couldn't find specific information. Please rephrase your question."
            
            follow_ups = generate_follow_up_questions(user_input, answer)
            st.session_state.messages.append({'role': 'assistant', 'content': answer, 'follow_ups': follow_ups[:2]})
        except Exception as e:
            st.session_state.messages.append({'role': 'assistant', 'content': f"Error: {str(e)[:100]}", 'follow_ups': []})
    
    st.rerun()