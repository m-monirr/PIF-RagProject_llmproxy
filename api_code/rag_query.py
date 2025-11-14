from pathlib import Path
from transformers import AutoTokenizer, AutoModel
from api_code.config import EMBED_MODEL_ID, year_to_filename_ar, year_to_filename_en
from api_code.embedding import embed_query
from qdrant_client import QdrantClient
import re
import json
from typing import List, Dict, Optional

# Load model and tokenizer once
_tokenizer = AutoTokenizer.from_pretrained(EMBED_MODEL_ID)
_model = AutoModel.from_pretrained(EMBED_MODEL_ID)
_qdrant = QdrantClient(host='localhost', port=6333)

def is_arabic(text):
    """Detect if text contains Arabic characters"""
    arabic_pattern = re.compile(r'[\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF\uFB50-\uFDFF\uFE70-\uFEFF]')
    return bool(arabic_pattern.search(text))

def search_multiple_collections(question: str, is_arabic: bool, limit_per_collection: int = 3) -> List[Dict]:
    """Search across multiple years and collections for better coverage"""
    results = []
    
    if is_arabic:
        collections = year_to_filename_ar
    else:
        collections = year_to_filename_en
    
    query_vector = embed_query(question, _model, _tokenizer)
    
    # Search in all available years
    for year, filename in collections.items():
        try:
            collection_name = f"{filename}_collection"
            year_results = _qdrant.search(
                collection_name=collection_name,
                query_vector=query_vector[0],
                limit=limit_per_collection,
                with_payload=True,
                score_threshold=0.3  # Only include relevant results
            )
            
            for result in year_results:
                results.append({
                    'text': result.payload.get("text", ""),
                    'score': result.score,
                    'year': year,
                    'source': filename
                })
        except Exception as e:
            print(f"Error searching collection {collection_name}: {e}")
            continue
    
    # Sort by relevance score and remove duplicates
    results.sort(key=lambda x: x['score'], reverse=True)
    
    # Remove duplicate content (simple text similarity)
    unique_results = []
    seen_texts = set()
    for result in results:
        text_key = result['text'][:100]  # Use first 100 chars as key
        if text_key not in seen_texts:
            unique_results.append(result)
            seen_texts.add(text_key)
    
    return unique_results[:5]  # Return top 5 unique results

def generate_answer_from_context(question: str, context_chunks: List[Dict], is_arabic: bool) -> str:
    """Generate a comprehensive answer from multiple context chunks"""
    if not context_chunks:
        return "I couldn't find specific information about that in the PIF annual reports. Could you please rephrase your question or ask about a different aspect of PIF's investments?"
    
    # Combine and process context chunks for better readability
    combined_context = "\n\n".join([chunk['text'] for chunk in context_chunks])
    
    # Process the context to create a more natural response
    if is_arabic:
        # Generate a more natural Arabic response
        intro_phrases = [
            "بناءً على المعلومات المتاحة في تقارير صندوق الاستثمارات العامة:",
            "وفقاً لتقارير صندوق الاستثمارات العامة السنوية:",
            "تشير المعلومات المتاحة إلى أن:",
        ]
        intro = intro_phrases[0]  # Use first one for now
        
        # Clean and format the context
        formatted_context = combined_context.replace('\n\n', '\n').strip()
        
        # Create a structured response
        if len(formatted_context) > 800:
            # For longer responses, create a summary structure
            answer = f"{intro}\n\n{formatted_context[:800]}...\n\n💡 يمكنك طرح أسئلة أكثر تحديداً للحصول على معلومات أكثر تفصيلاً حول هذا الموضوع."
        else:
            answer = f"{intro}\n\n{formatted_context}"
            
    else:
        # Generate a more natural English response
        intro_phrases = [
            "Based on the PIF annual reports:",
            "According to the available information from PIF:",
            "The PIF annual reports indicate that:",
        ]
        intro = intro_phrases[0]  # Use first one for now
        
        # Clean and format the context
        formatted_context = combined_context.replace('\n\n', '\n').strip()
        
        # Create a structured response
        if len(formatted_context) > 800:
            # For longer responses, create a summary structure
            answer = f"{intro}\n\n{formatted_context[:800]}...\n\n💡 You can ask more specific questions to get detailed information about this topic."
        else:
            answer = f"{intro}\n\n{formatted_context}"
    
    return answer

def get_rag_answer(question: str) -> str:
    """Enhanced RAG function with better retrieval and answer generation"""
    try:
        # Detect language
        is_arabic_question = is_arabic(question)
        
        # Search across multiple collections
        context_chunks = search_multiple_collections(question, is_arabic_question)
        
        if not context_chunks:
            if is_arabic_question:
                return "عذراً، لم أجد معلومات محددة حول هذا السؤال في تقارير صندوق الاستثمارات العامة السنوية. يمكنك إعادة صياغة سؤالك أو السؤال عن جانب مختلف من استثمارات الصندوق."
            else:
                return "I'm sorry, I couldn't find specific information about that in the PIF annual reports. You can rephrase your question or ask about a different aspect of PIF's investments."
        
        # Generate comprehensive answer
        answer = generate_answer_from_context(question, context_chunks, is_arabic_question)
        
        return answer
        
    except Exception as e:
        print(f"Error in RAG processing: {e}")
        if is_arabic(question):
            return "عذراً، حدث خطأ في معالجة سؤالك. يرجى المحاولة مرة أخرى أو طرح سؤال مختلف."
        else:
            return "I'm sorry, there was an error processing your question. Please try again or ask a different question."

def get_rag_answer_with_sources(question: str) -> Dict:
    """Get RAG answer with source information for debugging"""
    try:
        is_arabic_question = is_arabic(question)
        context_chunks = search_multiple_collections(question, is_arabic_question)
        
        if not context_chunks:
            return {
                'answer': "No relevant information found",
                'sources': [],
                'confidence': 0.0
            }
        
        answer = generate_answer_from_context(question, context_chunks, is_arabic_question)
        
        return {
            'answer': answer,
            'sources': [{'year': chunk['year'], 'score': chunk['score']} for chunk in context_chunks],
            'confidence': context_chunks[0]['score'] if context_chunks else 0.0
        }
        
    except Exception as e:
        return {
            'answer': f"Error: {str(e)}",
            'sources': [],
            'confidence': 0.0
        }
