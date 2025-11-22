import numpy as np
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
import logging
import time

logger = logging.getLogger(__name__)

def test_qdrant_connection(host='localhost', port=6333, max_retries=5):
    """Test Qdrant connection with retries"""
    for attempt in range(max_retries):
        try:
            client = QdrantClient(host=host, port=port)
            # Try to get collections to verify connection
            client.get_collections()
            logger.info(f"✅ Successfully connected to Qdrant at {host}:{port}")
            return client
        except Exception as e:
            logger.warning(f"Attempt {attempt + 1}/{max_retries}: Failed to connect to Qdrant: {e}")
            if attempt < max_retries - 1:
                wait_time = 2 ** attempt  # Exponential backoff
                logger.info(f"Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
            else:
                logger.error("Failed to connect to Qdrant after all retries")
                raise ConnectionError(
                    f"Could not connect to Qdrant at {host}:{port}. "
                    "Please ensure Docker container is running:\n"
                    "docker run -p 6333:6333 -p 6334:6334 "
                    "-v \"<your-path>\\qdrant_storage\":/qdrant/storage qdrant/qdrant"
                )

def create_qdrant_collection(collection_name, vector_size, host='localhost', port=6333):
    """Create or recreate a Qdrant collection with error handling"""
    try:
        # Test connection first
        qdrant = test_qdrant_connection(host, port)
        
        # Check if collection exists
        try:
            collections = qdrant.get_collections().collections
            existing_collection = next(
                (c for c in collections if c.name == collection_name), 
                None
            )
            
            if existing_collection:
                logger.info(f"Collection '{collection_name}' already exists, deleting...")
                qdrant.delete_collection(collection_name=collection_name)
                logger.info(f"Deleted existing collection '{collection_name}'")
                time.sleep(1)  # Give Qdrant time to clean up
        except Exception as e:
            logger.warning(f"Error checking existing collection: {e}")
        
        # Create new collection
        logger.info(f"Creating collection '{collection_name}' with vector size {vector_size}...")
        qdrant.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE)
        )
        logger.info(f"✅ Successfully created collection '{collection_name}'")
        
        return qdrant
        
    except Exception as e:
        logger.error(f"Failed to create Qdrant collection: {e}")
        raise

def verify_collection_data(qdrant, collection_name):
    """Verify data integrity in a collection"""
    try:
        # Get collection info
        info = qdrant.get_collection(collection_name)
        
        logger.info(f"📊 Collection '{collection_name}' statistics:")
        logger.info(f"  - Total points: {info.points_count}")
        logger.info(f"  - Segments: {info.segments_count}")
        
        # Sample some points to verify
        if info.points_count > 0:
            sample, _ = qdrant.scroll(
                collection_name=collection_name,
                limit=5,
                with_payload=True,
                with_vectors=True
            )
            
            logger.info(f"  - Sample verified: {len(sample)} points")
            
            # Check for issues
            issues = []
            for point in sample:
                if not point.vector or len(point.vector) == 0:
                    issues.append(f"Point {point.id} has empty vector")
                if not point.payload or 'text' not in point.payload:
                    issues.append(f"Point {point.id} missing text payload")
            
            if issues:
                logger.warning(f"  ⚠️  Found {len(issues)} issues:")
                for issue in issues:
                    logger.warning(f"    - {issue}")
                return False
            else:
                logger.info(f"  ✅ All sampled points are valid")
                return True
        else:
            logger.warning(f"  ⚠️  Collection is empty!")
            return False
            
    except Exception as e:
        logger.error(f"Failed to verify collection: {e}")
        return False

def upload_points(qdrant, collection_name, vectors, chunks, batch_size=100):
    """Upload points to Qdrant collection with batching and error handling"""
    try:
        total_points = len(vectors)
        logger.info(f"Uploading {total_points} points to collection '{collection_name}'...")
        
        # Upload in batches to avoid timeouts
        for i in range(0, total_points, batch_size):
            batch_end = min(i + batch_size, total_points)
            batch_vectors = vectors[i:batch_end]
            batch_chunks = chunks[i:batch_end]
            
            points = [
                PointStruct(
                    id=idx, 
                    vector=vec.tolist(), 
                    payload={"text": chunk["text"]}
                )
                for idx, (vec, chunk) in enumerate(zip(batch_vectors, batch_chunks), start=i)
            ]
            
            # Upload with wait
            qdrant.upload_points(
                collection_name=collection_name, 
                points=points,
                wait=True
            )
            
            logger.info(f"Uploaded batch {i//batch_size + 1}: points {i+1}-{batch_end}/{total_points}")
        
        logger.info(f"✅ Successfully uploaded all {total_points} points to '{collection_name}'")
        
        # Verify the upload
        logger.info(f"🔍 Verifying uploaded data...")
        if verify_collection_data(qdrant, collection_name):
            logger.info(f"✅ Data verification passed!")
        else:
            logger.warning(f"⚠️  Data verification found issues!")
        
    except Exception as e:
        logger.error(f"Failed to upload points: {e}")
        raise

def search_collection(qdrant, collection_name, query_vector, limit=5, with_payload=True):
    """Search collection with error handling"""
    try:
        return qdrant.search(
            collection_name=collection_name,
            query_vector=query_vector[0],
            limit=limit,
            with_payload=with_payload
        )
    except Exception as e:
        logger.error(f"Failed to search collection '{collection_name}': {e}")
        raise
