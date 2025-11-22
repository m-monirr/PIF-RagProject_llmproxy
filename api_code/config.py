# Configuration constants for the pipeline

# Ollama Embedding Configuration
OLLAMA_BASE_URL = "http://localhost:11434"  # Default Ollama URL

# Qwen3-embedding model
EMBED_MODEL_ID = "qwen3-embedding"
EMBED_DIMENSION = 1024  # Qwen3-embedding dimension - verify with test_embedding_dimension.py

# Note: Run 'python test_embedding_dimension.py' to verify the actual dimension
# The qwen2.5-embedding model typically outputs 1024-dimensional embeddings

# Legacy settings (keep for backward compatibility during migration)
MAX_TOKENS = 8192
EMBED_BATCH_SIZE = 8

# Example input/output mapping for main script
year_to_filename_ar = {
    "2021": "PIF Annual Report 2021-ar",
    "2022": "PIF Annual Report 2022-ar",
    "2023": "PIF-2023-Annual-Report-AR"
}
year_to_filename_en = {
    "2021": "PIF Annual Report 2021",
    "2022": "PIF Annual Report 2022",
    "2023": "PIF-2023-Annual-Report-EN"
}
