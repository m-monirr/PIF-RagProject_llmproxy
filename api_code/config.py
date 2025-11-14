# Configuration constants for the pipeline

EMBED_MODEL_ID = "BAAI/bge-m3"
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
