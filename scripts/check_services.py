"""
Check if all required services are running
"""

import requests
import sys
import os
from dotenv import load_dotenv
from pathlib import Path

def check_service(name, url, description):
    """Check if a service is running"""
    try:
        response = requests.get(url, timeout=3)
        if response.status_code == 200:
            print(f"✅ {name:20} → Running at {url}")
            return True
        else:
            print(f"❌ {name:20} → Not responding (HTTP {response.status_code})")
            return False
    except requests.exceptions.ConnectionError:
        print(f"❌ {name:20} → Not running")
        print(f"   💡 {description}")
        return False
    except Exception as e:
        print(f"⚠️  {name:20} → Error: {str(e)[:50]}")
        return False

def check_env_keys():
    """Check if required API keys are set"""
    # Load environment
    env_path = Path(__file__).parent.parent / "config" / ".env"
    load_dotenv(dotenv_path=env_path)
    
    print("\n4️⃣ Checking Environment Variables...")
    
    groq_key = os.getenv("GROQ_API_KEY")
    if not groq_key or groq_key == "your-groq-api-key-here":
        print("❌ GROQ_API_KEY not set or using placeholder")
        print("   💡 Get free key: https://console.groq.com/keys")
        print("   💡 Add to: config/.env")
        return False
    else:
        print(f"✅ GROQ_API_KEY is set ({groq_key[:10]}...)")
    
    return True

def main():
    """Run all service checks"""
    print("\n" + "="*70)
    print("🔍 Checking PIF RAG Chat Services...\n")
    print("="*70)
    
    all_ok = True
    
    services = {
        "Ollama (Embeddings)": {
            "url": "http://localhost:11434/api/version",
            "help": "Start: ollama serve (or auto-starts on Windows)"
        },
        "Qdrant (Vector DB)": {
            "url": "http://localhost:6333/collections",
            "help": "Start: python scripts/start_qdrant.py"
        },
        "LLM Proxy (Answers)": {
            "url": "http://localhost:4000/health",
            "help": "Start: python scripts/start_llm_proxy.py"
        }
    }
    
    # Check environment variables (NEW)
    if not check_env_keys():
        all_ok = False
    print()
    
    # Check Ollama (embeddings)
    if not check_service("Ollama (Embeddings)", "http://localhost:11434/api/version", "Start: ollama serve (or auto-starts on Windows)"):
        all_ok = False
    
    # Check Qdrant (Vector DB)
    if not check_service("Qdrant (Vector DB)", "http://localhost:6333/collections", "Start: python scripts/start_qdrant.py"):
        all_ok = False
    
    # Check LLM Proxy (Answers)
    if not check_service("LLM Proxy (Answers)", "http://localhost:4000/health", "Start: python scripts/start_llm_proxy.py"):
        all_ok = False
    
    print("\n" + "="*70)
    if all_ok:
        print("✅ ALL SERVICES RUNNING")
        print("="*70)
        print("\n🚀 You can now:")
        print("   1. Process documents: python -m scripts.process_documents")
        print("   2. Start app: streamlit run app.py")
    else:
        print("⚠️  SOME SERVICES NOT RUNNING")
        print("="*70)
        print("\n📋 Quick Start Guide:")
        print("   1. Start Qdrant: python scripts/start_qdrant.py")
        print("   2. Start LLM Proxy: python scripts/start_llm_proxy.py")
        print("   3. Check Ollama: ollama list")
        print("   4. Run this check again: python scripts/check_services.py")
    
    print("="*70 + "\n")
    
    return 0 if all_ok else 1

if __name__ == "__main__":
    sys.exit(main())
