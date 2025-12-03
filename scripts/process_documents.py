"""
Document processing script - extracts, chunks, embeds, and uploads PDFs to Qdrant
Moved from api_code/main.py
"""

import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import logging
import requests
from docling.chunking import HybridChunker
from docling_core.transforms.chunker.tokenizer.huggingface import HuggingFaceTokenizer
from transformers import AutoTokenizer
from src.core.config import MAX_TOKENS, EMBED_BATCH_SIZE, year_to_filename_ar, year_to_filename_en, EMBED_DIMENSION
from src.core.extraction import extract_from_pdf
from src.core.chunking import chunk_document
from src.core.embedding import embed
from src.core.qdrant_utils import create_qdrant_collection, upload_points, verify_collection_data

def check_services():
    """Check if required services are running"""
    print("\n🔍 Checking required services...\n")
    
    services_ok = True
    
    # Check Qdrant
    try:
        response = requests.get("http://localhost:6333/collections", timeout=2)
        if response.status_code == 200:
            print("✅ Qdrant: Running")
        else:
            print("❌ Qdrant: Not responding")
            services_ok = False
    except:
        print("❌ Qdrant: Not running")
        print("   💡 Start with: python scripts/start_qdrant.py")
        services_ok = False
    
    # Check Ollama
    try:
        response = requests.get("http://localhost:11434/api/version", timeout=2)
        if response.status_code == 200:
            print("✅ Ollama: Running")
        else:
            print("❌ Ollama: Not responding")
            services_ok = False
    except:
        print("❌ Ollama: Not running")
        print("   💡 Start with: ollama serve (or auto-starts on Windows)")
        services_ok = False
    
    print()
    return services_ok

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

def find_pdf_file(doc_filename, project_root):
    """
    Search for PDF file in multiple locations:
    1. data/pdfs/ (new structure)
    2. Project root (old location)
    """
    # Try new location first
    pdf_path = project_root / "data" / "pdfs" / f"{doc_filename}.pdf"
    if pdf_path.exists():
        return pdf_path
    
    # Try old location (project root)
    pdf_path = project_root / f"{doc_filename}.pdf"
    if pdf_path.exists():
        return pdf_path
    
    return None

def main():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Check services first
    if not check_services():
        print("❌ Required services are not running!")
        print("\n📋 Please start services first:")
        print("   1. python scripts/start_qdrant.py")
        print("   2. ollama serve (if not auto-started)")
        print("\nOr run service check: python scripts/check_services.py")
        sys.exit(1)
    
    # Get project root
    root_dir = Path(__file__).parent.parent
    
    print("="*70)
    print("📚 PIF Annual Reports - Document Processing Pipeline")
    print("="*70)
    print(f"\n📂 Project directory: {root_dir}")
    print(f"🔍 Searching for PDF files...\n")
    
    # Check if data/pdfs directory exists, create if not
    pdfs_dir = root_dir / "data" / "pdfs"
    if not pdfs_dir.exists():
        print(f"📁 Creating directory: {pdfs_dir}")
        pdfs_dir.mkdir(parents=True, exist_ok=True)
    
    # Process configurations
    configs = [
        (year_to_filename_ar, "output_ar_{}", True, "Arabic"),
        (year_to_filename_en, "output_en_{}", False, "English")
    ]
    
    total_files = 0
    processed_files = 0
    missing_files = []
    
    for mapping, output_fmt, is_arabic, lang_name in configs:
        print(f"\n{'='*70}")
        print(f"🌐 Processing {lang_name} Reports")
        print(f"{'='*70}\n")
        
        for year, doc_filename in mapping.items():
            total_files += 1
            
            # Find PDF file
            pdf_file = find_pdf_file(doc_filename, root_dir)
            
            if pdf_file is None:
                print(f"❌ [{year}] File not found: {doc_filename}.pdf")
                missing_files.append(f"{doc_filename}.pdf")
                continue
            
            print(f"✅ [{year}] Found: {pdf_file.name}")
            print(f"   📍 Location: {pdf_file.parent}")
            
            # Set output directory
            output_dir = root_dir / "data" / "outputs" / output_fmt.format(year)
            output_dir.mkdir(parents=True, exist_ok=True)
            
            try:
                print(f"   🔄 Processing...")
                process_report(pdf_file, output_dir, is_arabic)
                processed_files += 1
                print(f"   ✅ Successfully processed!\n")
            except Exception as e:
                print(f"   ❌ Error processing: {str(e)}\n")
                logging.error(f"Failed to process {pdf_file}: {e}", exc_info=True)
    
    # Summary
    print("\n" + "="*70)
    print("📊 PROCESSING SUMMARY")
    print("="*70)
    print(f"✅ Successfully processed: {processed_files}/{total_files} files")
    print(f"❌ Failed/Missing: {total_files - processed_files}/{total_files} files")
    
    if missing_files:
        print(f"\n⚠️  Missing PDF files:")
        for filename in missing_files:
            print(f"   • {filename}")
        print(f"\n💡 Please place your PDF files in one of these locations:")
        print(f"   1. {root_dir / 'data' / 'pdfs'}/  (recommended)")
        print(f"   2. {root_dir}/  (project root)")
        print(f"\n📋 Expected filenames:")
        print(f"   Arabic: PIF Annual Report YYYY-ar.pdf or PIF-YYYY-Annual-Report-AR.pdf")
        print(f"   English: PIF Annual Report YYYY.pdf or PIF-YYYY-Annual-Report-EN.pdf")
    
    print("="*70 + "\n")

if __name__ == "__main__":
    main()
