# Helper utilities for the UI
import re
import time

class UIUtils:
    """Utility functions for the UI components"""
    
    @staticmethod
    def extract_name_from_input(user_input):
        """Extract just the name from user input, removing greetings and phrases"""
        # Convert to lowercase for easier processing
        input_lower = user_input.lower().strip()
        
        # Common greetings and phrases to remove
        greetings = [
            'hello', 'hi', 'hey', 'good morning', 'good afternoon', 'good evening',
            'مرحبا', 'السلام عليكم', 'أهلا', 'صباح الخير', 'مساء الخير',
            'i am', 'i\'m', 'my name is', 'اسمي', 'أنا', 'أنا اسمي'
        ]
        
        # Remove greetings from the beginning
        for greeting in greetings:
            if input_lower.startswith(greeting):
                input_lower = input_lower[len(greeting):].strip()
        
        # Remove common phrases and variations
        phrases_to_remove = [
            'my name is', 'i am', 'i\'m', 'iam', 'اسمي', 'أنا اسمي', 'أنا'
        ]
        
        for phrase in phrases_to_remove:
            if phrase in input_lower:
                input_lower = input_lower.replace(phrase, '').strip()
        
        # Clean up extra spaces and punctuation
        name = input_lower.strip()
        name = ' '.join(name.split())  # Remove extra spaces
        
        # Capitalize the name properly
        if name:
            name = name.title()
        
        return name if name else user_input.strip()
    
    @staticmethod
    def generate_follow_up_questions(question, answer):
        """Generate follow-up questions based on the current Q&A with deduplication"""
        # Create an empty set to track used questions
        used_questions = set()
        follow_ups = []
        
        # Detect if the question is in Arabic
        arabic_pattern = re.compile(r'[\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF\uFB50-\uFDFF\uFE70-\uFEFF]')
        is_arabic = bool(arabic_pattern.search(question))
        
        # Convert to lowercase for easier matching
        question_lower = question.lower()
        answer_lower = answer.lower()
        
        if is_arabic:
            # Arabic follow-up questions
            # Investment and portfolio related
            if any(word in question_lower for word in ['استثمار', 'محفظة', 'أصول', 'صندوق', 'investment', 'portfolio', 'asset', 'fund']):
                potential_questions = [
                    "ما هي القطاعات الاستثمارية الرئيسية؟",
                    "كيف تدير صندوق الاستثمارات العامة المخاطر؟",
                    "ما هي أحدث اتجاهات الاستثمار؟"
                ]
                for q in potential_questions:
                    if q not in used_questions:
                        follow_ups.append(q)
                        used_questions.add(q)
            
            # Financial and performance related
            elif any(word in question_lower for word in ['مالي', 'إيرادات', 'أرباح', 'أداء', 'financial', 'revenue', 'profit', 'performance', 'earnings']):
                potential_questions = [
                    "ما هي مصادر الإيرادات الرئيسية؟",
                    "كيف تغير الأداء مع مرور الوقت؟",
                    "ما هي الأهداف المالية؟"
                ]
                for q in potential_questions:
                    if q not in used_questions:
                        follow_ups.append(q)
                        used_questions.add(q)
            
            # NEOM and Vision 2030 related
            elif any(word in question_lower for word in ['نيوم', 'رؤية', '2030', 'مشروع', 'neom', 'vision', 'project']):
                potential_questions = [
                    "ما هي مشاريع رؤية 2030 الأخرى؟",
                    "كيف تساهم نيوم في الاقتصاد؟",
                    "ما هي المبادرات البيئية؟"
                ]
                for q in potential_questions:
                    if q not in used_questions:
                        follow_ups.append(q)
                        used_questions.add(q)
            
            # Employment and jobs related
            elif any(word in question_lower for word in ['وظيفة', 'توظيف', 'قوى عاملة', 'موظف', 'job', 'employment', 'workforce', 'employee']):
                potential_questions = [
                    "كم وظيفة أنشأها صندوق الاستثمارات العامة المخاطر؟",
                    "ما هي مبادرات التوظيف؟",
                    "كيف يدعم صندوق الاستثمارات العامة المواهب المحلية؟"
                ]
                for q in potential_questions:
                    if q not in used_questions:
                        follow_ups.append(q)
                        used_questions.add(q)
            
            # Technology and innovation related
            elif any(word in question_lower for word in ['تقنية', 'ابتكار', 'رقمي', 'تكنولوجيا', 'technology', 'innovation', 'digital', 'tech']):
                potential_questions = [
                    "ما هي استثمارات صندوق الاستثمارات العامة في التقنية؟",
                    "كيف يدعم صندوق الاستثمارات العامة الابتكار؟",
                    "ما هي المبادرات الرقمية؟"
                ]
                for q in potential_questions:
                    if q not in used_questions:
                        follow_ups.append(q)
                        used_questions.add(q)
            
            # Sustainability and environment related
            elif any(word in question_lower for word in ['استدامة', 'بيئة', 'أخضر', 'مناخ', 'sustainability', 'environment', 'green', 'climate']):
                potential_questions = [
                    "ما هي أهداف صندوق الاستثمارات العامة للاستدامة؟",
                    "كيف يتعامل صندوق الاستثمارات العامة مع تغير المناخ؟",
                    "ما هي الاستثمارات الخضراء؟"
                ]
                for q in potential_questions:
                    if q not in used_questions:
                        follow_ups.append(q)
                        used_questions.add(q)
            else:
                # Generic Arabic follow-ups
                if 'صندوق' in answer_lower or 'محفظة' in answer_lower:
                    potential_questions = [
                        "ما هي الإنجازات الرئيسية؟",
                        "كيف يقارن هذا بالسنوات السابقة؟",
                        "ما هي الخطط المستقبلية؟"
                    ]
                    for q in potential_questions:
                        if q not in used_questions:
                            follow_ups.append(q)
                            used_questions.add(q)
                else:
                    potential_questions = [
                        "هل يمكنك تقديم المزيد من التفاصيل؟",
                        "ما هي النقاط الرئيسية؟",
                        "كيف يرتبط هذا بمهمة صندوق الاستثمارات العامة؟"
                    ]
                    for q in potential_questions:
                        if q not in used_questions:
                            follow_ups.append(q)
                            used_questions.add(q)
        else:
            # English follow-up questions (existing logic)
            # Investment and portfolio related
            if any(word in question_lower for word in ['investment', 'portfolio', 'asset', 'fund']):
                potential_questions = [
                    "What are the key investment sectors?",
                    "How does PIF manage risk?",
                    "What are the latest investment trends?"
                ]
                for q in potential_questions:
                    if q not in used_questions:
                        follow_ups.append(q)
                        used_questions.add(q)
            # Financial and performance related
            elif any(word in question_lower for word in ['financial', 'revenue', 'profit', 'performance', 'earnings']):
                potential_questions = [
                    "What are the main revenue sources?",
                    "How has performance changed over time?",
                    "What are the financial targets?"
                ]
                for q in potential_questions:
                    if q not in used_questions:
                        follow_ups.append(q)
                        used_questions.add(q)
            # NEOM and Vision 2030 related
            elif any(word in question_lower for word in ['neom', 'vision', '2030', 'project']):
                potential_questions = [
                    "What other Vision 2030 projects are there?",
                    "How does NEOM contribute to the economy?",
                    "What are the environmental initiatives?"
                ]
                for q in potential_questions:
                    if q not in used_questions:
                        follow_ups.append(q)
                        used_questions.add(q)
            # Employment and jobs related
            elif any(word in question_lower for word in ['job', 'employment', 'workforce', 'employee']):
                potential_questions = [
                    "How many jobs has PIF created?",
                    "What are the employment initiatives?",
                    "How does PIF support local talent?"
                ]
                for q in potential_questions:
                    if q not in used_questions:
                        follow_ups.append(q)
                        used_questions.add(q)
            # Technology and innovation related
            elif any(word in question_lower for word in ['technology', 'innovation', 'digital', 'tech']):
                potential_questions = [
                    "What are PIF's technology investments?",
                    "How does PIF support innovation?",
                    "What digital initiatives are there?"
                ]
                for q in potential_questions:
                    if q not in used_questions:
                        follow_ups.append(q)
                        used_questions.add(q)
            # Sustainability and environment related
            elif any(word in question_lower for word in ['sustainability', 'environment', 'green', 'climate']):
                potential_questions = [
                    "What are PIF's sustainability goals?",
                    "How does PIF address climate change?",
                    "What green investments are there?"
                ]
                for q in potential_questions:
                    if q not in used_questions:
                        follow_ups.append(q)
                        used_questions.add(q)
            else:
                # Generic follow-ups based on common topics
                if 'pif' in answer_lower or 'portfolio' in answer_lower:
                    potential_questions = [
                        "What are the key achievements?",
                        "How does this compare to previous years?",
                        "What are the future plans?"
                    ]
                    for q in potential_questions:
                        if q not in used_questions:
                            follow_ups.append(q)
                            used_questions.add(q)
                else:
                    potential_questions = [
                        "Can you provide more details?",
                        "What are the key points?",
                        "How does this relate to PIF's mission?"
                    ]
                    for q in potential_questions:
                        if q not in used_questions:
                            follow_ups.append(q)
                            used_questions.add(q)
        
        # Return only unique questions (max 3)
        return list(used_questions)[:3]
    
    @staticmethod
    def validate_question_input(question):
        """Validate user question input"""
        if not question:
            return False, 'Please enter a question!'
        
        if len(question) < 3:
            return False, 'Please enter a longer question (at least 3 characters)!'
        
        if len(question) > 500:
            return False, 'Question is too long! Please keep it under 500 characters.'
        
        return True, None