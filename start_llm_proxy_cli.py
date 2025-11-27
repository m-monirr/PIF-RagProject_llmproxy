"""
LLM Proxy startup using CLI command
More reliable than direct import

IMPORTANT: Keep this terminal open while using the application!
"""

import subprocess
import sys
from pathlib import Path
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

if __name__ == "__main__":
    print("🚀 Starting LLM Proxy Server (CLI Method)...")
    print("⚠️  IMPORTANT: Keep this terminal window open!")
    print("   Do NOT close it while using the application!")
    print("   Press Ctrl+C only when you want to stop the proxy.\n")
    
    # Check for Groq API key
    groq_key = os.getenv("GROQ_API_KEY")
    if not groq_key or groq_key == "your-groq-api-key-here":
        print("❌ ERROR: GROQ_API_KEY not set in .env file!")
        print("\nPlease:")
        print("1. Get your free API key from: https://console.groq.com/keys")
        print("2. Add it to .env file: GROQ_API_KEY=gsk_your_actual_key")
        input("\nPress Enter to exit...")
        sys.exit(1)
    
    print(f"✅ Groq API key found: {groq_key[:10]}...")
    
    config_file = Path("llm_proxy_config.yaml")
    
    if not config_file.exists():
        print(f"❌ Config file not found: {config_file}")
        input("\nPress Enter to exit...")
        sys.exit(1)
    
    print(f"📋 Using config: {config_file.absolute()}")
    print(f"🌐 Connecting to Groq (Primary) + Ollama Cloud (Fallback)\n")
    
    # Use subprocess to call litellm CLI
    cmd = [
        "litellm",
        "--config", str(config_file.absolute()),
        "--port", "4000",
        "--host", "0.0.0.0"
    ]
    
    print(f"Running: {' '.join(cmd)}\n")
    
    try:
        # Run and stream output
        process = subprocess.Popen(
            cmd,
            stdout=sys.stdout,
            stderr=sys.stderr,
            text=True
        )
        
        print("\n" + "="*60)
        print("✅ LLM Proxy is starting...")
        print("   Wait 10-15 seconds for full initialization")
        print("   Then start Streamlit: streamlit run app.py")
        print("="*60 + "\n")
        
        # Wait for process to complete
        process.wait()
        
    except KeyboardInterrupt:
        print("\n\n🛑 Stopping LLM Proxy...")
        process.terminate()
        process.wait()
        print("✅ Proxy stopped successfully")
        print("\nYou can now close this window.")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        input("\nPress Enter to exit...")
        sys.exit(1)
