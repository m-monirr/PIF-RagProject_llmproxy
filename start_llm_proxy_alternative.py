"""
Alternative LLM Proxy startup using direct Python import
Bypasses CLI compatibility issues with Python 3.13
"""

import logging
import sys
from pathlib import Path
import yaml

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    print("🚀 Starting LLM Proxy Server (Direct Import Method)...")
    print("This bypasses CLI issues and works with Python 3.13")
    print("Press Ctrl+C to stop\n")
    
    try:
        # Import required modules
        import uvicorn
        from litellm.proxy.proxy_server import app, initialize
        
        # Set config file path
        config_file = Path("llm_proxy_config.yaml")
        
        if not config_file.exists():
            print(f"❌ Config file not found: {config_file}")
            print("Please ensure llm_proxy_config.yaml exists in the project root")
            sys.exit(1)
        
        print(f"📋 Using config: {config_file.absolute()}")
        print(f"🌐 Connecting to Groq (Primary) + Ollama Cloud (Fallback)\n")
        
        # Load config
        with open(config_file, 'r') as f:
            config = yaml.safe_load(f)
        
        # Initialize the proxy
        logger.info("Initializing LiteLLM proxy...")
        initialize(
            model=None,
            alias=None,
            api_base=None,
            api_version=None,
            debug=False,
            temperature=None,
            max_tokens=None,
            request_timeout=600,
            max_budget=None,
            telemetry=False,
            drop_params=True,
            add_function_to_prompt=False,
            headers=None,
            save=False,
            config=str(config_file.absolute()),
            use_queue=False
        )
        
        print("\n✅ LLM Proxy initialized successfully!")
        print("   📍 Base URL: http://0.0.0.0:4000")
        print("   🤖 Primary: Groq (llama3-8b-8192) - FREE & FAST!")
        print("   🔄 Fallback: Ollama Cloud (qwen2.5:3b, llama3.2:3b)\n")
        print("Now you can start the main application with: streamlit run app.py\n")
        
        # Run the server on port 4000
        uvicorn.run(
            app,
            host="0.0.0.0",
            port=4000,
            log_level="info",
            access_log=False
        )
        
    except ImportError as e:
        print(f"\n❌ Failed to import required modules: {e}")
        print("\nPlease install required packages:")
        print("  pip install 'litellm[proxy]' uvicorn pyyaml")
        sys.exit(1)
        
    except Exception as e:
        print(f"\n❌ Error starting LLM proxy: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
        
    except KeyboardInterrupt:
        print("\n\n🛑 Stopping LLM Proxy...")
        print("✅ Proxy stopped successfully")
