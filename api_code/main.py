import logging
from pathlib import Path
from transformers import AutoTokenizer, AutoModel
from docling_core.transforms.chunker.tokenizer.huggingface import HuggingFaceTokenizer
from docling.chunking import HybridChunker
from api_code.config import EMBED_MODEL_ID, MAX_TOKENS, EMBED_BATCH_SIZE, year_to_filename_ar, year_to_filename_en
from api_code.extraction import extract_from_pdf
from api_code.chunking import chunk_document
from api_code.embedding import embed
from api_code.qdrant_utils import create_qdrant_collection, upload_points

def process_report(input_pdf_path, output_dir, is_arabic):
    doc, doc_filename = extract_from_pdf(input_pdf_path, output_dir)
    tokenizer = HuggingFaceTokenizer(
        tokenizer=AutoTokenizer.from_pretrained(EMBED_MODEL_ID),
        max_tokens=MAX_TOKENS,
    )
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
    embed_tokenizer = AutoTokenizer.from_pretrained(EMBED_MODEL_ID)
    embed_model = AutoModel.from_pretrained(EMBED_MODEL_ID)
    texts = [chunk["text"] for chunk in all_chunks]
    vectors = embed(texts, embed_model, embed_tokenizer, batch_size=EMBED_BATCH_SIZE)
    # Use Qdrant server
    collection_name = f"{doc_filename}_collection"
    qdrant = create_qdrant_collection(collection_name, vectors.shape[1])
    upload_points(qdrant, collection_name, vectors, all_chunks)
    logging.info(f"Processed and uploaded {len(all_chunks)} chunks for {input_pdf_path}")

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
