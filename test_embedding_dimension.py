import ollama
import numpy as np
import os

def test_qwen_embedding():
    """Test Qwen3-embedding model and display embedding information"""
    print("🔍 Testing qwen3-embedding model (Local Ollama)...\n")
    
    # Get configuration
    ollama_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    
    try:
        # Initialize Ollama client for local server
        print(f"🏠 Connecting to Local Ollama: {ollama_url}")
        client = ollama.Client(host=ollama_url)
        
        # Test with a sample text
        test_text = "This is a test to check the embedding dimension for qwen3-embedding"
        
        print(f"📝 Test text: '{test_text}'")
        print("\n⏳ Generating embedding...\n")
        
        # Get embedding with qwen3-embedding model
        try:
            response = client.embeddings(
                model='qwen3-embedding',
                prompt=test_text
            )
            model_used = 'qwen3-embedding'
        except Exception as e:
            print(f"❌ Error: {e}")
            print("\n💡 Model not found. Please pull it first:")
            print("   ollama pull qwen3-embedding")
            print("\nOR try an alternative:")
            print("   ollama pull nomic-embed-text")
            print("   ollama pull mxbai-embed-large")
            return None
        
        if 'embedding' in response:
            embedding = response['embedding']
            dimension = len(embedding)
            
            print("✅ Success! Embedding generated successfully\n")
            print(f"🤖 Model used: {model_used}")
            print(f"📊 Embedding Dimension: {dimension}")
            print(f"📏 Embedding shape: ({dimension},)")
            print(f"🔢 Data type: {type(embedding[0])}")
            print(f"\n📈 First 10 values: {embedding[:10]}")
            print(f"📉 Last 10 values: {embedding[-10:]}")
            
            # Calculate statistics
            arr = np.array(embedding)
            print(f"\n📊 Statistics:")
            print(f"   - Mean: {np.mean(arr):.6f}")
            print(f"   - Std Dev: {np.std(arr):.6f}")
            print(f"   - Min: {np.min(arr):.6f}")
            print(f"   - Max: {np.max(arr):.6f}")
            print(f"   - L2 Norm: {np.linalg.norm(arr):.6f}")
            
            # Test with Arabic text
            print("\n🇸🇦 Testing with Arabic text...")
            arabic_text = "هذا اختبار للتحقق من دعم اللغة العربية في نموذج qwen3-embedding"
            arabic_response = client.embeddings(
                model=model_used,
                prompt=arabic_text
            )
            
            if 'embedding' in arabic_response:
                arabic_embedding = arabic_response['embedding']
                arabic_dimension = len(arabic_embedding)
                print(f"✅ Arabic embedding dimension: {arabic_dimension}")
                print(f"📊 Dimensions match: {dimension == arabic_dimension}")
            
            # Recommendation
            print("\n" + "="*60)
            print("📝 CONFIGURATION UPDATE:")
            print("="*60)
            print(f"\nUpdate your config.py file with:")
            print(f"\n  EMBEDDING_PROVIDER = 'ollama'")
            print(f"  EMBED_MODEL_ID = '{model_used}'")
            print(f"  EMBED_DIMENSION = {dimension}")
            print(f"  OLLAMA_BASE_URL = '{ollama_url}'")
            print("\n🏠 Using Local Ollama - No cloud API needed!")
            print("="*60)
            
            return dimension, model_used
        else:
            print("❌ Error: No embedding in response")
            print(f"Response: {response}")
            return None
            
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\n💡 Troubleshooting:")
        print("1. Make sure Ollama is installed: https://ollama.com/download")
        print("2. Start Ollama service:")
        print("   Windows: Ollama starts automatically after installation")
        print("   Mac/Linux: ollama serve")
        print("3. Pull the qwen3-embedding model:")
        print("   ollama pull qwen3-embedding")
        print("4. Check Ollama is running:")
        print("   curl http://localhost:11434/api/version")
        print("5. List available models:")
        print("   ollama list")
        return None

if __name__ == "__main__":
    result = test_qwen_embedding()
    
    if result:
        dimension, model = result
        print(f"\n✨ Test completed successfully!")
        print(f"🎯 Use EMBED_DIMENSION = {dimension} and EMBED_MODEL_ID = '{model}' in your config.py")
    else:
        print("\n❌ Test failed. Please check the troubleshooting steps above.")
