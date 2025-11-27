"""
Quick health check script for all required services
Run this before starting the application
"""

import requests
import sys
import subprocess

def check_service(name, url, timeout=5):
    """Check if a service is running"""
    try:
        response = requests.get(url, timeout=timeout)
        if response.status_code == 200:
            print(f"✅ {name} is running at {url}")
            return True
        else:
            print(f"⚠️  {name} responded with status {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print(f"❌ {name} is NOT running at {url}")
        return False
    except Exception as e:
        print(f"❌ {name} check failed: {e}")
        return False

def check_ollama_model():
    """Check if required Ollama model is available"""
    try:
        result = subprocess.run(
            ["ollama", "list"],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        if "qwen3-embedding" in result.stdout:
            print("✅ Ollama model 'qwen3-embedding' is available")
            return True
        else:
            print("❌ Ollama model 'qwen3-embedding' NOT found")
            print("   Run: ollama pull qwen3-embedding")
            return False
    except FileNotFoundError:
        print("❌ Ollama is not installed or not in PATH")
        return False
    except Exception as e:
        print(f"❌ Ollama model check failed: {e}")
        return False

def main():
    """Run all service checks"""
    print("🔍 Checking PIF RAG Chat Services...\n")
    
    all_ok = True
    
    # Check Ollama (embeddings)
    print("1️⃣ Checking Ollama (Embeddings)...")
    if not check_service("Ollama", "http://localhost:11434/api/version"):
        all_ok = False
        print("   💡 Start with: ollama serve")
    if not check_ollama_model():
        all_ok = False
    print()
    
    # Check Qdrant (vector database)
    print("2️⃣ Checking Qdrant (Vector Database)...")
    if not check_service("Qdrant", "http://localhost:6333/collections"):
        all_ok = False
        print("   💡 Start with: docker run -d -p 6333:6333 -p 6334:6334 -v \"%cd%\\qdrant_storage\":/qdrant/storage qdrant/qdrant")
    print()
    
    # Check LLM Proxy (answer generation) - FIXED PORT
    print("3️⃣ Checking LLM Proxy (Answer Generation)...")
    if not check_service("LLM Proxy", "http://localhost:4000/health"):
        all_ok = False
        print("   💡 Start with: python start_llm_proxy_alternative.py")
    print()
    
    # Summary
    print("=" * 50)
    if all_ok:
        print("🎉 All services are running!")
        print("\n✅ You can now start the application:")
        print("   streamlit run app.py")
    else:
        print("⚠️  Some services are not running!")
        print("\n📋 Please start the missing services above")
        print("   See RUN_GUIDE.md for detailed instructions")
    print("=" * 50)
    
    return 0 if all_ok else 1

if __name__ == "__main__":
    sys.exit(main())
