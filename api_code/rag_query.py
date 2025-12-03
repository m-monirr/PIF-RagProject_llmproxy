from pathlib import Path
from api_code.config import year_to_filename_ar, year_to_filename_en
from api_code.embedding import embed_query
from api_code.llm_proxy import get_llm_proxy
from qdrant_client import QdrantClient
import re
import json
from typing import List, Dict, Optional
import logging

logger = logging.getLogger(__name__)

# Initialize Qdrant client once
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
    
    # Get query embedding using Ollama (no need to pass model/tokenizer)
    try:
        query_vector = embed_query(question)
    except Exception as e:
        logger.error(f"Error generating query embedding: {e}")
        return []
    
    # Search in all available years
    for year, filename in collections.items():
        try:
            collection_name = f"{filename}_collection"
            year_results = _qdrant.search(
                collection_name=collection_name,
                query_vector=query_vector[0].tolist(),
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
            logger.error(f"Error searching collection {collection_name}: {e}")
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

def generate_answer_from_context(question: str, context_chunks: List[Dict], is_arabic: bool, chat_history: List[Dict] = None) -> str:
    """Generate a comprehensive answer using LLM proxy with chat history"""
    if not context_chunks:
        if is_arabic:
            return "عذراً، لم أجد معلومات محددة حول هذا السؤال في تقارير صندوق الاستثمارات العامة السنوية."
        else:
            return "I couldn't find specific information about that in the PIF annual reports."
    
    # Combine context chunks
    combined_context = "\n\n".join([chunk['text'] for chunk in context_chunks])
    
    # Get LLM proxy instance
    try:
        llm_proxy = get_llm_proxy()
        
        # Generate answer using LLM with context AND chat history
        answer = llm_proxy.generate_answer(
            question=question,
            context=combined_context,
            is_arabic=is_arabic,
            chat_history=chat_history or [],  # Pass chat history
            max_tokens=500,
            temperature=0.3
        )
        
        return answer
        
    except Exception as e:
        logger.error(f"Error generating answer with LLM: {e}")
        
        # Fallback to simple context-based answer
        if is_arabic:
            intro = "بناءً على المعلومات المتاحة في تقارير صندوق الاستثمارات العامة:\n\n"
        else:
            intro = "Based on the PIF annual reports:\n\n"
        
        formatted_context = combined_context.replace('\n\n', '\n').strip()
        
        if len(formatted_context) > 800:
            answer = f"{intro}{formatted_context[:800]}..."
        else:
            answer = f"{intro}{formatted_context}"
        
        return answer

def get_rag_answer(question: str, chat_history: List[Dict] = None) -> str:
    """Enhanced RAG function with chat history support"""
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
        
        # Generate comprehensive answer WITH chat history
        answer = generate_answer_from_context(question, context_chunks, is_arabic_question, chat_history)
        
        return answer
        
    except Exception as e:
        logger.error(f"Error in RAG processing: {e}")
        if is_arabic(question):
            return "عذراً، حدث خطأ في معالجة سؤالك. يرجى المحاولة مرة أخرى أو طرح سؤال مختلف."
        else:
            return "I'm sorry, there was an error processing your question. Please try again or ask a different question."

def get_rag_answer_with_sources(question: str, chat_history: List[Dict] = None) -> Dict:
    """Get RAG answer with source information and chat history"""
    try:
        is_arabic_question = is_arabic(question)
        context_chunks = search_multiple_collections(question, is_arabic_question)
        
        if not context_chunks:
            return {
                'answer': "No relevant information found",
                'sources': [],
                'confidence': 0.0
            }
        
        answer = generate_answer_from_context(question, context_chunks, is_arabic_question, chat_history)
        
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
