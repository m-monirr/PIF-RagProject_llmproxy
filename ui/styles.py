# UI styling and theming
from nicegui import ui

class UIStyles:
    """Manages all UI styling and CSS for the PIF RAG Chat application"""
    
    # Saudi-themed branding colors
    PIF_GREEN = '#006C35'
    PIF_GOLD = '#8F7838'
    PIF_BEIGE = '#F5F3ED'
    PIF_WHITE = '#FFFFFF'
    PIF_DARK_GREEN = '#004D25'
    PIF_LIGHT_GREEN = '#00A651'
    PIF_LOGO_URL = 'https://cdn.brandfetch.io/idnYHC3i7K/theme/dark/logo.svg?c=1bxid64Mup7aczewSAYMX&t=1754092788470'
    PIF_FAVICON = 'https://www.pif.gov.sa/favicon.ico'
    
    # User and RAG logos
    USER_LOGO = 'https://cdn-icons-png.flaticon.com/512/1077/1077114.png'
    RAG_LOGO = 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQGOu-9Cw5nSKEO_Y-sNhgFiL88d-OWc-fOYQ&s'
    
    @classmethod
    def apply_custom_css(cls):
        """Apply custom CSS styles to the application"""
        ui.add_head_html('''
<style>
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700&display=swap');
body { font-family: 'Montserrat', Arial, sans-serif; }
.hero-title { font-size:2.5rem; font-weight:bold; color:#222; margin-bottom:8px; animation:slidein 1s; }
.hero-subtitle { font-size:1.2rem; color:#006C35; margin-bottom:24px; animation:fadein 2s; }
.fadein { animation:fadein 1.5s; }
@keyframes fadein { from { opacity:0; } to { opacity:1; } }
@keyframes slidein { from { opacity:0; transform:translateY(40px);} to { opacity:1; transform:translateY(0);} }
@keyframes typing { from { width:0; } to { width:100%; } }
@keyframes blink { 0%, 50% { border-color:transparent; } 100% { border-color:#006C35; } }
.stat-card { background:#fff; border-radius:16px; box-shadow:0 2px 8px #0001; padding:18px 28px; margin:0 12px; display:flex; align-items:center; gap:12px; min-width:180px; transition:transform 0.3s, box-shadow 0.3s; }
.stat-card:hover { transform:translateY(-5px); box-shadow:0 8px 25px #0002; }
.stat-icon { font-size:2rem; color:#006C35; }
.stat-label { font-size:1.1rem; color:#222; }
.stat-value { font-size:1.5rem; color:#006C35; font-weight:bold; }
.chat-glow { box-shadow:0 0 16px 2px #006C3588, 0 2px 8px #0003; transition:box-shadow 0.3s, transform 0.3s; }
.chat-glow:hover { box-shadow:0 0 32px 6px #006C35cc, 0 2px 8px #0003; transform:scale(1.1); }
.chat-message { background:#f8f9fa; border-radius:12px; padding:12px; margin:8px 0; border-left:4px solid #006C35; animation:slidein 0.5s; }
.chat-input { border-radius:20px; border:2px solid #e0e0e0; transition:all 0.3s ease; background:#fff; box-shadow:0 2px 8px rgba(0,0,0,0.1); font-family:'Montserrat', Arial, sans-serif; }
.chat-input:focus { border-color:#006C35; box-shadow:0 0 0 3px #006C3533, 0 4px 12px rgba(0,108,53,0.2); outline:none; transform:translateY(-1px); }
.chat-input::placeholder { color:#999; font-style:italic; opacity:0.8; }
.chat-input:hover { border-color:#006C35; box-shadow:0 4px 12px rgba(0,108,53,0.1); }
.typing-indicator { display:inline-block; width:20px; height:20px; border:2px solid #006C35; border-radius:50%; border-top-color:transparent; animation:spin 1s linear infinite; }
@keyframes spin { to { transform:rotate(360deg); } }
.pulse { animation:pulse 2s infinite; }
@keyframes pulse { 0% { transform:scale(1); } 50% { transform:scale(1.05); } 100% { transform:scale(1); } }
.message-container { display:flex; align-items:flex-start; gap:8px; margin:6px 0; }
.message-avatar { width:32px; height:32px; border-radius:50%; object-fit:cover; }
.message-content { flex:1; background:#006C35; color:white; border-radius:12px; padding:12px; border-left:4px solid #006C35; }
.user-message { background:#006C35; color:white; border-left-color:#00A651; }
.rag-message { background:#006C35; color:white; border-left-color:#006C35; }
.follow-up-suggestions { margin-top:8px; display:flex; flex-wrap:wrap; gap:8px; }
.follow-up-btn { background:#006C35; color:white; border:1px solid white; border-radius:16px; padding:8px 16px; font-size:0.9rem; cursor:pointer; transition:all 0.3s; }
.follow-up-btn:hover { background:white; color:#006C35; }
/* Improved text readability */
.message-content { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; font-size: 14px; line-height: 1.6; }
.chat-output { font-weight: 400; letter-spacing: 0.3px; }
/* Saudi-themed interactive styles */
.gradient-header { background: linear-gradient(135deg, #006C35 0%, #004D25 50%, #006C35 100%); color:white; box-shadow:0 4px 20px rgba(0,108,53,0.3); }
.floating-animation { animation: float 3s ease-in-out infinite; }
@keyframes float { 0%, 100% { transform: translateY(0px); } 50% { transform: translateY(-10px); } }
.bounce-in { animation: bounceIn 0.8s ease-out; }
@keyframes bounceIn { 0% { transform: scale(0.3); opacity: 0; } 50% { transform: scale(1.05); } 70% { transform: scale(0.9); } 100% { transform: scale(1); opacity: 1; } }
.shimmer { background: linear-gradient(90deg, transparent, rgba(255,255,255,0.4), transparent); background-size: 200% 100%; animation: shimmer 2s infinite; }
@keyframes shimmer { 0% { background-position: -200% 0; } 100% { background-position: 200% 0; } }
.interactive-card { transition: all 0.3s ease; cursor: pointer; }
.interactive-card:hover { transform: translateY(-8px) scale(1.02); box-shadow: 0 12px 30px rgba(0,108,53,0.2); }
.glow-effect { position: relative; }
.glow-effect::before { content: ''; position: absolute; top: -2px; left: -2px; right: -2px; bottom: -2px; background: linear-gradient(45deg, #006C35, #00A651, #006C35); border-radius: inherit; z-index: -1; opacity: 0; transition: opacity 0.3s; }
.glow-effect:hover::before { opacity: 1; }
.personalized-welcome { background: linear-gradient(135deg, #006C35, #004D25); color: white; border-radius: 12px; padding: 16px; margin: 8px 0; animation: slidein 0.8s; }
/* Utility buttons at top */
.utility-buttons { display: flex; gap: 8px; justify-content: flex-end; margin: 8px; }
.utility-btn { border-radius: 50%; width: 32px; height: 32px; display: flex; align-items: center; justify-content: center; background: #006C35; color: white; border: none; cursor: pointer; transition: all 0.3s; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }
.utility-btn:hover { transform: translateY(-2px); box-shadow: 0 4px 8px rgba(0,0,0,0.2); background: #004D25; }
.utility-btn svg { width: 16px; height: 16px; }
/* Arabic text support */
.rag-message, .user-message, .message-content { 
    direction: auto; 
    text-align: left; 
    font-family: 'Montserrat', 'Arial', 'Segoe UI', sans-serif;
    line-height: 1.5;
    word-wrap: break-word;
    overflow-wrap: break-word;
}
/* Ensure proper Arabic text rendering */
[lang="ar"], .arabic-text { 
    direction: rtl; 
    text-align: right; 
    font-family: 'Arial', 'Segoe UI', sans-serif;
}
/* Chat area improvements */
.chat-area { 
    direction: auto; 
    text-align: left; 
    font-family: 'Montserrat', 'Arial', 'Segoe UI', sans-serif;
    line-height: 1.5;
    word-wrap: break-word;
    overflow-wrap: break-word;
    border-top: none;
    border-bottom: none;
    scrollbar-width: thin;
    scrollbar-color: rgba(0,108,53,0.5) transparent;
}

.chat-area::-webkit-scrollbar {
    width: 4px;
}

.chat-area::-webkit-scrollbar-thumb {
    background-color: rgba(0,108,53,0.5);
    border-radius: 4px;
}
/* Saudi-themed placeholders */
.input-wrapper { position: relative; width: 100%; margin: 0; }
.input-wrapper input:focus::placeholder { opacity: 0; }
/* Header button styles */
.header-button {
    background: #006C35 !important;
    color: white;
    border: none;
    min-width: 40px;
    width: 40px;
    height: 40px;
    padding: 0;
    border-radius: 50%;
    transition: background-color 0.2s, transform 0.2s;
    display: flex;
    align-items: center;
    justify-content: center;
}

.header-button:hover {
    background-color: #008040 !important;
    transform: scale(1.1);
}

.header-button:active {
    background-color: #005030 !important;
    transform: scale(0.95);
}

/* Improved header styling */
.chat-header {
    background: #006C35;
    border-radius: 12px 12px 0 0;
    margin: 0;
    padding: 0;
}
</style>
        ''')
    
    @classmethod
    def apply_particles_background(cls):
        """Apply animated particles background effect"""
        ui.add_head_html('''
<div id="particles-js" style="position:fixed; top:0; left:0; width:100%; height:100%; z-index:-1; pointer-events:none;"></div>
<script src="https://cdn.jsdelivr.net/particles.js/2.0.0/particles.min.js"></script>
<script>
particlesJS('particles-js', {
  particles: {
    number: { value: 50, density: { enable: true, value_area: 800 } },
    color: { value: '#bfa046' },
    shape: { type: 'circle' },
    opacity: { value: 0.3, random: false },
    size: { value: 3, random: true },
    line_linked: { enable: true, distance: 150, color: '#bfa046', opacity: 0.2, width: 1 },
    move: { enable: true, speed: 2, direction: 'none', random: false, straight: false, out_mode: 'out', bounce: false }
  },
  interactivity: {
    detect_on: 'canvas',
    events: { onhover: { enable: true, mode: 'repulse' }, onclick: { enable: true, mode: 'push' }, resize: true },
    modes: { repulse: { distance: 100, duration: 0.4 }, push: { particles_nb: 4 } }
  },
  retina_detect: true
});
</script>
        ''')
    
    @classmethod
    def set_body_background(cls):
        """Set the main body background gradient"""
        ui.query('body').style(f'background:linear-gradient(135deg, {cls.PIF_BEIGE} 60%, #fff 100%);')
    
    @classmethod
    def add_input_placeholder_script(cls):
        """Add JavaScript for enhanced input placeholder behavior"""
        ui.add_body_html("""
        <script>
        document.addEventListener('DOMContentLoaded', function() {
            setTimeout(function() {
                const inputs = document.querySelectorAll('.chat-input input');
                inputs.forEach(input => {
                    input.addEventListener('focus', function() {
                        if (this.placeholder) {
                            this.dataset.placeholder = this.placeholder;
                            this.placeholder = '';
                        }
                    });
                    input.addEventListener('blur', function() {
                        if (!this.value && this.dataset.placeholder) {
                            this.placeholder = this.dataset.placeholder;
                        }
                    });
                });
            }, 1000);
        });
        </script>
        """)