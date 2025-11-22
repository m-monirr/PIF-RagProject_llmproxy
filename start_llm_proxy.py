"""
Standalone script to start the LLM proxy server
Run this before starting the main application
"""

import logging
from api_code.llm_proxy import LLMProxyManager

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

if __name__ == "__main__":
    print("🚀 Starting LLM Proxy Server...")
    print("This will handle answer generation with automatic fallback")
    print("Press Ctrl+C to stop\n")
    
    proxy = LLMProxyManager()
    
    try:
        if proxy.start_proxy():
            print("\n✅ LLM Proxy is running!")
            print(f"   Base URL: {proxy.base_url}")
            print("   Models: Ollama Cloud (qwen2.5:3b) → Ollama Cloud (llama3.2:3b) → Local Ollama")
            print("\nNow you can start the main application with: python rag_chat_ui.py\n")
            
            # Keep running
            import time
            while True:
                time.sleep(1)
        else:
            print("\n❌ Failed to start LLM proxy")
            print("Please check:")
            print("1. litellm is installed: pip install 'litellm[proxy]'")
            print("2. Config file exists: llm_proxy_config.yaml")
            
    except KeyboardInterrupt:
        print("\n\n🛑 Stopping LLM Proxy...")
        proxy.stop_proxy()
        print("✅ Proxy stopped successfully")
