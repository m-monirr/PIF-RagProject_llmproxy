"""
LLM Proxy startup script - Using litellm CLI
"""

import sys
import subprocess
from pathlib import Path
import shutil
from dotenv import load_dotenv

if __name__ == "__main__":
    # FIXED: Use absolute path relative to this script
    project_root = Path(__file__).parent.parent
    config_file = project_root / "config" / "llm_proxy_config.yaml"
    env_file = project_root / "config" / ".env"
    
    # CRITICAL: Load environment variables
    if env_file.exists():
        load_dotenv(dotenv_path=env_file)
        print(f"✅ Loaded environment from {env_file.name}")
    else:
        print(f"⚠️  Warning: {env_file} not found!")
    
    if not config_file.exists():
        print(f"❌ Config file not found: {config_file}")
        print("Please ensure llm_proxy_config.yaml exists in the config/ folder")
        sys.exit(1)
    
    print("🚀 Starting LLM Proxy Server...")
    print(f"📋 Config: {config_file.name}")
    print(f"🌐 Groq (Primary) + Ollama Cloud (Fallback)\n")
    
    # Check if litellm command exists
    litellm_cmd = shutil.which("litellm")
    
    if litellm_cmd:
        # Use litellm CLI directly
        cmd = [
            "litellm",
            "--config", str(config_file.absolute()),
            "--port", "4000"
        ]
    else:
        # Fallback: try using uvicorn to run the proxy directly
        print("⚠️  'litellm' command not found, using alternative method...\n")
        cmd = [
            sys.executable, "-c",
            f"""
import sys
import os
os.environ['LITELLM_CONFIG_PATH'] = r'{config_file.absolute()}'
from litellm.proxy.proxy_server import app
import uvicorn
uvicorn.run(app, host='0.0.0.0', port=4000, log_level='info')
"""
        ]
    
    try:
        print(f"Starting LLM proxy on http://localhost:4000")
        print("="*70)
        print("Press Ctrl+C to stop")
        print("="*70 + "\n")
        
        # Run the proxy
        subprocess.run(cmd, check=True)
        
    except KeyboardInterrupt:
        print("\n\n🛑 Stopping LLM Proxy...")
        print("✅ Proxy stopped successfully")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\n💡 Alternative: Run manually with:")
        print(f"   litellm --config {config_file.absolute()} --port 4000")
        sys.exit(1)
