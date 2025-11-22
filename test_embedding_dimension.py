import ollama
import numpy as np

def test_qwen_embedding():
    """Test Qwen3-embedding model and display embedding information"""
    print("🔍 Testing Qwen3-embedding model...\n")
    
    try:
        # Initialize Ollama client
        client = ollama.Client(host='http://localhost:11434')
        
        # Test with a sample text
        test_text = "This is a test to check the embedding dimension"
        
        print(f"📝 Test text: '{test_text}'")
        print("\n⏳ Generating embedding...\n")
        
        # Get embedding
        response = client.embeddings(
            model='qwen3-embedding',
            prompt=test_text
        )
        
        if 'embedding' in response:
            embedding = response['embedding']
            dimension = len(embedding)
            
            print("✅ Success! Embedding generated successfully\n")
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
            arabic_text = "هذا اختبار للتحقق من دعم اللغة العربية"
            arabic_response = client.embeddings(
                model='qwen3-embedding',
                prompt=arabic_text
            )
            
            if 'embedding' in arabic_response:
                arabic_embedding = arabic_response['embedding']
                arabic_dimension = len(arabic_embedding)
                print(f"✅ Arabic embedding dimension: {arabic_dimension}")
                print(f"📊 Matches English dimension: {dimension == arabic_dimension}")
            
            # Recommendation
            print("\n" + "="*60)
            print("📝 CONFIGURATION UPDATE NEEDED:")
            print("="*60)
            print(f"\nUpdate your config.py file with:")
            print(f"\n  EMBED_MODEL_ID = 'qwen3-embedding'")
            print(f"  EMBED_DIMENSION = {dimension}")
            print("\n" + "="*60)
            
            return dimension
        else:
            print("❌ Error: No embedding in response")
            print(f"Response: {response}")
            return None
            
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\n💡 Troubleshooting:")
        print("1. Make sure Ollama is running: ollama serve")
        print("2. Make sure the model is pulled: ollama pull qwen3-embedding")
        print("3. Check Ollama status: curl http://localhost:11434/api/version")
        return None

if __name__ == "__main__":
    dimension = test_qwen_embedding()
    
    if dimension:
        print(f"\n✨ Test completed successfully!")
        print(f"🎯 Use EMBED_DIMENSION = {dimension} in your config.py")
    else:
        print("\n❌ Test failed. Please check the troubleshooting steps above.")
