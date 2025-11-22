# Configuration constants for the pipeline

# Ollama Embedding Configuration
OLLAMA_BASE_URL = "http://localhost:11434"  # Default Ollama URL
EMBED_MODEL_ID = "qwen2.5:latest"  # Qwen3-embedding model
EMBED_DIMENSION = 1024  # Qwen3-embedding dimension (adjust based on actual model)

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
