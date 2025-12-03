import re
from docling_core.transforms.chunker.tokenizer.huggingface import HuggingFaceTokenizer
from docling.chunking import HybridChunker

# Helper: filter lines in Markdown that are too short or meaningless
def is_valid_line(line: str) -> bool:
    line = line.strip()
    if not line:
        return False
    if len(line) < 5:
        return False
    if re.fullmatch(r"[|\\/\-=_*~.\s]+", line):
        return False
    if sum(c.isalnum() for c in line) / max(len(line), 1) < 0.3:
        return False
    return True

# Clean up Markdown before chunking
def clean_markdown(md: str) -> str:
    lines = md.splitlines()
    filtered_lines = [line for line in lines if is_valid_line(line)]
    return "\n".join(filtered_lines)

# Placeholder for chunking logic using HuggingFaceTokenizer and HybridChunker
def chunk_document(doc, tokenizer, max_tokens=8192, merge_peers=True):
    chunker = HybridChunker(tokenizer=tokenizer, merge_peers=merge_peers)
    return list(chunker.chunk(dl_doc=doc))