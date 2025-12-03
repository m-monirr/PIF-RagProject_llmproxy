"""
Check if all required services are running
"""

import requests
import sys

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

def main():
    print("\n" + "="*70)
    print("🔍 SERVICE STATUS CHECK")
    print("="*70 + "\n")
    
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
    
    all_running = True
    for name, info in services.items():
        if not check_service(name, info["url"], info["help"]):
            all_running = False
    
    print("\n" + "="*70)
    if all_running:
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
    
    return 0 if all_running else 1

if __name__ == "__main__":
    sys.exit(main())
