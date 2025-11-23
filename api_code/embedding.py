import numpy as np
import ollama
from typing import List, Union
import logging
from .config import EMBEDDING_PROVIDER, EMBED_MODEL_ID, OLLAMA_BASE_URL, EMBED_DIMENSION

logger = logging.getLogger(__name__)

# Initialize Ollama client as singleton (reuse connection)
_ollama_client = None

def get_ollama_client():
    """Get or create Ollama client (singleton pattern)"""
    global _ollama_client
    if _ollama_client is None:
        try:
            _ollama_client = ollama.Client(host=OLLAMA_BASE_URL)
            logger.info(f"✅ Ollama client initialized at {OLLAMA_BASE_URL}")
        except Exception as e:
            logger.error(f"Failed to initialize Ollama client: {e}")
            raise RuntimeError(f"Could not connect to Ollama: {e}")
    return _ollama_client

def embed(texts: Union[str, List[str]], model=None, tokenizer=None, batch_size=4) -> np.ndarray:
    """
    Embed texts using Ollama's qwen3-embedding model (optimized for memory)
    
    Args:
        texts: Single text or list of texts to embed
        batch_size: Reduced to 4 to save memory (was 8)
        
    Returns:
        numpy array of embeddings normalized to unit length
    """
    client = get_ollama_client()
    
    # Handle single string input
    if isinstance(texts, str):
        texts = [texts]
    
    embeddings = []
    total_texts = len(texts)
    
    # Process in smaller batches to reduce memory usage
    for i in range(0, total_texts, batch_size):
        batch = texts[i:i + batch_size]
        
        try:
            for text in batch:
                # Call Ollama embedding API
                response = client.embeddings(
                    model=EMBED_MODEL_ID,
                    prompt=text,
                    options={
                        "num_thread": 4,  # Limit CPU threads to save resources
                    }
                )
                
                # Extract embedding from response
                if 'embedding' in response:
                    embeddings.append(response['embedding'])
                else:
                    logger.warning(f"No embedding in response for text: {text[:50]}...")
                    embeddings.append([0.0] * EMBED_DIMENSION)
                    
        except Exception as e:
            logger.error(f"Error embedding batch {i//batch_size + 1}: {e}")
            # Add zero vectors for failed embeddings
            for _ in range(len(batch)):
                embeddings.append([0.0] * EMBED_DIMENSION)
        
        # Log progress
        if (i + batch_size) % 20 == 0 or (i + batch_size) >= total_texts:
            logger.info(f"Embedded {min(i + batch_size, total_texts)}/{total_texts} texts")
    
    # Convert to numpy array
    embeddings = np.array(embeddings, dtype=np.float32)
    
    # Normalize embeddings to unit length for cosine similarity
    norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
    norms = np.where(norms == 0, 1, norms)
    embeddings = embeddings / norms
    
    return embeddings

def embed_query(text: str, model=None, tokenizer=None) -> np.ndarray:
    """Embed a single query using qwen3-embedding"""
    client = get_ollama_client()
    
    try:
        response = client.embeddings(
            model=EMBED_MODEL_ID,
            prompt=text,
            options={
                "num_thread": 4,
            }
        )
        
        if 'embedding' in response:
            vec = np.array([response['embedding']], dtype=np.float32)
        else:
            logger.warning(f"No embedding in response for query: {text[:50]}...")
            vec = np.zeros((1, EMBED_DIMENSION), dtype=np.float32)
        
        # Normalize to unit length
        norm = np.linalg.norm(vec)
        if norm > 0:
            vec = vec / norm
            
        return vec
        
    except Exception as e:
        logger.error(f"Error embedding query: {e}")
        return np.zeros((1, EMBED_DIMENSION), dtype=np.float32)
