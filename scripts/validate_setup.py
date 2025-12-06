"""
Pre-flight validation script - Check all prerequisites before starting
Run this to ensure everything is properly configured
"""

import sys
from pathlib import Path
import os
from dotenv import load_dotenv

# Load environment
env_path = Path(__file__).parent.parent / "config" / ".env"
load_dotenv(dotenv_path=env_path)

def check_env_file():
    """Check if .env file exists and is configured"""
    if not env_path.exists():
        print("❌ config/.env file not found!")
        print("   💡 Copy config/.env.example to config/.env")
        return False
    
    print("✅ config/.env file exists")
    return True

def check_api_keys():
    """Validate API keys are set"""
    groq_key = os.getenv("GROQ_API_KEY")
    
    if not groq_key or groq_key == "your-groq-api-key-here":
        print("❌ GROQ_API_KEY not configured")
        print("   💡 Get free key: https://console.groq.com/keys")
        print("   💡 Add to config/.env: GROQ_API_KEY=gsk_...")
        return False
    
    print(f"✅ GROQ_API_KEY is configured ({groq_key[:15]}...)")
    return True

def check_config_files():
    """Check required config files exist"""
    project_root = Path(__file__).parent.parent
    config_file = project_root / "config" / "llm_proxy_config.yaml"
    
    if not config_file.exists():
        print(f"❌ {config_file.name} not found")
        return False
    
    print(f"✅ {config_file.name} exists")
    return True

def check_data_directories():
    """Ensure data directories exist"""
    project_root = Path(__file__).parent.parent
    
    dirs = {
        "PDFs": project_root / "data" / "pdfs",
        "Outputs": project_root / "data" / "outputs",
        "Qdrant": project_root / "data" / "qdrant_storage"
    }
    
    all_ok = True
    for name, dir_path in dirs.items():
        if not dir_path.exists():
            print(f"⚠️  {name} directory missing, creating: {dir_path}")
            dir_path.mkdir(parents=True, exist_ok=True)
        else:
            print(f"✅ {name} directory exists")
    
    return all_ok

def check_pdf_files():
    """Check if PDF files are present"""
    project_root = Path(__file__).parent.parent
    pdfs_dir = project_root / "data" / "pdfs"
    
    if not pdfs_dir.exists():
        print("⚠️  data/pdfs/ directory not found")
        return False
    
    pdf_files = list(pdfs_dir.glob("*.pdf"))
    
    if len(pdf_files) == 0:
        print("⚠️  No PDF files found in data/pdfs/")
        print("   💡 Add PIF annual report PDFs to data/pdfs/")
        return False
    
    print(f"✅ Found {len(pdf_files)} PDF file(s)")
    for pdf in pdf_files[:3]:  # Show first 3
        print(f"   • {pdf.name}")
    
    return True

def check_python_version():
    """Check Python version"""
    version = sys.version_info
    
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print(f"❌ Python {version.major}.{version.minor} detected")
        print("   💡 Requires Python 3.8 or higher")
        return False
    
    print(f"✅ Python {version.major}.{version.minor}.{version.micro}")
    return True

def main():
    """Run all validation checks"""
    print("\n" + "="*70)
    print("🔍 PIF RAG CHAT - PRE-FLIGHT VALIDATION")
    print("="*70 + "\n")
    
    checks = [
        ("Python Version", check_python_version),
        ("Environment File", check_env_file),
        ("API Keys", check_api_keys),
        ("Config Files", check_config_files),
        ("Data Directories", check_data_directories),
        ("PDF Files", check_pdf_files)
    ]
    
    results = []
    
    for name, check_func in checks:
        print(f"\n📋 Checking: {name}")
        print("-" * 70)
        result = check_func()
        results.append((name, result))
        print()
    
    # Summary
    print("=" * 70)
    print("📊 VALIDATION SUMMARY")
    print("=" * 70)
    
    passed = sum(1 for _, r in results if r)
    total = len(results)
    
    for name, result in results:
        status = "✅" if result else "❌"
        print(f"{status} {name}")
    
    print(f"\n{passed}/{total} checks passed")
    
    if passed == total:
        print("\n🎉 ALL CHECKS PASSED!")
        print("\n🚀 Next steps:")
        print("   1. Check services: python scripts/check_services.py")
        print("   2. Process documents: python scripts/process_documents.py")
        print("   3. Start app: streamlit run app.py")
    else:
        print("\n⚠️  SOME CHECKS FAILED")
        print("   Please fix the issues above before proceeding")
        return 1
    
    print("=" * 70 + "\n")
    return 0

if __name__ == "__main__":
    sys.exit(main())
