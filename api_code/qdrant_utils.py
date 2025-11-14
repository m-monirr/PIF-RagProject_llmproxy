import numpy as np
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
import logging

def create_qdrant_collection(collection_name, vector_size):
    qdrant = QdrantClient(host='localhost', port=6333)
    qdrant.recreate_collection(
        collection_name=collection_name,
        vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE)
    )
    return qdrant

def upload_points(qdrant, collection_name, vectors, chunks):
    points = [
        PointStruct(id=i, vector=vec.tolist(), payload={"text": chunk["text"]})
        for i, (vec, chunk) in enumerate(zip(vectors, chunks))
    ]
    qdrant.upload_points(collection_name=collection_name, points=points)
    logging.info(f"Uploaded {len(points)} points to Qdrant collection '{collection_name}'")

def search_collection(qdrant, collection_name, query_vector, limit=5, with_payload=True):
    return qdrant.search(
        collection_name=collection_name,
        query_vector=query_vector[0],
        limit=limit,
        with_payload=with_payload
    )
