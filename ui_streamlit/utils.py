"""
Utility functions for Streamlit UI
"""

import re

def extract_name_from_input(user_input):
    """Extract name from user input"""
    input_lower = user_input.lower().strip()
    
    # Remove greetings
    greetings = [
        'hello', 'hi', 'hey', 'good morning', 'good afternoon',
        'مرحبا', 'السلام عليكم', 'أهلا', 'صباح الخير'
    ]
    
    for greeting in greetings:
        if input_lower.startswith(greeting):
            input_lower = input_lower[len(greeting):].strip()
    
    # Remove phrases
    phrases = [
        'my name is', 'i am', 'i\'m', 'اسمي', 'أنا'
    ]
    
    for phrase in phrases:
        if phrase in input_lower:
            input_lower = input_lower.replace(phrase, '').strip()
    
    # Clean and capitalize
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
    """Generate follow-up questions"""
    # Import from original utils
    from ui.utils import UIUtils
    return UIUtils.generate_follow_up_questions(question, answer)
