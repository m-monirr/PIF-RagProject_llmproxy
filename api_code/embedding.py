import numpy as np
import ollama
from typing import List, Union
import logging
from .config import EMBEDDING_PROVIDER, EMBED_MODEL_ID, OLLAMA_BASE_URL

logger = logging.getLogger(__name__)

# Initialize Ollama client for LOCAL server
if EMBEDDING_PROVIDER == "ollama":
    try:
        ollama_client = ollama.Client(host=OLLAMA_BASE_URL)
        logger.info(f"✅ Ollama client initialized at {OLLAMA_BASE_URL}")
    except Exception as e:
        logger.error(f"Failed to initialize Ollama client: {e}")
        ollama_client = None
else:
    ollama_client = None
    logger.error(f"Unsupported embedding provider: {EMBEDDING_PROVIDER}")

def embed(texts: Union[str, List[str]], model=None, tokenizer=None, batch_size=8) -> np.ndarray:
    """
    Embed texts using Ollama's local embedding model.
    
    Args:
        texts: Single text or list of texts to embed
        model: Kept for backward compatibility (not used)
        tokenizer: Kept for backward compatibility (not used)
        batch_size: Number of texts to process at once
        
    Returns:
        numpy array of embeddings normalized to unit length
    """
    if ollama_client is None:
        raise RuntimeError("Ollama client not initialized. Please ensure Ollama is running.")
    
    # Handle single string input
    if isinstance(texts, str):
        texts = [texts]
    
    embeddings = []
    
    # Process in batches
    for i in range(0, len(texts), batch_size):
        batch = texts[i:i + batch_size]
        
        try:
            for text in batch:
                # Call Ollama embedding API
                response = ollama_client.embeddings(
                    model=EMBED_MODEL_ID,
                    prompt=text
                )
                
                # Extract embedding from response
                if 'embedding' in response:
                    embeddings.append(response['embedding'])
                else:
                    logger.warning(f"No embedding in response for text: {text[:50]}...")
                    # Return zero vector as fallback (will be determined by actual dimension)
                    embeddings.append([0.0] * 1024)
                    
        except Exception as e:
            logger.error(f"Error embedding batch {i//batch_size + 1}: {e}")
            # Add zero vectors for failed embeddings
            for _ in range(len(batch)):
                embeddings.append([0.0] * 1024)
    
    # Convert to numpy array
    embeddings = np.array(embeddings, dtype=np.float32)
    
    # Normalize embeddings to unit length for cosine similarity
    norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
    norms = np.where(norms == 0, 1, norms)  # Avoid division by zero
    embeddings = embeddings / norms
    
    return embeddings

def embed_query(text: str, model=None, tokenizer=None) -> np.ndarray:
    """
    Embed a single query using Ollama's local embedding model.
    
    Args:
        text: Query text to embed
        model: Kept for backward compatibility (not used)
        tokenizer: Kept for backward compatibility (not used)
        
    Returns:
        numpy array of shape (1, embedding_dim) normalized to unit length
    """
    if ollama_client is None:
        raise RuntimeError("Ollama client not initialized. Please ensure Ollama is running.")
    
    try:
        # Call Ollama embedding API
        response = ollama_client.embeddings(
            model=EMBED_MODEL_ID,
            prompt=text
        )
        
        # Extract embedding from response
        if 'embedding' in response:
            vec = np.array([response['embedding']], dtype=np.float32)
        else:
            logger.warning(f"No embedding in response for query: {text[:50]}...")
            vec = np.zeros((1, 1024), dtype=np.float32)
        
        # Normalize to unit length
        norm = np.linalg.norm(vec)
        if norm > 0:
            vec = vec / norm
            
        return vec
        
    except Exception as e:
        logger.error(f"Error embedding query: {e}")
        # Return zero vector as fallback
        return np.zeros((1, 1024), dtype=np.float32)
