# Chat interaction handling
from nicegui import ui, background_tasks, context
from api_code.rag_query import get_rag_answer
import asyncio
import time
from .utils import UIUtils
from .components import UIComponents
from .styles import UIStyles

class ChatLogic:
    """Handles all chat-related logic and interactions"""
    
    def __init__(self):
        self.chat_history = []
        self.user_name = None
        self.is_first_interaction = True
        self.debug_mode = False
        self.current_question_input = None
        self.client_context = None
        
        # UI components
        self.components = UIComponents()
        
        # Initialize UI elements (will be set by main app)
        self.chat_area = None
        self.question_input = None
        self.char_counter = None
        self.send_btn = None
        self.chat_card = None
        self.chat_button = None
    
    def set_ui_elements(self, chat_area, question_input, char_counter, send_btn, chat_card, chat_button):
        """Set references to UI elements"""
        self.chat_area = chat_area
        self.question_input = question_input
        self.char_counter = char_counter
        self.send_btn = send_btn
        self.chat_card = chat_card
        self.chat_button = chat_button
        self.current_question_input = question_input
        # Store the client context for background tasks
        self.client_context = context.client
    
    def create_follow_up_handler(self, question_text):
        """Create a handler for follow-up questions"""
        def handler():
            if self.current_question_input:
                self.current_question_input.value = question_text
                ui.timer(0.1, lambda: self.handle_send(), once=True)
        return handler
    
    def show_tips(self):
        """Show tips for better answers"""
        self.components.show_tips_notification()
    
    def clear_chat(self):
        """Clear chat history and reset to initial state"""
        self.chat_history.clear()
        self.is_first_interaction = True
        self.user_name = None
        self.chat_area.clear()
        self.question_input.value = ''
        # Show welcome message again
        self.components.create_welcome_message(self.chat_area)
        self.question_input.placeholder = "What is your question...?"
    
    def toggle_debug(self):
        """Toggle debug mode"""
        self.debug_mode = not self.debug_mode
        ui.notify(f'Debug mode: {"ON" if self.debug_mode else "OFF"}', type='info')
    
    def close_chat(self):
        """Close chat and show chat button"""
        self.chat_card.visible = False
        self.chat_button.visible = True
    
    def open_chat(self):
        """Open chat and hide chat button"""
        self.chat_card.visible = True
        self.chat_button.visible = False
    
    def create_new_input_field(self):
        """Create a new input field with the correct placeholder"""
        # Remove the old input field
        self.question_input.delete()
        # Create new input field with correct placeholder
        self.question_input = ui.input('What is your question...?')
        self.question_input.style('width:100%; margin:8px; border-radius:20px; padding:12px 16px; font-size:14px; border:2px solid #e0e0e0; transition:all 0.3s ease;').classes('chat-input')
        # Reconnect the event handlers
        self.question_input.on('keydown.enter', self.handle_send)
        self.send_btn.on_click(self.handle_send)
    
    async def stream_text(self, text, question):
        """Stream text word by word with typing effect"""
        words = text.split()
        full_text = ""
        
        # Use stored client context for background task
        with self.chat_area:
            # Add user message first
            with ui.row().classes('message-container'):
                ui.image(UIStyles.USER_LOGO).classes('message-avatar')
                with ui.column().classes('message-content user-message'):
                    ui.markdown(f'{question}')
            
            # Add RAG message with streaming
            with ui.row().classes('message-container'):
                ui.image(UIStyles.RAG_LOGO).classes('message-avatar')
                with ui.column().classes('message-content rag-message') as rag_content:
                    for word in words:
                        full_text += word + " "
                        rag_content.clear()
                        ui.markdown(f'{full_text.strip()}')
                        await asyncio.sleep(0.05)  # Faster streaming
        
        # Add follow-up suggestions after streaming is complete
        follow_ups = UIUtils.generate_follow_up_questions(question, text)
        with self.chat_area:
            if follow_ups:
                limited_follow_ups = follow_ups[:2]
                with ui.row().classes('follow-up-suggestions').style('gap:12px; margin-top:8px;'):
                    for follow_up in limited_follow_ups:
                        handler = self.create_follow_up_handler(follow_up)
                        btn = ui.button(follow_up, on_click=handler)
                        btn.classes('follow-up-btn bounce-in')
                        btn.style('background:#006C35; color:white; border:1px solid white; border-radius:16px; padding:8px 16px; font-size:0.9rem;')
    
    async def send_question(self):
        """Process and send user question"""
        question = self.question_input.value.strip()
        
        # Input validation
        is_valid, error_message = UIUtils.validate_question_input(question)
        if not is_valid:
            # Use context manager for background task notifications
            with self.chat_area:
                with ui.row().classes('message-container'):
                    ui.image(UIStyles.RAG_LOGO).classes('message-avatar')
                    with ui.column().classes('message-content rag-message'):
                        ui.markdown(f'⚠️ {error_message}')
            return
        
        if question:
            # Show typing indicator
            with self.chat_area:
                typing_row = ui.row().classes('message-container')
                with typing_row:
                    ui.image(UIStyles.RAG_LOGO).classes('message-avatar')
                    with ui.column().classes('message-content rag-message'):
                        ui.html('<div style="display:flex; align-items:center; gap:8px;"><div class="typing-indicator"></div><span style="color:#666; font-size:0.9rem;">Searching PIF documents...</span></div>')
            
            # Handle first interaction (name input)
            if self.is_first_interaction:
                self.user_name = UIUtils.extract_name_from_input(question)
                self.is_first_interaction = False
                
                # Clear chat and show personalized welcome
                self.chat_area.clear()
                
                with self.chat_area:
                    # User message
                    with ui.row().classes('message-container'):
                        ui.image(UIStyles.USER_LOGO).classes('message-avatar')
                        with ui.column().classes('message-content user-message'):
                            ui.markdown(f'{question}')
                    
                    # Personalized welcome
                    with ui.row().classes('message-container bounce-in'):
                        ui.image(UIStyles.RAG_LOGO).classes('message-avatar')
                        with ui.column().classes('message-content rag-message personalized-welcome'):
                            welcome_text = f"🎉 Wonderful to meet you, {self.user_name}! I'm excited to help you explore PIF's amazing world of investments. What would you like to know about today? I can tell you about:\n\n• 💰 Investment strategies and portfolio performance\n• 🏗️ Vision 2030 projects like NEOM\n• 📊 Financial achievements and targets\n• 🌱 Sustainability initiatives\n• 🚀 Technology and innovation investments\n\nJust ask me anything!"
                            ui.markdown(welcome_text)
                
                self.question_input.value = ''
                return
            
            # Regular RAG interaction
            try:
                if self.debug_mode:
                    from api_code.rag_query import get_rag_answer_with_sources
                    rag_result = get_rag_answer_with_sources(question)
                    answer = rag_result['answer']
                    
                    if rag_result['sources']:
                        debug_info = f"\n\n🔍 **Debug Info:**\n"
                        debug_info += f"• Found {len(rag_result['sources'])} relevant sources\n"
                        debug_info += f"• Confidence: {rag_result['confidence']:.2f}\n"
                        # Fixed: Escape the quotes properly in f-string
                        sources_str = ', '.join([f"{s['year']} (score: {s['score']:.2f})" for s in rag_result['sources']])
                        debug_info += f"• Sources: {sources_str}\n"
                        answer += debug_info
                    else:
                        answer += "\n\n🔍 **Debug Info:** No relevant sources found"
                else:
                    answer = get_rag_answer(question)
                
                if not answer or answer.strip() == "":
                    answer = "I apologize, but I couldn't find a specific answer to your question. Could you please rephrase your question or ask about a different aspect of PIF's investments?"
            except Exception as e:
                answer = f"I'm experiencing some technical difficulties right now. Please try again in a moment or ask a different question about PIF's investments.\n\n_Error details: {str(e)[:100]}_"
            
            # Remove typing indicator
            self.chat_area.clear()
            
            # Add to chat history
            self.chat_history.append({
                'question': question,
                'answer': answer,
                'timestamp': time.time()
            })
            
            # Display all previous chat history
            with self.chat_area:
                for i, chat_item in enumerate(self.chat_history[:-1]):
                    # User message
                    with ui.row().classes('message-container bounce-in'):
                        ui.image(UIStyles.USER_LOGO).classes('message-avatar')
                        with ui.column().classes('message-content user-message'):
                            ui.markdown(f'{chat_item["question"]}')
                    # RAG message
                    with ui.row().classes('message-container'):
                        ui.image(UIStyles.RAG_LOGO).classes('message-avatar')
                        with ui.column().classes('message-content rag-message'):
                            ui.markdown(f'{chat_item["answer"]}')
            
            # Stream the latest response
            latest_chat = self.chat_history[-1]
            await self.stream_text(latest_chat["answer"], latest_chat["question"])
            
            # Clear input
            self.question_input.value = ''
    
    def handle_send(self):
        """Connect the async function to the UI"""
        self.current_question_input = self.question_input
        background_tasks.create(self.send_question())