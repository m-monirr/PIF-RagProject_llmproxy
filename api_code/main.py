import logging
from pathlib import Path
from docling.chunking import HybridChunker
from docling_core.transforms.chunker.tokenizer.huggingface import HuggingFaceTokenizer
from transformers import AutoTokenizer
from api_code.config import MAX_TOKENS, EMBED_BATCH_SIZE, year_to_filename_ar, year_to_filename_en, EMBED_DIMENSION
from api_code.extraction import extract_from_pdf
from api_code.chunking import chunk_document
from api_code.embedding import embed
from api_code.qdrant_utils import create_qdrant_collection, upload_points, verify_collection_data

def process_report(input_pdf_path, output_dir, is_arabic):
    doc, doc_filename = extract_from_pdf(input_pdf_path, output_dir)
    
    # Create HuggingFace tokenizer instance first
    try:
        hf_tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
        tokenizer = HuggingFaceTokenizer(tokenizer=hf_tokenizer, max_tokens=MAX_TOKENS)
    except Exception as e:
        logging.error(f"Failed to create tokenizer: {e}")
        raise
    
    chunker = HybridChunker(tokenizer=tokenizer, merge_peers=True)
    chunk_iter = chunker.chunk(dl_doc=doc)
    
    all_chunks = []
    for i, chunk in enumerate(chunk_iter, 1):
        enriched_text = chunker.contextualize(chunk=chunk).strip()
        if len(enriched_text) < 100:
            continue
        all_chunks.append({
            "index": i,
            "text": enriched_text,
            "chunk_id": f"{doc_filename}_chunk_{i:03}"
        })
    
    if not all_chunks:
        logging.warning(f"No valid chunks found for {input_pdf_path}")
        return
    
    # Use Ollama embeddings (no need to pass model/tokenizer)
    texts = [chunk["text"] for chunk in all_chunks]
    vectors = embed(texts, batch_size=EMBED_BATCH_SIZE)
    
    # Use Qdrant server with correct dimension
    collection_name = f"{doc_filename}_collection"
    qdrant = create_qdrant_collection(collection_name, EMBED_DIMENSION)
    upload_points(qdrant, collection_name, vectors, all_chunks)
    
    # Verify the data was stored correctly
    logging.info(f"Verifying data storage for {collection_name}...")
    if verify_collection_data(qdrant, collection_name):
        logging.info(f"✅ Successfully processed and verified {len(all_chunks)} chunks for {input_pdf_path}")
    else:
        logging.warning(f"⚠️  Data verification issues for {input_pdf_path}")

def main():
    logging.basicConfig(level=logging.INFO)
    inputs = [
        (year_to_filename_ar, "output_ar_{}"),
        (year_to_filename_en, "output_en_{}")
    ]
    for mapping, output_fmt in inputs:
        for year, doc_filename in mapping.items():
            pdf_file = Path(f"{doc_filename}.pdf")
            output_dir = Path(output_fmt.format(year))
            is_arabic = "-ar" in doc_filename.lower()
            if not pdf_file.exists():
                logging.warning(f"File not found: {pdf_file}")
                continue
            process_report(pdf_file, output_dir, is_arabic)

if __name__ == "__main__":
    main()
