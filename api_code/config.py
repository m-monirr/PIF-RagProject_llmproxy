# Configuration constants for the pipeline
import os

# Ollama Embedding Configuration - LOCAL SETUP
EMBEDDING_PROVIDER = "ollama"  # Using local Ollama
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")  # Fixed: Default Ollama port

# Qwen3-embedding model
EMBED_MODEL_ID = "qwen3-embedding"  # Qwen3-embedding model
EMBED_DIMENSION = 4096  # qwen3-embedding actual dimension (verified by test)

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

# LLM Proxy Configuration
LLM_PROXY_PORT = 4000
LLM_PROXY_CONFIG = "llm_proxy_config.yaml"
LLM_MAX_TOKENS = 500
LLM_TEMPERATURE = 0.3

# Ollama Cloud Configuration (Free Tier)
OLLAMA_CLOUD_BASE = "https://cloud.ollama.ai"
OLLAMA_PRIMARY_MODEL = "qwen2.5:3b"  # Fast and efficient
OLLAMA_FALLBACK_MODEL = "llama3.2:3b"  # Alternative
