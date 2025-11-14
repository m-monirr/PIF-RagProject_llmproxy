# UI component definitions
from nicegui import ui
from .styles import UIStyles

class UIComponents:
    """Manages UI component creation and layout"""
    
    def __init__(self):
        self.styles = UIStyles()
    
    def create_header(self):
        """Create the top header with Saudi-themed design"""
        header = ui.header().classes('gradient-header floating-animation')
        with header:
            with ui.row().style('align-items:center; justify-content:space-between; width:100%;'):
                with ui.row().style('align-items:center;'):
                    title = ui.label('PIF RAG Chat')
                    title.style('font-size:2rem; font-weight:bold; color:white; text-shadow:2px 2px 4px rgba(0,0,0,0.3);')
                
                # Add interactive elements to header
                with ui.row().style('gap:16px;'):
                    ui.button(icon='refresh', on_click=lambda: ui.notify('Refreshing...')).style('background:rgba(255,255,255,0.2); border:none; color:white;')
                    ui.button(icon='settings', on_click=lambda: ui.notify('Settings coming soon!')).style('background:rgba(255,255,255,0.2); border:none; color:white;')
        
        return header
    
    def create_hero_section(self):
        """Create the hero section with animations and stats"""
        with ui.column().style('max-width:900px; margin:48px auto 0 auto; align-items:center; text-align:center;'):
            ui.html('<div class="hero-title bounce-in">Pioneering investments send ripples of real impact through Saudi Arabia and the world</div>')
            ui.html('<div class="hero-subtitle shimmer">Ask any question about PIF annual reports and get instant answers powered by AI.</div>')
            
            # Enhanced interactive stats with hover effects and Saudi theme
            with ui.row().style('justify-content:center; gap:32px; margin-bottom:32px;'):
                with ui.element('div').classes('stat-card fadein interactive-card glow-effect'):
                    ui.icon('attach_money').classes('stat-icon')
                    ui.html('<div><div class="stat-value">925BN+ USD</div><div class="stat-label">Assets Under Management</div></div>')
                
                with ui.element('div').classes('stat-card fadein interactive-card glow-effect'):
                    ui.icon('groups').classes('stat-icon')
                    ui.html('<div><div class="stat-value">1.1+ Million</div><div class="stat-label">Direct & Indirect Jobs</div></div>')
                
                with ui.element('div').classes('stat-card fadein interactive-card glow-effect'):
                    ui.icon('business').classes('stat-icon')
                    ui.html('<div><div class="stat-value">220+</div><div class="stat-label">Portfolio Companies</div></div>')
    
    def create_chat_button(self, on_click_handler):
        """Create floating chat button"""
        chat_button = ui.button(
            icon='chat',
            on_click=on_click_handler,
            color=UIStyles.PIF_GREEN,
        )
        chat_button.style('position:fixed; bottom:32px; right:32px; border-radius:50%; width:64px; height:64px; z-index:1000;').classes('chat-glow fadein floating-animation')
        return chat_button
    
    def create_chat_card_header(self, close_handler, tips_handler, clear_handler, debug_handler):
        """Create the chat card header with utility buttons matching the photo design"""
        with ui.row().style('align-items:center; justify-content:space-between; background:#006C35; padding:12px 16px; border-radius:12px 12px 0 0; height:60px; width:100%; margin:0;'):
            with ui.row().style('align-items:center; gap:12px;'):
                # PIF logo/icon
                ui.icon('account_balance', size='24px').style('color:white;')
                ui.label('PIF Chat').style('color:white; font-weight:600; font-size:1.2rem; margin:0;')
            
            # Utility buttons row with styling matching the header color
            with ui.row().style('gap:8px;'):
                # Light bulb button
                tips_btn = ui.button(icon='lightbulb_outline', on_click=tips_handler)
                tips_btn.style('background:#006C35; color:white; border:none; min-width:40px; width:40px; height:40px; padding:0; border-radius:50%;')
                tips_btn.tooltip('Tips')
                tips_btn.classes('header-button')
                
                # Refresh/reset button
                reset_btn = ui.button(icon='refresh', on_click=clear_handler)
                reset_btn.style('background:#006C35; color:white; border:none; min-width:40px; width:40px; height:40px; padding:0; border-radius:50%;')
                reset_btn.tooltip('Reset Chat')
                reset_btn.classes('header-button')
                
                # Debug button
                debug_btn = ui.button(icon='build', on_click=debug_handler)
                debug_btn.style('background:#006C35; color:white; border:none; min-width:40px; width:40px; height:40px; padding:0; border-radius:50%;')
                debug_btn.tooltip('Debug Mode')
                debug_btn.classes('header-button')
                
                # Close button
                close_btn = ui.button(icon='close', on_click=close_handler)
                close_btn.style('background:#006C35; color:white; border:none; min-width:40px; width:40px; height:40px; padding:0; border-radius:50%;')
                close_btn.tooltip('Close Chat')
                close_btn.classes('header-button')

    
    def create_chat_area(self):
        """Create the chat messages area"""
        chat_area = ui.column()
        # Remove margin and adjust padding to eliminate gaps
        chat_area.style('min-height:200px; max-height:300px; overflow-y:auto; background:#fff; border-radius:0; padding:8px; margin:0;').classes('chat-area')
        return chat_area
    
    def create_chat_input_area(self, input_handler, send_handler):
        """Create the chat input area with input field and send button"""
        # Create a row to hold both input and send button side by side
        with ui.row().style('width:100%; margin:0; padding:8px; gap:8px; align-items:center;'):
            # Input area with enhanced styling
            with ui.element('div').classes('input-wrapper').style('flex:1; margin:0;'):
                question_input = ui.input(placeholder='What is your question...?')
                question_input.style('width:100%; border-radius:20px; padding:12px 16px; font-size:14px; border:2px solid #e0e0e0; transition:all 0.3s ease;').classes('chat-input')
        
            # Send button to the side
            send_btn = ui.button(icon='send', color=UIStyles.PIF_GREEN)
            send_btn.style('border-radius:50%; width:44px; height:44px; min-width:44px; padding:0;').classes('glow-effect')
    
        # Connect handlers
        question_input.on('keydown.enter', input_handler)
        send_btn.on_click(send_handler)
        
        # Return None for char_counter to maintain compatibility
        return question_input, None, send_btn
    
    def create_welcome_message(self, chat_area):
        """Create the initial welcome message in chat"""
        with chat_area:
            with ui.row().classes('message-container bounce-in'):
                ui.image(UIStyles.RAG_LOGO).classes('message-avatar')
                with ui.column().classes('message-content rag-message personalized-welcome'):
                    ui.markdown('👋 Hello! I\'m your PIF AI assistant. What\'s your name? I\'d love to personalize our conversation about PIF investments and help you discover amazing insights!')
    
    def create_user_message(self, chat_area, message):
        """Create a user message in the chat"""
        with chat_area:
            with ui.row().classes('message-container bounce-in'):
                ui.image(UIStyles.USER_LOGO).classes('message-avatar')
                with ui.column().classes('message-content user-message'):
                    ui.markdown(f'{message}')
    
    def create_rag_message(self, chat_area, message):
        """Create a RAG response message in the chat"""
        with chat_area:
            with ui.row().classes('message-container'):
                ui.image(UIStyles.RAG_LOGO).classes('message-avatar')
                with ui.column().classes('message-content rag-message'):
                    ui.markdown(f'{message}')
    
    def create_typing_indicator(self, chat_area):
        """Create typing indicator in chat"""
        with chat_area:
            with ui.row().classes('message-container'):
                ui.image(UIStyles.RAG_LOGO).classes('message-avatar')
                with ui.column().classes('message-content rag-message'):
                    typing_indicator = ui.html('<div style="display:flex; align-items:center; gap:8px;"><div class="typing-indicator"></div><span style="color:#666; font-size:0.9rem;">Searching PIF documents...</span></div>')
        return typing_indicator
    
    def create_follow_up_buttons(self, chat_area, follow_ups, handler_creator):
        """Create follow-up suggestion buttons"""
        if follow_ups:
            # Limit to only 2 follow-ups and display them side by side
            limited_follow_ups = follow_ups[:2]
            with chat_area:
                with ui.row().classes('follow-up-suggestions').style('gap:12px; margin-top:8px;'):
                    for follow_up in limited_follow_ups:
                        # Create a unique handler for each follow-up
                        handler = handler_creator(follow_up)
                        btn = ui.button(follow_up, on_click=handler)
                        btn.classes('follow-up-btn bounce-in')
                        btn.style('background:#006C35; color:white; border:1px solid white; border-radius:16px; padding:8px 16px; font-size:0.9rem;')
    
    def show_tips_notification(self):
        """Show tips notification"""
        tips_text = "**💡 Tips for Better Answers:**\n\n"
        tips_text += "1. **Be Specific**: Instead of 'What is PIF?', try 'What are PIF's main investment sectors?'\n\n"
        tips_text += "2. **Use Keywords**: Include terms like:\n"
        tips_text += "   - Investment, portfolio, assets\n"
        tips_text += "   - NEOM, Vision 2030, projects\n"
        tips_text += "   - Financial, revenue, performance\n"
        tips_text += "   - Jobs, employment, workforce\n"
        tips_text += "   - Technology, innovation, digital\n"
        tips_text += "   - Sustainability, environment, green\n\n"
        tips_text += "3. **Ask Follow-ups**: Use the suggested questions that appear after each answer\n\n"
        tips_text += "4. **Try Both Languages**: You can ask in Arabic or English\n\n"
        tips_text += "5. **Be Patient**: Complex questions may take a moment to process"
        
        ui.notify(tips_text, type='info', timeout=90, close_button=True)