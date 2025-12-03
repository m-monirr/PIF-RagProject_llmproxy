"""
Query processing and RAG retrieval functionality
"""

from .rag_query import (
    get_rag_answer,
    get_rag_answer_with_sources,
    is_arabic,
    search_multiple_collections
)

__all__ = [
    'get_rag_answer',
    'get_rag_answer_with_sources',
    'is_arabic',
    'search_multiple_collections',
]
