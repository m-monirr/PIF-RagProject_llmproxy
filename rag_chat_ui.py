from nicegui import ui
from ui import ChatLogic, UIComponents, UIStyles, UIUtils

def main():
    """Main application entry point"""
    # Initialize components
    styles = UIStyles()
    components = UIComponents()
    chat_logic = ChatLogic()
    
    # Apply styling
    styles.apply_custom_css()
    styles.apply_particles_background()
    styles.set_body_background()
    styles.add_input_placeholder_script()
    
    # Create header
    header = components.create_header()
    
    # Create hero section
    components.create_hero_section()
    
    # Floating chat button
    chat_button = components.create_chat_button(
        on_click_handler=lambda: chat_logic.open_chat()
    )
    
    # Pop-out chat card with Saudi-themed design - add display:flex and flex-direction:column
    chat_card = ui.card()
    chat_card.style(f'position:fixed; bottom:100px; right:32px; width:450px; max-width:90vw; z-index:1001; box-shadow:0 8px 32px rgba(0,108,53,0.3); background:#fff; border-radius:12px; max-height:65vh; overflow:hidden; padding:0; margin:0; display:flex; flex-direction:column;')
    
    with chat_card:
        # Enhanced header with Saudi gradient
        components.create_chat_card_header(
            close_handler=chat_logic.close_chat,
            tips_handler=chat_logic.show_tips,
            clear_handler=chat_logic.clear_chat,
            debug_handler=chat_logic.toggle_debug
        )
        
        # Chat area with scrollable content
        chat_area = components.create_chat_area()
        
        # Personalized welcome message
        components.create_welcome_message(chat_area)
        
        # Input area with enhanced styling
        question_input, char_counter, send_btn = components.create_chat_input_area(
            input_handler=chat_logic.handle_send,
            send_handler=chat_logic.handle_send
        )
    
    # Set initial visibility
    chat_card.visible = False
    
    # Connect UI elements to chat logic
    chat_logic.set_ui_elements(chat_area, question_input, char_counter, send_btn, chat_card, chat_button)

if __name__ in {"__main__", "__mp_main__"}:
    main()
    ui.run(title='PIF RAG Chat – Ask About Saudi Investments', dark=False, favicon=UIStyles.PIF_FAVICON)
