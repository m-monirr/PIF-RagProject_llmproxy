import numpy as np
import torch
from transformers import AutoTokenizer, AutoModel

# Batch embedding for a list of texts
def embed(texts, model, tokenizer, batch_size=8):
    embeddings = []
    for i in range(0, len(texts), batch_size):
        batch = texts[i:i + batch_size]
        inputs = tokenizer(batch, padding=True, truncation=True, return_tensors="pt")
        with torch.no_grad():
            model_output = model(**inputs)
        emb = model_output.last_hidden_state[:, 0]  # CLS token
        embeddings.extend(emb.cpu().numpy())
    embeddings = np.array(embeddings).astype("float32")
    embeddings /= np.linalg.norm(embeddings, axis=1, keepdims=True)
    return embeddings

# Single query embedding
def embed_query(text, model, tokenizer):
    tokens = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
    with torch.no_grad():
        model_output = model(**tokens)
    vec = model_output.last_hidden_state[:, 0].cpu().numpy()
    vec = vec / np.linalg.norm(vec)
    return vec.astype("float32")
