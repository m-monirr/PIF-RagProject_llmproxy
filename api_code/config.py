# Configuration constants for the pipeline
import os

# Ollama Embedding Configuration - LOCAL SETUP
EMBEDDING_PROVIDER = "ollama"  # Using local Ollama
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")  # Local Ollama server

# Qwen3-embedding model
EMBED_MODEL_ID = "qwen3-embedding"  # Qwen3-embedding model
EMBED_DIMENSION = 1024  # Will be verified with test script - typical for qwen3-embedding

# Note: To use Local Ollama:
# 1. Download Ollama from https://ollama.com/download
# 2. Start Ollama: ollama serve (Windows starts automatically)
# 3. Pull the model: ollama pull qwen3-embedding
# 4. Run your application

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
